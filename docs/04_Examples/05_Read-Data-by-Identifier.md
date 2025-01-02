---
sidebar_position: 5
---

# Examples - 0x22 


Below are practical examples of how to implement the **Read Data By Identifier (0x22)** service, based on the UDS protocol (ISO 14229). These examples will include code snippets to simulate the service request and response using different tools, including Python and CAPL.

---

## 1. **Python Example: Using `python-uds` Library**

We will use the `python-uds` library, an open-source Python package that allows you to send and receive UDS messages. The example demonstrates how to send a **Read Data By Identifier** request to an ECU and interpret the response.

### 1.1. Install the `python-uds` Library

First, install the `python-uds` library:

```bash
pip install python-uds
```

### 1.2. Python Code to Read Data by Identifier

In this example, we’ll use the `python-uds` library to send a **Read Data By Identifier (0x22)** request for the ECU software version (identifier `0x01`) and retrieve the response.

```python
import uds
from uds.enums import Services
from uds.services import ReadDataByIdentifier
from uds.datatypes import Address
import time

# Define the ECU address (example CAN address)
ecu_address = Address("0x7E0")  # Common address for ECU on CAN bus

# Create a UDS transport object (CAN transport in this case)
# The `uds` library supports CAN and other transports; configure accordingly
transport = uds.transport.can.CANTransport(channel="can0", address=ecu_address)

# Define the identifier for Software Version (example: 0x01)
data_identifier = [0x01]

# Create a ReadDataByIdentifier service request
service_request = ReadDataByIdentifier(data_identifier)

# Send the request and receive the response
response = transport.request(service_request)

# Print the response data (Software version, for example)
print("Received Response:")
print(response)

# Example of interpreting the response
# Assuming the response is: 0x62 0x01 0x01 0x00 0x02 0x03 (Software version: 1.0.2.3)
if response.service_id == 0x62:
    version_data = response.data[2:]  # Skip the identifier byte
    software_version = ".".join([str(byte) for byte in version_data])
    print(f"Software Version: {software_version}")
else:
    print("Error: Invalid response")
```

## Key Points:
- **CAN Address**: `0x7E0` is typically the address for the ECU in a CAN network.
- **Transport Layer**: In this case, we're using **CAN** as the transport layer.
- **Request**: We're sending a **Read Data By Identifier** request to retrieve the ECU's software version using identifier `0x01`.
- **Response**: The response is parsed to extract and display the software version (for example: `1.0.2.3`).

---

## 2. **CAPL Example: Simulating RDBI Request**

In **CAPL** (CAN Application Protocol Language), which is used in **Vector CANoe** and **CANalyzer**, you can implement UDS services directly for CAN simulation and testing.

### 2.1. CAPL Code to Read Data by Identifier (0x22)

This example demonstrates how to implement a **Read Data By Identifier** request for the software version (identifier `0x01`).

```CAPL
variables
{
  msTimer timeoutTimer;  // Timer for response timeout
}

on start
{
  // Send a Read Data By Identifier (0x22) request for the Software Version (identifier 0x01)
  output("Sending RDBI request for Software Version (0x01)...");

  // Send UDS request on the CAN bus
  byte request[8] = {0x22, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};  // 0x22 = RDBI, 0x01 = identifier for software version
  output("Request: %x %x", request[0], request[1]);
  output(request);

  // Send message via CAN interface (assume CAN channel is configured)
  outputMessage(0x7E0, request, 8);  // Assuming 0x7E0 is the ECU address

  // Start timer for response timeout
  setTimer(timeoutTimer, 1000);  // 1-second timeout
}

on message 0x7E8  // Assuming ECU responds on CAN address 0x7E8
{
  byte response[8];
  response = thisByte;

  // Check the response service ID (should be 0x62 for successful response)
  if (response[0] == 0x62) {
    output("Received valid response for RDBI!");
    output("Software Version: %x.%x.%x.%x", response[2], response[3], response[4], response[5]);
  } else {
    output("Error: Invalid response received.");
  }
}

on timer timeoutTimer
{
  output("Error: Response timeout!");
}
```

## Key Points:
- **Service ID**: We send `0x22` for the **Read Data By Identifier** service and `0x01` for the software version identifier.
- **CAN Message**: The message is sent to address `0x7E0` (ECU address) and waits for the response from `0x7E8` (ECU response address).
- **Response Handling**: When the ECU responds with a message starting with `0x62`, we interpret the response to extract and print the software version (e.g., `1.0.2.3`).

---

## 3. **Simulating UDS RDBI Request Using CANoe** (Vector CANoe Simulation)

If you use **Vector CANoe** for UDS simulation, you can implement the **Read Data By Identifier** service in a similar way to the CAPL example. In CANoe, you will use the **CAPL script** to send the request and receive the response. The configuration will include setting up the ECU simulation to respond with specific identifiers for testing.

### 3.1. Setting Up the CANoe Simulation

- **ECU Simulator**: Set up an ECU in CANoe to respond to UDS requests, including the `0x22` service.
- **Database**: Use **DBC** files to define the CAN messages and signal mappings.

### 3.2. Example CANoe Simulation Setup

1. **Message Configuration**: Define the CAN message for the `0x22` request and its response.
2. **CAPL Script**: Implement CAPL script to send the request and handle the response, as shown in the previous CAPL example.

This example will ensure that the UDS **Read Data By Identifier** service is successfully simulated and tested using Vector CANoe.

---

## 4. **Example: Testing Vehicle Speed (0x02)**

### 4.1. Python Example: Request Vehicle Speed (Identifier `0x02`)

Let’s send a request to retrieve the **vehicle speed** using identifier `0x02`:

```python
import uds
from uds.enums import Services
from uds.services import ReadDataByIdentifier
from uds.datatypes import Address

# Define ECU address
ecu_address = Address("0x7E0")  # CAN address of the ECU

# Define transport layer (CAN transport in this example)
transport = uds.transport.can.CANTransport(channel="can0", address=ecu_address)

# Define vehicle speed identifier (0x02)
data_identifier = [0x02]

# Create a ReadDataByIdentifier request for vehicle speed
service_request = ReadDataByIdentifier(data_identifier)

# Send the request and get the response
response = transport.request(service_request)

# Process and print response
print("Received Response:")
print(response)

# Example: Interpret vehicle speed response
if response.service_id == 0x62:
    vehicle_speed = int.from_bytes(response.data[2:], byteorder="big")  # Get speed (bytes 2 and 3)
    print(f"Vehicle Speed: {vehicle_speed} km/h")
else:
    print("Error: Invalid response")
```

## 4.2. CAPL Example: Request Vehicle Speed (Identifier `0x02`)

```CAPL
on start
{
  byte request[8] = {0x22, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};  // 0x22 = RDBI, 0x02 = Vehicle Speed
  output("Sending RDBI request for Vehicle Speed (0x02)...");

  // Send UDS message on CAN bus
  outputMessage(0x7E0, request, 8);  // CAN address of ECU: 0x7E0

  // Set timeout timer
  setTimer(timeoutTimer, 1000);  // 1 second timeout
}

on message 0x7E8  // Assuming the ECU responds on address 0x7E8
{
  byte response[8];
  response = thisByte;

  // Handle the response
  if (response[0] == 0x62) {
    output("Received valid response for RDBI.");
    output("Vehicle Speed: %x", response[2] * 256 + response[

3]);  // Speed value in km/h
  } else {
    output("Error: Invalid response");
  }
}
```

---

## 5. **Conclusion**

These examples show how to implement and simulate the **Read Data By Identifier (0x22)** service using Python and CAPL. By using tools like `python-uds`, **Vector CANoe**, and **CAPL scripts**, you can simulate diagnostic interactions with ECUs, retrieve vehicle data (e.g., software version, vehicle speed), and integrate the service into vehicle testing and diagnostics workflows.

By following these examples, you should be able to implement UDS requests for various data identifiers in both real-world and simulated environments, and handle responses in an automated and robust manner.