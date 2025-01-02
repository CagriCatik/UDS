---
sidebar_position: 6
---

# Examples - 0x2E

## **1. Python Example: Write Data By Identifier (0x2E)**

In this example, the Python code communicates with a vehicle's ECU using the **CAN protocol** to send a **Write Data By Identifier (0x2E)** request. The code uses the `python-can` library to send and receive CAN messages.

### **Python Setup**

1. Install the `python-can` library:
   ```bash
   pip install python-can
   ```

2. **Python Script:**

```python
import can
import time

# Define the CAN bus interface (e.g., socketcan for Linux, can0 interface)
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Service ID for Write Data By Identifier (0x2E)
SERVICE_ID = 0x2E

# Example Data Identifier and Data to Write
data_identifier = 0x1234  # Example Data Identifier for engine calibration
data_to_write = [0x00, 0x00, 0x00, 0x05]  # Example data (e.g., new calibration value)

# Function to send the Write Data By Identifier request
def send_write_data_by_identifier():
    # Construct the request message
    request_message = [SERVICE_ID, data_identifier >> 8, data_identifier & 0xFF] + data_to_write
    # Create a CAN message object
    msg = can.Message(arbitration_id=0x7DF,  # Assuming 0x7DF is the standard CAN ID for diagnostics
                      data=request_message,
                      is_extended_id=False)
    try:
        # Send the message on the CAN bus
        bus.send(msg)
        print(f"Request Sent: {msg}")
    except can.CanError:
        print("Message sending failed.")

# Function to receive and handle the response
def receive_response():
    while True:
        msg = bus.recv()  # Wait for a response
        if msg:
            # Print the response message
            print(f"Response Received: {msg}")
            if msg.data[0] == SERVICE_ID:
                # Check for positive or negative response
                if msg.data[1] == 0x00:
                    print("Write Data Successful")
                else:
                    print(f"Error: Negative Response Code {msg.data[1]}")
            break
        time.sleep(0.1)  # Delay to avoid excessive CPU usage

# Sending the Write Data By Identifier request and waiting for response
send_write_data_by_identifier()
receive_response()
```

### **Explanation**:

- The **`send_write_data_by_identifier()`** function constructs a CAN message for the **0x2E Write Data By Identifier** service, which consists of the service ID (`0x2E`), the Data Identifier (`0x1234`), and the data to be written (`0x00000005`).
- The **`receive_response()`** function listens for a response on the CAN bus. It checks if the response matches the requested service ID and prints whether the operation was successful or if an error was encountered, based on the **Negative Response Code (NRC)**.

### **Example Output**:
```plaintext
Request Sent: Message(arbitration_id=2031, data=[46, 18, 52, 0, 0, 0, 5], is_extended_id=False)
Response Received: Message(arbitration_id=2031, data=[46, 0, 0, 0, 0, 0, 0, 0], is_extended_id=False)
Write Data Successful
```

This indicates that the **Write Data By Identifier (0x2E)** request was successful and the data was written to the ECU.

---

## **2. CAPL Example: Write Data By Identifier (0x2E)**

In **CAPL (CAN Application Programming Language)**, we can implement a similar functionality by defining a script that sends a **Write Data By Identifier** request and processes the response.

### **CAPL Script:**

```capl
variables
{
  msTimer writeTimer;  // Timer to manage write attempt timeouts
}

// Define constants for the CAN protocol
const long CAN_ID = 0x7DF; // Standard diagnostic CAN ID (0x7DF)
const byte SERVICE_ID = 0x2E;  // Write Data By Identifier service ID

// Example Data Identifier and data to write
const word dataIdentifier = 0x1234;  // Data Identifier for engine calibration
const byte dataToWrite[] = {0x00, 0x00, 0x00, 0x05};  // New calibration value to write

// Function to send Write Data By Identifier request
void sendWriteDataByIdentifier()
{
  byte message[8];  // CAN message buffer
  
  // Fill the message with the request data: Service ID, Data Identifier, and data to write
  message[0] = SERVICE_ID;
  message[1] = (dataIdentifier >> 8) & 0xFF;  // High byte of Data Identifier
  message[2] = dataIdentifier & 0xFF;         // Low byte of Data Identifier
  message[3] = dataToWrite[0];  // Data byte 1
  message[4] = dataToWrite[1];  // Data byte 2
  message[5] = dataToWrite[2];  // Data byte 3
  message[6] = dataToWrite[3];  // Data byte 4

  // Send the message on the CAN network
  output(CAN_ID, message, 7);
  writeTimer = setTimer(1000);  // Set a timer for response timeout
  output("Write Data Request Sent.");
}

// Function to handle response
on message CAN_ID
{
  byte response[8];
  
  // Check if the response is for Write Data By Identifier service
  if (this.message[0] == SERVICE_ID)
  {
    if (this.message[1] == 0x00)  // Positive response: 0x00 means success
    {
      output("Write Data Successful");
    }
    else
    {
      output("Error: Negative Response Code %X", this.message[1]);
    }
    cancelTimer(writeTimer);  // Stop the timeout timer
  }
  else
  {
    output("Unexpected response received.");
  }
}

// Start the Write Data By Identifier process
on start
{
  sendWriteDataByIdentifier();
}
```

### **Explanation**:

- The `sendWriteDataByIdentifier()` function constructs the CAN message with the **Service ID (0x2E)**, the **Data Identifier (0x1234)**, and the data to write (calibration value `0x00000005`).
- The script listens for the response to this message in the `on message CAN_ID` block. It checks if the first byte of the message matches the service ID (`0x2E`) and evaluates the second byte to determine if the operation was successful (positive response code `0x00`).
- If the response is valid, it outputs the success or failure of the write operation.

### **Example Output**:
```plaintext
Write Data Request Sent.
Write Data Successful
```

Or if an error occurs:
```plaintext
Write Data Request Sent.
Error: Negative Response Code 0x12  // Subfunction Not Supported
```

---

## **3. Detailed Example of Negative Response Codes in CAPL**

In this case, let’s simulate a scenario where a **Negative Response Code** (NRC) is returned. For example, the ECU could reject the write operation due to an invalid data identifier or due to not being in a valid session.

### **Example CAPL Response Simulation:**

Assume that when trying to write data to a protected identifier, the ECU returns `0x22 - Conditions Not Correct`:

**CAPL Script Handling NRC:**

```capl
on message CAN_ID
{
  byte response[8];
  
  // Check if the response is for Write Data By Identifier service
  if (this.message[0] == SERVICE_ID)
  {
    // Handle specific Negative Response Codes
    switch (this.message[1])
    {
      case 0x00: // Success
        output("Write Data Successful");
        break;
      case 0x22: // Conditions Not Correct
        output("Error: Conditions Not Correct (0x22)");
        break;
      case 0x31: // Request Out of Range
        output("Error: Request Out of Range (0x31)");
        break;
      case 0x33: // Security Access Denied
        output("Error: Security Access Denied (0x33)");
        break;
      default:
        output("Error: Unknown NRC %X", this.message[1]);
        break;
    }
  }
  else
  {
    output("Unexpected response received.");
  }
}
```

### **Example Output with NRC `0x22`**:
```plaintext
Write Data Request Sent.
Error: Conditions Not Correct (0x22)
```

---

## **Conclusion**

These **realistic Python** and **CAPL** examples demonstrate how to implement the **Write Data By Identifier (0x2E)** service for diagnostic communication with ECUs. They include detailed handling of **positive responses** and **negative response codes (NRCs)**, such as **0x22** (Conditions Not Correct),

 which you would encounter in real-world scenarios.

By leveraging these examples, you can adapt the code to your specific vehicle's ECUs and the associated diagnostic network, ensuring that the Write Data By Identifier service works correctly in various automotive diagnostic situations.