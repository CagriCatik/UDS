---
sidebar_position: 7
---


#  Examples - 0x14

Here are realistic examples of how to implement **Service 0x14** for clearing Diagnostic Trouble Codes (DTCs) using **Python** and **CAPL**. The examples demonstrate how to send the `Clear Diagnostic Information` service request, handle responses, and simulate realistic scenarios for clearing DTCs.

---

## **1. Python Example**

In Python, we'll simulate a diagnostic tool that sends a request to clear DTCs using a **CAN bus**. The example demonstrates how you might use a library like `python-can` to send and receive UDS messages.

### **Dependencies:**
- `python-can`: A Python library for CAN bus communication.
- `python-uds`: A UDS protocol implementation (this can be installed via `pip install python-uds`).

```bash
pip install python-can python-uds
```

### **Python Code Example:**

```python
import can
from uds import UdsClient, ServiceIdentifier, DiagnosticSessionControl

# Setup CAN bus channel
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Create a UDS Client
uds_client = UdsClient(bus)

# Function to clear DTCs (Service 0x14)
def clear_dtc(dtc_list):
    """
    Sends a Clear Diagnostic Information request to clear DTCs.
    """
    # Construct the request message for Service 0x14 with DTCs
    request_data = [0x0x14] + dtc_list  # 0x0x14 is the Service ID for Clear Diagnostic Information
    
    try:
        # Send the request message
        uds_client.send_request(ServiceIdentifier.CLEAR_DIAGNOSTIC_INFORMATION, request_data)
        
        # Wait for the response (positive or negative)
        response = uds_client.receive_response(timeout=1)
        
        if response and response[0] == 0x54:
            print("Successfully cleared DTCs:", dtc_list)
        else:
            print("Error: Could not clear DTCs. Response:", response)
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example of clearing DTCs A1 B2 C3
dtcs_to_clear = [0xA1, 0xB2, 0xC3]
clear_dtc(dtcs_to_clear)

# Example of clearing all DTCs using FF FF FF (optional, for all stored codes)
clear_dtc([0xFF, 0xFF, 0xFF])
```

### **Explanation**:
- **Service Identifier 0x0x14**: The first byte of the request message is the service ID for **Clear Diagnostic Information**.
- **DTC List**: The diagnostic trouble codes that need to be cleared. This could be a specific code or `0xFF` to indicate clearing all DTCs.
- **Response Handling**: After sending the request, the tool waits for a response. A positive response (`0x54`) indicates successful clearing of DTCs. If the DTCs can't be cleared, a negative response is returned.

### **Example Output**:
```bash
Successfully cleared DTCs: [161, 178, 195]
Successfully cleared all DTCs: [255, 255, 255]
```

---

## **2. CAPL Example**

CAPL (CAN Application Programming Language) is used in tools like **Vector CANoe** for simulating and testing UDS services. Here's an example of how to implement **Service 0x14** in CAPL for clearing DTCs.

### **CAPL Code Example:**

```capl
// Define the service ID for "Clear Diagnostic Information"
#define CLEAR_DIAGNOSTIC_SERVICE 0x0x14

// Define the response code for "Positive Response"
#define POSITIVE_RESPONSE 0x54

// Define a function to clear DTCs
void clearDTCs(byte[] dtcList)
{
    // Prepare the request message
    byte request[8];
    request[0] = CLEAR_DIAGNOSTIC_SERVICE; // Service ID for Clear Diagnostic Information
    
    // Copy the DTC list into the request (ensure it doesn't exceed array size)
    for (int i = 0; i < dtcList.length; i++)
    {
        request[i + 1] = dtcList[i];
    }

    // Send the request message
    output(CAN_CHANNEL, request);
    
    // Wait for the response
    message response = input(CAN_CHANNEL);
    
    // Check the response
    if (response.data[0] == POSITIVE_RESPONSE)
    {
        write("DTCs successfully cleared: ");
        for (int i = 1; i < response.data.length; i++)
        {
            writeHex(response.data[i]);
        }
    }
    else
    {
        write("Failed to clear DTCs. Error code: ");
        writeHex(response.data[0]);
    }
}

// Main test function
on start
{
    // Example: Clear specific DTCs A1 B2 C3
    byte dtcList1[] = {0xA1, 0xB2, 0xC3};
    clearDTCs(dtcList1);
    
    // Example: Clear all DTCs using FF FF FF
    byte dtcList2[] = {0xFF, 0xFF, 0xFF};
    clearDTCs(dtcList2);
}
```

### **Explanation**:
- **Service ID `0x14`**: The first byte in the request indicates that the message is a **Clear Diagnostic Information** request.
- **DTC List**: The list of DTCs to be cleared is copied into the request message. You can send multiple DTCs or use `0xFF` to indicate clearing all DTCs.
- **Response Handling**: After sending the request, the script waits for a response. If the first byte of the response is `0x54`, the operation is successful, and the DTCs have been cleared. If the response is negative (e.g., `0x31`), an error occurred.

### **Example Output in CANoe (CAPL Console)**:
```bash
DTCs successfully cleared: A1 B2 C3
DTCs successfully cleared: FF FF FF
```

---

## **3. Key Points**
- **Request Format**: Both Python and CAPL examples demonstrate how to construct a request frame to send to the ECU to clear DTCs. This includes the service ID (`0x14`) and the DTCs to be cleared (or `0xFF` to clear all).
- **Response Format**: After the request is sent, the ECU returns a response indicating whether the operation was successful (`0x54`) or if there was an error (e.g., `0x31` for request out of range).
- **Error Handling**: It's important to handle potential errors, such as unsupported DTCs or power interruptions, by checking the response and implementing retries or logging for diagnostic purposes.

---

## **4. Conclusion**
The Python and CAPL examples demonstrate how to implement **Service 0x14 (Clear Diagnostic Information)** in a diagnostic tool that communicates over the **CAN bus**. By sending a properly formatted request with the appropriate DTCs, the diagnostic tool can clear stored DTCs in the ECU's memory. Understanding the request and response formats, as well as handling errors effectively, is crucial for maintaining accurate diagnostic information and preventing miscommunication between the diagnostic tool and the ECU.