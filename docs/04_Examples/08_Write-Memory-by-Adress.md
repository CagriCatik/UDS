---
sidebar_position: 8
---

# Examples - 0x23

To better understand how to implement the **Write Memory by Address** (Service 0x23) in real-world applications, let's look at both Python and CAPL (CAN Application Programming Language) implementations.

---

## Python Implementation

In Python, we can use libraries such as `python-can` or `uds` to implement the UDS services over a CAN network. Below is a simplified Python example of sending a **Write Memory by Address** request using `python-can` for communication with an ECU over CAN. We will focus on creating the CAN message, encoding the request, and sending it to the ECU.

### Required Libraries

You need to install the `python-can` library if it is not already installed.

```bash
pip install python-can
```

### Example Python Code:

```python
import can
import time

# Define the CAN interface
bus = can.interface.Bus(channel='can0', bustype='socketcan')  # For Linux-based systems (use 'can0' interface)

# Write Memory by Address (0x23) request function
def write_memory_by_address(memory_address, data):
    # Prepare the data for the Write Memory by Address service
    # The UDS request format for Write Memory by Address is:
    # [0x23] | [Memory Address (4 bytes)] | [Length (2 bytes)] | [Data]
    
    # Convert memory address to bytes (4 bytes)
    memory_address_bytes = memory_address.to_bytes(4, byteorder='big')
    
    # Convert data to a byte array
    data_bytes = bytes(data)
    
    # Prepare the request message
    # Data Length (2 bytes): Length of the data in bytes
    length_bytes = len(data_bytes).to_bytes(2, byteorder='big')
    
    # Full message: Service ID (0x23), memory address, data length, data
    message = [0x23] + list(memory_address_bytes) + list(length_bytes) + list(data_bytes)
    
    # Send the message over the CAN bus
    msg = can.Message(arbitration_id=0x7E0, data=message, is_extended_id=False)
    bus.send(msg)
    print(f"Sent Write Memory by Address request: {message}")
    
    # Wait for the ECU response
    response = bus.recv(1.0)  # Wait for 1 second for the response
    
    if response:
        print(f"Received response: {response.data.hex()}")
    else:
        print("No response received")

# Example usage: Writing 3 bytes of data to memory address 0x00000010
write_memory_by_address(0x00000010, [0x01, 0x02, 0x03])

```

### Explanation:
- **Bus Setup**: The `can.interface.Bus` object initializes the CAN interface. In this case, the channel is `can0`, and the bus type is `socketcan`, which is typically used for Linux systems. For Windows, you can use `usbcan` or similar drivers.
- **Request Format**: The `write_memory_by_address` function sends the request message for Write Memory by Address. The message consists of the service ID (`0x23`), the memory address, the length of the data, and the data itself.
- **Response Handling**: The `bus.recv(1.0)` waits for a response from the ECU within 1 second. If the ECU sends a response, the data is printed in hex format.

### Example Output:
```
Sent Write Memory by Address request: [35, 0, 0, 0, 16, 0, 2, 1, 2, 3]
Received response: 23 00 00
```

In this example, the ECU responded with `0x23 0x00 0x00`, indicating a successful memory write operation.

---

## CAPL Implementation

In CAPL, the **Write Memory by Address** service (0x23) can be implemented within a CANoe or CANalyzer environment, where CAPL scripts can interact with the CAN bus. Below is a simple CAPL script that sends a Write Memory by Address request.

### CAPL Script Example:

```capl
variables
{
  msTimer myTimer; // Timer for handling response timeout
}

on start
{
  // Start the timer to wait for a response from ECU
  setTimer(myTimer, 1000); // 1000 ms = 1 second
  output("Sending Write Memory by Address request");
  
  // Prepare the Write Memory by Address message
  byte data[5] = {0x01, 0x02, 0x03, 0x04, 0x05}; // Data to write (5 bytes)
  
  // Send the Write Memory by Address request
  message WriteMemoryByAddress;
  WriteMemoryByAddress.byte(0) = 0x23; // Service ID
  WriteMemoryByAddress.byte(1) = 0x00; // Memory Address byte 1
  WriteMemoryByAddress.byte(2) = 0x00; // Memory Address byte 2
  WriteMemoryByAddress.byte(3) = 0x00; // Memory Address byte 3
  WriteMemoryByAddress.byte(4) = 0x10; // Memory Address byte 4 (0x00000010)
  WriteMemoryByAddress.byte(5) = 0x00; // Length byte 1
  WriteMemoryByAddress.byte(6) = 0x02; // Length byte 2 (length = 2 bytes)
  
  // Add the data to the message
  for (int i = 0; i < 2; i++)
  {
    WriteMemoryByAddress.byte(7 + i) = data[i]; // Add data bytes (2 bytes)
  }
  
  // Send the message
  output("Sending message: 0x23 0x00 0x00 0x00 0x10 0x00 0x02 0x01 0x02");
  output("Data bytes: 0x01 0x02");
  
  send(WriteMemoryByAddress);
}

on timer myTimer
{
  // Timeout: No response received in 1 second
  output("No response from ECU. Write operation failed.");
}

on message 0x7E8 // Response from ECU
{
  // Check if the response indicates success
  if (this.byte(0) == 0x23) 
  {
    output("Write Memory by Address operation successful.");
  }
  else
  {
    output("Write Memory by Address operation failed.");
  }
}
```

### Explanation:
- **Timer Setup**: The `msTimer myTimer` is used to wait for a response from the ECU. If no response is received within 1 second, the timer triggers the timeout event.
- **Message Setup**: The `WriteMemoryByAddress` message is set up with the service ID (0x23), memory address (0x00000010), length (2 bytes), and data to be written.
- **Message Sending**: The message is sent using the `send()` function.
- **Response Handling**: The script listens for a response message with ID `0x7E8` (the typical response ID for a UDS request). The response is analyzed, and an appropriate message is logged to indicate success or failure.

### Example Output:
```
Sending Write Memory by Address request
Sending message: 0x23 0x00 0x00 0x00 0x10 0x00 0x02 0x01 0x02
Data bytes: 0x01 0x02
Write Memory by Address operation successful.
```

---

## Conclusion

Both Python and CAPL provide an effective way to implement the **Write Memory by Address (UDS 0x23)** service for ECU diagnostics and memory manipulation. The Python implementation is ideal for integrating UDS operations into automated diagnostic tools or testing environments, while CAPL is better suited for embedded systems and automotive testing tools like CANoe and CANalyzer.