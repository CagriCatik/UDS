---
sidebar_position: 8
---

# Examples - 0x28

Below are examples of how you can implement Communication Control (0x28) in Python and CAPL. These examples demonstrate how you might use both languages to request and handle UDS communication control for enabling/disabling reception and transmission.

## 1. Python Implementation for Communication Control (0x28)

To implement a UDS communication control request in Python, you can use libraries like `python-can` for CAN communication, `uds` (a Python UDS library), or `python-uds`. In this example, we'll use the `python-uds` library (which needs to be installed) to create a simple communication control request.

Installation of Required Libraries:
First, install the `python-uds` library (if not installed already):
```bash
pip install python-uds
```

Python Code for Communication Control Request:

```python
import uds
import can
import time

# Create a CAN bus instance (using a virtual CAN bus for demonstration)
bus = can.interface.Bus(bustype='virtual', channel='vcan0', bitrate=500000)

# Define UDS Communication Control (0x28) Request with Enable Rx & Tx (0x00)
def send_communication_control_request():
    # Create the UDS request frame
    request_frame = uds.Request(0x28)  # 0x28 is the service ID for Communication Control
    request_frame.add_data(0x00)  # Sub-function: 0x00 (Enable Rx & Tx)
    request_frame.add_data(0x01)  # Communication Type: CAN
    request_frame.add_data(0x01)  # Node Id (ECU 1)

    # Send the UDS request
    print("Sending Communication Control Request: Enable Rx & Tx")
    bus.send(can.Message(arbitration_id=0x7DF, data=request_frame.get_data(), is_extended_id=False))

    # Wait for response (5 seconds timeout)
    start_time = time.time()
    while time.time() - start_time < 5:
        message = bus.recv()
        if message:
            # Parse the response
            if message.arbitration_id == 0x7E8:  # Assuming ECU responds with ID 0x7E8
                response = uds.Response(message.data)
                print(f"Received Response: {response.data}")
                break
    else:
        print("No response received within the timeout.")

# Call the function to send the request
send_communication_control_request()
```

Explanation:
- The code creates a UDS request for Communication Control (0x28) with Enable Rx & Tx (0x00).
- We use the `python-can` library to send the request over a virtual CAN bus (`vcan0`).
- The `uds` library is used to generate the UDS request frame with the necessary sub-function and communication type.

---

## 2. CAPL Script for Communication Control (0x28)

CAPL (CAN Application Programming Language) is typically used for testing ECUs and can be executed in environments like CANoe or CANalyzer. Below is an example CAPL script for requesting the Communication Control (0x28) service with the sub-function Enable Rx & Tx (0x00).

CAPL Script for Communication Control Request:

```capl
variables
{
  msTimer timeoutTimer;
}

on start
{
  // Initialize timer for response timeout
  setTimer(timeoutTimer, 5000);  // 5 seconds timeout
}

on message 0x7DF  // CAN request message (0x7DF is the standard UDS request address)
{
  // Check if the request is for Communication Control service (0x28)
  if (this.byte(0) == 0x28) {
    byte subFunction = this.byte(1); // Get the sub-function from the request (index 1)
    
    if (subFunction == 0x00) { // Enable Rx & Tx
      output("Received UDS Communication Control Request: Enable Rx & Tx");

      // Create the response message
      byte response[8];
      response[0] = 0x28;  // Service Id (Communication Control)
      response[1] = 0x00;  // Sub-function (Enable Rx & Tx)

      // Send the response to the ECU
      output("Sending Response: Enable Rx & Tx");
      sendMessage(0x7E8, response, 2);  // Respond with ID 0x7E8 (ECU response address)
    }
  }
}

on timer timeoutTimer
{
  // If no response is received within the timeout
  output("No response received within the timeout.");
}

```

Explanation:
- The script listens for a UDS Communication Control service (0x28) request sent by the tester on CAN ID `0x7DF` (UDS standard address).
- When it detects a request for Enable Rx & Tx (0x00), the ECU responds with a confirmation message containing the same service ID and sub-function.
- If no response is received within the set timeout (5 seconds), the script outputs a timeout message.

---

## 3. Testing and Running the Scripts

### Testing the Python Script:
1. Set Up a Virtual CAN Network:
   Before running the Python script, you need to set up a virtual CAN network. On Linux, you can do this by running:
   ```bash
   sudo modprobe vcan
   sudo ip link add dev vcan0 type vcan bitrate 500000
   sudo ip link set up vcan0
   ```

2. Run the Python Script:
   Make sure that your Python environment has the required libraries (`python-uds` and `python-can`). Then, run the script:
   ```bash
   python3 uds_comm_control.py
   ```

3. Test and Verify:
   - If everything is set up correctly, the script will send a request to enable communication and will wait for a response from the ECU (simulated here via a CAN bus).
   - The response will be printed out if it is received within the timeout period.

### Testing the CAPL Script:
1. Open CANoe or CANalyzer and create a new configuration that includes a CAN bus with the required message IDs.
2. Paste the CAPL Script into the CANoe or CANalyzer scripting environment.
3. Run the simulation.
   - The script will trigger when a CAN message with the ID `0x7DF` (UDS request) is received.
   - The response will be sent from the ECU (simulated by the script) on CAN ID `0x7E8`.

---

## 4. Conclusion

Both Python and CAPL provide robust environments for testing and simulating UDS communication control. These examples show how you can use Python for creating UDS communication requests and handle responses, as well as how you can use CAPL in CANoe or CANalyzer to simulate the ECU's response to communication control requests.

- The Python example uses the `python-can` and `python-uds` libraries to send and receive UDS requests over a virtual CAN network.
- The CAPL example demonstrates how to implement a simple response in an ECU simulation environment, like CANoe or CANalyzer.

Both implementations help automate and verify the UDS communication control functionality, which is critical for diagnostic and testing environments.