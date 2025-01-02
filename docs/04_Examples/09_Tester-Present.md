---
sidebar_position: 8
---

# Examples - 0x03

Below are realistic examples demonstrating the usage of the **Tester Present** service (Service ID 0x03) in both **Python** and **CAPL**. These examples focus on sending **Tester Present** requests and handling the response, using the two sub-functions **0x00** (no suppression of response) and **0x80** (suppress response).

---

## Python Example: Tester Present Request

In Python, we can use the `python-can` library to simulate sending a **Tester Present** request over the CAN bus. The `python-can` library allows interaction with CAN interfaces (e.g., USB-to-CAN adapters) to send and receive messages.

### Prerequisites:
1. Install `python-can`:
   ```bash
   pip install python-can
   ```

2. Configure the CAN interface (e.g., SocketCAN for Linux or Vector for Windows).

### Python Code to Send a Tester Present Request:

```python
import can
import time

# Initialize CAN interface (adjust for your specific hardware and OS)
can_interface = 'can0'  # Example for Linux (use 'vcan0' for virtual CAN)
bus = can.interface.Bus(can_interface, bustype='socketcan')

def send_tester_present(subfunction):
    """Sends a Tester Present request (Service ID 0x03)"""
    message = can.Message(
        arbitration_id=0x7E0,  # Standard ECU address, change if needed
        data=[0x03, subfunction],  # Service ID 0x03 and Sub-function
        is_extended_id=False
    )
    
    try:
        bus.send(message)
        print(f"Tester Present (sub-function 0x{subfunction:X}) request sent.")
    except can.CanError:
        print("Failed to send Tester Present request.")

def receive_response():
    """Waits for the response message and prints it."""
    while True:
        message = bus.recv()  # Receive message from the CAN bus
        if message.arbitration_id == 0x7E8:  # Assuming response is from ECU (change if needed)
            print(f"Received response: {message.data.hex()}")
            break

# Send Tester Present with Sub-function 0x00 (no suppression of response)
send_tester_present(0x00)
time.sleep(0.1)  # Wait to allow ECU response
receive_response()

# Send Tester Present with Sub-function 0x80 (suppress response)
send_tester_present(0x80)
time.sleep(0.1)  # Wait to allow ECU response
receive_response()
```

### Explanation:
- **Bus Initialization**: The CAN interface is initialized using `python-can` (replace `'can0'` with your actual interface name).
- **send_tester_present()**: This function sends the **Tester Present** request with the given sub-function (0x00 or 0x80).
  - The message structure is built with **Service ID 0x03** and the appropriate **sub-function**.
- **receive_response()**: This function listens for a response on the CAN bus and prints the received data. It assumes a response from the ECU (with **arbitration ID 0x7E8**).

### Expected Output:
- For **Sub-function 0x00**, the ECU sends a response (positive response).
- For **Sub-function 0x80**, no response is expected (response is suppressed).

---

## CAPL Example: Tester Present Request

In **CAPL** (CANoe Programming Language), we can use a similar approach to send the **Tester Present** service request on the CAN network. CAPL is designed to simulate the communication between ECUs, so the example below demonstrates how you can implement this in a CANoe environment.

### CAPL Code to Send a Tester Present Request:

```capl
variables
{
  msTimer testerPresentTimer;
}

on start
{
  // Start sending Tester Present requests periodically
  setTimer(testerPresentTimer, 100);  // Timer to trigger Tester Present every 100 ms
}

on timer testerPresentTimer
{
  // Send Tester Present with Sub-function 0x00 (no suppression)
  outputTesterPresent(0x00);
  
  // Reschedule the timer to keep sending Tester Present requests
  setTimer(testerPresentTimer, 100);  // Send again in 100 ms
}

void outputTesterPresent(int subFunction)
{
  message TesterPresentMessage;
  
  // Create the Tester Present request message (Service ID 0x03)
  TesterPresentMessage.byte(0) = 0x03;  // Service ID
  TesterPresentMessage.byte(1) = subFunction;  // Sub-function (0x00 or 0x80)
  
  // Send the message on the CAN bus
  output(TesterPresentMessage);
  
  // Log the sent message
  write("Sent Tester Present (Sub-function 0x%02X)", subFunction);
}

on message TesterPresentMessage
{
  // Handle responses from ECU here
  if (TesterPresentMessage.byte(0) == 0x03)
  {
    // Positive response for Sub-function 0x00
    write("Received response: Tester Present acknowledged (0x03).");
  }
  else
  {
    // Handle other cases (e.g., errors)
    write("Unexpected response received.");
  }
}
```

### Explanation:
- **Timer Setup**: The `testerPresentTimer` is set to trigger every 100 milliseconds. This ensures that the **Tester Present** request is periodically sent to the ECU.
- **outputTesterPresent()**: This function creates and sends the **Tester Present** message with the specified **sub-function**.
  - **Sub-function 0x00** sends a request without suppressing the response, while **Sub-function 0x80** suppresses the response.
- **Message Reception**: The `TesterPresentMessage` handler listens for responses from the ECU, specifically for a **Service ID 0x03** message.

### Expected Behavior in CANoe:
- The tester sends a **Tester Present** message every 100 ms.
- The response handler logs the response received from the ECU. If **Sub-function 0x00** is used, the ECU should reply with a positive response. If **Sub-function 0x80** is used, no response will be sent.

---

## Practical Considerations:
- **Timing**: In both examples, the timing is crucial. The **Tester Present** request must be sent periodically, typically at intervals that prevent the ECU from automatically transitioning back to the default session.
- **Error Handling**: Both Python and CAPL examples should include error handling for invalid responses, timeouts, or other issues that could arise during communication with the ECU.
- **Custom ECUs**: The arbitration IDs used in the examples (e.g., `0x7E0` for the tester and `0x7E8` for the ECU) are placeholders. You must adapt these to match the specific CAN IDs used in your test environment.

---

These examples show how the **Tester Present** service can be implemented in both **Python** and **CAPL**, providing a clear view of how diagnostic testers maintain a non-default session and keep the ECU active during extended or programming sessions.