---
sidebar_position: 1
---

# Examples - 0x10

## Example 1: Initiating a Default Session (0x01)

### Scenario
A technician wants to initiate the **Default Session** (0x01) to perform basic diagnostics and retrieve vehicle information like the VIN.

### Request Message

| Byte Position | Length (Bytes) | Field Name      | Description                                    |
|---------------|----------------|-----------------|------------------------------------------------|
| 0             | 1              | Service ID      | `0x10` - Diagnostic Session Control            |
| 1             | 1              | Subfunction     | `0x01` - Default Session                      |

**Request Example:**
```
0x10 0x01
```

### Response Message

| Byte Position | Length (Bytes) | Field Name         | Description                                             |
|---------------|----------------|--------------------|---------------------------------------------------------|
| 0             | 1              | Service ID         | `0x50` - Positive Response (indicating session start)   |
| 1             | 1              | Subfunction        | `0x01` - Indicates Default Session has been initiated  |

**Response Example:**
```
0x50 0x01
```

---

## Example 2: Initiating a Programming Session (0x02)

### Scenario
The technician needs to initiate the **Programming Session** (0x02) for ECU flashing or reprogramming.

### Request Message

| Byte Position | Length (Bytes) | Field Name      | Description                                    |
|---------------|----------------|-----------------|------------------------------------------------|
| 0             | 1              | Service ID      | `0x10` - Diagnostic Session Control            |
| 1             | 1              | Subfunction     | `0x02` - Programming Session                   |

**Request Example:**
```
0x10 0x02
```

### Response Message

| Byte Position | Length (Bytes) | Field Name         | Description                                             |
|---------------|----------------|--------------------|---------------------------------------------------------|
| 0             | 1              | Service ID         | `0x50` - Positive Response (indicating session start)   |
| 1             | 1              | Subfunction        | `0x02` - Indicates Programming Session has been started |

**Response Example:**
```
0x50 0x02
```

---

## Example 3: Switching to an Extended Diagnostic Session (0x03)

### Scenario
The technician needs to switch to an **Extended Diagnostic Session** (0x03) to perform in-depth diagnostics, such as clearing DTCs and calibrating ECUs.

### Request Message

| Byte Position | Length (Bytes) | Field Name      | Description                                    |
|---------------|----------------|-----------------|------------------------------------------------|
| 0             | 1              | Service ID      | `0x10` - Diagnostic Session Control            |
| 1             | 1              | Subfunction     | `0x03` - Extended Diagnostic Session           |

**Request Example:**
```
0x10 0x03
```

### Response Message

| Byte Position | Length (Bytes) | Field Name         | Description                                             |
|---------------|----------------|--------------------|---------------------------------------------------------|
| 0             | 1              | Service ID         | `0x50` - Positive Response (indicating session switch)  |
| 1             | 1              | Subfunction        | `0x03` - Indicates Extended Diagnostic Session is active |

**Response Example:**
```
0x50 0x03
```

---

## Example 4: Initiating a Safety System Diagnostic Session (0x04)

### Scenario
The technician needs to diagnose safety-critical subsystems like airbags or braking systems, so they initiate the **Safety System Diagnostic Session** (0x04).

### Request Message

| Byte Position | Length (Bytes) | Field Name      | Description                                    |
|---------------|----------------|-----------------|------------------------------------------------|
| 0             | 1              | Service ID      | `0x10` - Diagnostic Session Control            |
| 1             | 1              | Subfunction     | `0x04` - Safety System Diagnostic Session     |

**Request Example:**
```
0x10 0x04
```

### Response Message

| Byte Position | Length (Bytes) | Field Name         | Description                                             |
|---------------|----------------|--------------------|---------------------------------------------------------|
| 0             | 1              | Service ID         | `0x50` - Positive Response (indicating session start)   |
| 1             | 1              | Subfunction        | `0x04` - Indicates Safety System Diagnostic Session active |

**Response Example:**
```
0x50 0x04
```

---

## Example 5: Error Handling - Conditions Not Correct (0x22)

### Scenario
The technician attempts to initiate an **Extended Diagnostic Session** (0x03), but the ECU cannot enter the session due to a current condition (e.g., the ECU is locked or busy).

### Request Message

| Byte Position | Length (Bytes) | Field Name      | Description                                    |
|---------------|----------------|-----------------|------------------------------------------------|
| 0             | 1              | Service ID      | `0x10` - Diagnostic Session Control            |
| 1             | 1              | Subfunction     | `0x03` - Extended Diagnostic Session           |

**Request Example:**
```
0x10 0x03
```

### Response Message (Error: Conditions Not Correct)

| Byte Position | Length (Bytes) | Field Name           | Description                                             |
|---------------|----------------|----------------------|---------------------------------------------------------|
| 0             | 1              | Service ID           | `0x7F` - Negative Response (indicating error)           |
| 1             | 1              | Service ID           | `0x10` - Diagnostic Session Control                    |
| 2             | 1              | Negative Response Code | `0x22` - Conditions Not Correct                        |

**Response Example:**
```
0x7F 0x10 0x22
```

---

## Python Example Code for Diagnostic Session Control (0x10)

The following Python code demonstrates how to send a UDS request to initiate and switch between diagnostic sessions using the `python-can` library, assuming a CAN interface (e.g., USB-to-CAN adapter).

### Python Code to Send UDS Request (Initiate Extended Diagnostic Session)

```python
import can
import struct

# Define CAN interface
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Function to send UDS request for Diagnostic Session Control
def send_diagnostic_session_request(subfunction):
    # Construct UDS request message for diagnostic session control
    message = bytearray()
    message.append(0x10)  # Service ID for Diagnostic Session Control
    message.append(subfunction)  # Subfunction to control the session
    
    # Send message over CAN bus
    bus.send(can.Message(arbitration_id=0x7E0, data=message))

# Send request to switch to Extended Diagnostic Session
send_diagnostic_session_request(0x03)
print("Request sent to switch to Extended Diagnostic Session")
```

### Python Code to Receive UDS Response

```python
def receive_diagnostic_session_response():
    # Listen for a CAN response message
    message = bus.recv()
    if message:
        print(f"Received CAN message: {message}")
        # Parse UDS response
        if message.data[0] == 0x50:  # Response to Diagnostic Session Control
            print("Diagnostic Session Control response received")
            session_subfunction = message.data[1]
            print(f"Session switched to: {session_subfunction}")
        elif message.data[0] == 0x7F:  # Negative response
            print("Error response received")
            error_code = message.data[2]
            print(f"Error Code: {error_code}")

# Wait for response (this is a simple blocking example)
receive_diagnostic_session_response()
```

---

## CAPL Example Code for Diagnostic Session Control (0x10)

The following CAPL script demonstrates sending a UDS request to initiate the **Default Session** and handle the response.

### CAPL Script to Initiate Default Session

```capl
variables
{
  msTimer timer1;
}

on start
{
  // Send UDS request to initiate Default Session
  output(0x10, 0x01);  // 0x10 is the Service ID, 0x01 is the Default Session subfunction
}

on message 0x7E8
{
  if (this.byte(0) == 0x50)  // Response to Diagnostic Session Control (0x10)
  {
    write("Diagnostic Session Control response received");
    if (this.byte(1) == 0x01)
    {
      write("Default Session initiated successfully");
    }
  }
}
```

---

## Conclusion

The **Diagnostic Session Control (0x10)** service is essential for managing diagnostic access levels within the vehicle's ECUs. Through UDS, diagnostic tools can initiate, switch, and terminate various diagnostic sessions such as **Default**, **Programming**, **Extended**, and **Safety System** sessions. By understanding the service ID, sub-functions, and message formats, automotive engineers can enhance diagnostic tool capabilities, ensuring seamless access to essential vehicle data and functions. 

These Python and CAPL examples demonstrate how to implement the **Diagnostic Session Control** service, handle responses, and address potential error scenarios.