---
sidebar_position: 2
---

# Examples - 0x19

## Example 1: Enabling a Specific DTC

### Scenario
A technician wants to enable a specific Diagnostic Trouble Code (DTC) for testing. In this case, we’ll enable DTC `0x1234` as a permanent fault code (`0x00`).

### Request Message

| Byte Position | Length (Bytes) | Field Name     | Description                                      |
|---------------|----------------|----------------|--------------------------------------------------|
| 0             | 1              | Service ID     | `0x19` - Control DTC Settings                   |
| 1             | 1              | Subfunction    | `0x01` - Enable DTC                            |
| 2             | 1              | DTC Type       | `0x00` - Permanent DTC                        |
| 3             | 2              | DTC            | `0x1234` - The specific DTC to enable           |
| 5             | 1              | Additional Info| `0x00` - No additional parameters              |

**Request Example:**
```
0x19 0x01 0x00 0x12 0x34 0x00
```

### Response Message

| Byte Position | Length (Bytes) | Field Name         | Description                                                |
|---------------|----------------|--------------------|------------------------------------------------------------|
| 0             | 1              | Service ID         | `0x59` - Response to Control DTC Settings service          |
| 1             | 1              | Positive Response  | `0x00` - Positive response code (Success)                  |
| 2             | 1              | Additional Info    | `0x00` - No additional information (Success)               |

**Response Example:**
```
0x59 0x00 0x00
```

---

## Example 2: Disabling a Specific DTC

### Scenario
A technician needs to disable a specific DTC (`0x5678`) temporarily during a diagnostic session for testing purposes.

### Request Message

| Byte Position | Length (Bytes) | Field Name     | Description                                      |
|---------------|----------------|----------------|--------------------------------------------------|
| 0             | 1              | Service ID     | `0x19` - Control DTC Settings                   |
| 1             | 1              | Subfunction    | `0x02` - Disable DTC                           |
| 2             | 1              | DTC Type       | `0x00` - Permanent DTC                         |
| 3             | 2              | DTC            | `0x5678` - The specific DTC to disable          |
| 5             | 1              | Additional Info| `0x01` - Confirmation byte for disabling DTC   |

**Request Example:**
```
0x19 0x02 0x00 0x56 0x78 0x01
```

### Response Message

| Byte Position | Length (Bytes) | Field Name         | Description                                                |
|---------------|----------------|--------------------|------------------------------------------------------------|
| 0             | 1              | Service ID         | `0x59` - Response to Control DTC Settings service          |
| 1             | 1              | Positive Response  | `0x00` - Positive response code (Success)                  |
| 2             | 1              | Additional Info    | `0x00` - No additional information (Success)               |

**Response Example:**
```
0x59 0x00 0x00
```

---

## Example 3: Modifying DTC Settings (Advanced Case)

### Scenario
A technician wants to modify the behavior of a DTC by changing its status to "pending" (`0x01`) instead of permanent (`0x00`) to simulate an intermediate state during testing.

### Request Message

| Byte Position | Length (Bytes) | Field Name     | Description                                      |
|---------------|----------------|----------------|--------------------------------------------------|
| 0             | 1              | Service ID     | `0x19` - Control DTC Settings                   |
| 1             | 1              | Subfunction    | `0x03` - Modify DTC Settings                    |
| 2             | 1              | DTC Type       | `0x01` - Pending DTC                           |
| 3             | 2              | DTC            | `0xABCD` - The specific DTC to modify            |
| 5             | 1              | Additional Info| `0x00` - No additional parameters               |

**Request Example:**
```
0x19 0x03 0x01 0xAB 0xCD 0x00
```

### Response Message

| Byte Position | Length (Bytes) | Field Name         | Description                                                |
|---------------|----------------|--------------------|------------------------------------------------------------|
| 0             | 1              | Service ID         | `0x59` - Response to Control DTC Settings service          |
| 1             | 1              | Positive Response  | `0x00` - Positive response code (Success)                  |
| 2             | 1              | Additional Info    | `0x00` - No additional information (Success)               |

**Response Example:**
```
0x59 0x00 0x00
```

---

## Python Example Code for Sending UDS Request

The following Python code demonstrates how to send a UDS request using the `python-can` library for CAN bus communication. It assumes you're working with a CAN interface like a USB-to-CAN adapter.

### Python Code to Send UDS Request (Enable DTC)

```python
import can
import struct

# Define CAN interface
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Function to send UDS request
def send_uds_request(service_id, subfunction, dtc_type, dtc):
    # Construct UDS request message
    message = bytearray()
    message.append(service_id)  # Service ID (0x19 for Control DTC Settings)
    message.append(subfunction)  # Subfunction (e.g., 0x01 for Enable DTC)
    message.append(dtc_type)  # DTC Type (0x00 for Permanent)
    message.extend(struct.pack(">H", dtc))  # DTC (2-byte value)
    
    # Send message over CAN bus
    bus.send(can.Message(arbitration_id=0x7E0, data=message))

# Send request to enable DTC 0x1234
send_uds_request(0x19, 0x01, 0x00, 0x1234)
print("UDS request sent to enable DTC 0x1234")
```

### Python Code to Receive UDS Response

```python
def receive_uds_response():
    # Listen for a CAN response message
    message = bus.recv()
    if message:
        print(f"Received CAN message: {message}")
        # Parse UDS response
        if message.data[0] == 0x59:  # Response to 0x19
            print("Control DTC Settings response received")
            response_code = message.data[1]
            if response_code == 0x00:
                print("DTC enabled successfully")
            else:
                print(f"Error: {response_code}")
        else:
            print("Unexpected message type")

# Wait for response (this is a simple blocking example)
receive_uds_response()
```

---

## CAPL Example Code for UDS (Enable DTC)

CAPL (CAN Application Programming Language) is used to script diagnostics in CANoe and CANalyzer. Below is a CAPL script to send a UDS request to enable a DTC.

```capl
variables
{
  msTimer timer1;
}

on start
{
  // Send UDS request to enable DTC 0x1234
  output(0x19, 0x01, 0x00, 0x12, 0x34, 0x00);
}

on message 0x7E8
{
  if (this.byte(0) == 0x59)  // Response to Control DTC Settings (0x19)
  {
    if (this.byte(1) == 0x00)
    {
      write("DTC enabled successfully");
    }
    else
    {
      write("Error in enabling DTC");
    }
  }
}
```

---

## Conclusion

These examples illustrate the implementation of the "Control DTC Settings" service (Service ID 0x19) in various scenarios. By understanding the request and response message formats and implementing them using Python or CAPL, you can control the DTC settings in a vehicle’s ECUs for testing and diagnostic purposes.

When working with UDS, always ensure that your diagnostic tools handle DTC codes and responses correctly and follow the best practices for error handling and security.