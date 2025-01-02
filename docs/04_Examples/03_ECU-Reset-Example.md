---
sidebar_position: 3
---

# Examples - 0x11 

## 1.1 Example 1: Soft Reset Request (Sub-function 0x01)

In this case, we send a soft reset request to the ECU, which will reinitialize the ECU's internal software without powering it off.

Request Message Format:
```plaintext
[0x11] [0x01]
```

- 0x11: Service Identifier for ECU Reset.
- 0x01: Sub-function for soft reset.

This request asks the ECU to perform a soft reset. The ECU will clear internal states and reinitialize its software.

## 1.2 Example 2: Hard Reset Request (Sub-function 0x02)

In this case, we send a hard reset request to the ECU. This would involve a complete power cycle of the ECU to restart its hardware and software.

Request Message Format:
```plaintext
[0x11] [0x02]
```

- 0x11: Service Identifier for ECU Reset.
- 0x02: Sub-function for hard reset.

This request instructs the ECU to perform a hard reset. It will power cycle the ECU, effectively restarting the ECU at a hardware level.

---

# 2. ECU Reset Response Examples

## 2.1 Example 1: Positive Response (0x00)

If the ECU successfully processes the reset request (either soft or hard), it sends a positive response back to the diagnostic tool.

Response Message Format:
```plaintext
[0x11] [0x00]
```

- 0x11: Service Identifier for ECU Reset.
- 0x00: Positive response, indicating the ECU reset was successful.

This message indicates that the reset was successfully executed. The ECU is now either soft or hard reset, depending on the request.

## 2.2 Example 2: Negative Response with Error Code (0x11)

If the ECU cannot perform the reset, it sends a negative response with an appropriate error code. The error code will help identify the reason for the failure.

Response Message Format:
```plaintext
[0x11] [0x11] [0x22]
```

- 0x11: Service Identifier for ECU Reset.
- 0x11: Negative response, indicating an error occurred.
- 0x22: Error code indicating that conditions were not correct for the requested service.

Explanation of Error Code (0x22):
- 0x22: "Conditions Not Correct for Requested Service." This error could occur if the ECU is in a state that prevents a reset, such as during critical operations or while the ECU is locked.

---

# 3. Error Handling Example

When a diagnostic tool receives a negative response, it must handle the error appropriately. Below is an example of how the tool might respond to a timeout error or incorrect state.

## 3.1 Example 1: Timeout Error (0x33)

If there’s a timeout in communication between the diagnostic tool and the ECU, a timeout error (`0x33`) might be returned. This error typically occurs if the ECU does not respond within the expected timeframe.

Response Message Format:
```plaintext
[0x11] [0x11] [0x33]
```

- 0x11: Service Identifier for ECU Reset.
- 0x11: Negative response.
- 0x33: Error code indicating a timeout.

Explanation of Error Code (0x33):
- 0x33: "ECU Communication Timeout." This error happens when the ECU fails to respond to the reset request within the specified time window, often due to ECU malfunctions or communication issues.

## 3.2 Example 2: Invalid Reset Sub-function (0x12)

If the diagnostic tool requests a reset type (sub-function) that the ECU does not support, an error code `0x12` may be returned.

Response Message Format:
```plaintext
[0x11] [0x11] [0x12]
```

- 0x11: Service Identifier for ECU Reset.
- 0x11: Negative response.
- 0x12: Error code indicating the requested sub-function is not supported by the ECU.

Explanation of Error Code (0x12):
- 0x12: "Sub-function Not Supported." This occurs when the ECU does not support the specific reset type requested (e.g., the ECU may only support a soft reset and the diagnostic tool requests a hard reset).

---

# 4. Practical Use Cases for ECU Reset

## 4.1 Use Case 1: Post-Update ECU Reset

In this scenario, the ECU has just been flashed with a firmware update. A hard reset is required to apply the update and restart the ECU with the new software.

Request Example: A diagnostic tool sends the following message to trigger the reset:
```plaintext
0x11 0x02
```
This sends a hard reset request to the ECU.

Response Example: The ECU responds with:
```plaintext
0x11 0x00
```
This indicates that the hard reset was successfully performed and the ECU has rebooted with the new software.

## 4.2 Use Case 2: Error Recovery

The ECU has entered an error state due to a software issue. A soft reset is requested to restore it to normal operation.

Request Example: A diagnostic tool sends:
```plaintext
0x11 0x01
```
This sends a soft reset request to the ECU.

Response Example: The ECU successfully resets:
```plaintext
0x11 0x00
```
The ECU reinitializes its software, clears error states, and returns to normal operation.

## 4.3 Use Case 3: Diagnostic Testing

During diagnostic testing, the ECU may be reset to verify that it can handle errors, recover from failures, and perform properly after a reset.

Request Example: The diagnostic tool sends a hard reset to verify that the ECU can recover from a critical state:
```plaintext
0x11 0x02
```

Response Example: The ECU successfully processes the reset:
```plaintext
0x11 0x00
```
The test confirms that the ECU is able to return to a functional state after the reset.

---

# 5. Example of a Full Diagnostic Session for ECU Reset

Here’s an example of a full diagnostic session involving an ECU reset, starting from the initial session request to the final reset request and response.

1. Diagnostic Session Start (0x10)
   The diagnostic tool starts a session with the ECU to prepare for diagnostic communication.
   ```plaintext
   0x10 0x01
   ```

2. ECU Reset Request (Soft Reset, 0x11 0x01)
   The diagnostic tool sends a soft reset request to the ECU:
   ```plaintext
   0x11 0x01
   ```

3. ECU Response (Successful Soft Reset)
   The ECU successfully processes the reset:
   ```plaintext
   0x11 0x00
   ```

4. Diagnostic Session End (0x50)
   The diagnostic session ends after the reset operation is complete:
   ```plaintext
   0x50 0x00
   ```

This full sequence illustrates a typical ECU reset scenario, including starting the diagnostic session, requesting a reset, receiving a successful response, and then closing the session.

---

# 6. Using UDS Libraries to Implement ECU Reset in Python

If you're implementing a custom diagnostic tool to interact with ECUs, libraries like `python-uds` can be used to send and receive ECU reset requests.

## 6.1 Example Code to Send ECU Reset Request in Python

Here is a simple Python code snippet to send a soft reset request using the `python-uds` library:

```python
import uds
from uds.services import Reset

# Initialize UDS Client and connect to ECU
client = uds.Client('can0')  # Replace with your CAN interface

# Send soft reset request (0x01) to the ECU
reset_service = Reset(client)
response = reset_service.reset(0x01)  # Soft Reset (0x01)

# Check the response
if response.is_success():
    print("ECU successfully reset!")
else:
    print(f"Failed to reset ECU. Error code: {response.error_code}")
```

This script connects to the ECU over the CAN network, sends a soft reset request (0x01), and prints the result based on the response.

