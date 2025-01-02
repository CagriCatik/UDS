---
sidebar_position: 1
---
# Basic Terms in UDS

## Introduction to UDS

Unified Diagnostic Services (UDS) is a diagnostic communication protocol standardized under ISO 14229. It is used for vehicle diagnostics and enables communication between diagnostic tools (testers) and Electronic Control Units (ECUs) in a vehicle. UDS ensures that different ECUs across various vehicle brands and models can be diagnosed and reprogrammed consistently, providing an efficient and reliable method for troubleshooting, maintenance, and software updates.

### Historical Context
- Old Diagnostics (Pre-UDS): In older vehicles (e.g., from the 1990s and early 2000s), diagnostics were largely manual. A mechanic would perform a visual inspection or use basic tools (like a multimeter) to identify the fault. However, this process was often imprecise because it lacked a method to diagnose specific system-level failures and root causes.
  
- Modern Diagnostics (Post-UDS): In modern vehicles, with the advent of more advanced ECUs (such as Engine Control Units, Airbag Modules, ABS systems, etc.), the need arose for more advanced diagnostics that could not only detect issues but also provide detailed fault codes, real-time data, and the ability to reprogram ECUs. UDS fulfills this need by providing a structured and standardized way to interact with ECUs.

---

## Key Terminologies in UDS

### 1. ECU (Electronic Control Unit)

An ECU is a microcontroller in a vehicle responsible for controlling specific subsystems like engine management, airbags, ABS, etc.

- Server: An ECU that receives diagnostic requests. In UDS, the server (ECU) listens to requests from diagnostic tools (testers) and performs actions based on those requests.
- Client: The diagnostic tool or tester that initiates requests to the ECU.

Example:  
- An Airbag ECU (server) receives a request from a diagnostic scanner (client) to check the airbag system’s status.

### 2. Diagnostic Session

A diagnostic session is an operating state that determines what level of diagnostic functions the ECU supports. UDS defines different sessions, each tailored for specific diagnostic tasks.

- Default Session (0x01): The standard operating session where the ECU functions as it does in everyday use.
- Programming Session (0x02): A special session where the ECU can accept reprogramming commands (e.g., firmware updates).
- Extended Diagnostic Session (0x03): Enables in-depth diagnostics, such as reading and clearing trouble codes (DTCs) or adjusting system parameters.
- Safety System Diagnostic Session (0x04): Used for critical vehicle systems (like airbags or ABS), often requiring additional safety precautions.

Example:  
- A programming session might be initiated when a technician needs to update the engine control software in an ECU.

Request (Diagnostic Session Control):
```hex
0x10 0x02  # Service ID for Diagnostic Session Control, with sub-function 0x02 for Programming Session
```

---

### 3. Request and Response

UDS communication follows a request-response pattern:
- Request: The tester (client) sends a command to the ECU (server) to perform a diagnostic function.
- Positive Response: If the ECU successfully executes the requested service, it sends a positive response.
- Negative Response: If the ECU cannot process the request, it sends a Negative Response Code (NRC).

Example:  
- Request: The tester requests the ECU to read the vehicle's VIN (Vehicle Identification Number).
  - Request Frame:
    ```hex
    0x22 0xF1  # 0x22 is Read Data By Identifier, 0xF1 is the VIN Data Identifier
    ```

- Response: The ECU returns the VIN of the vehicle.
  - Positive Response Frame:
    ```hex
    0x22 0xF1 0x01 0x2B 0x00  # VIN data returned as 0x01 0x2B 0x00
    ```

- Error Response: If the request is malformed, the ECU returns a Negative Response.
  - Negative Response Frame:
    ```hex
    0x7F 0x22 0x13  # Service 0x22, NRC 0x13 (Incorrect Message Length)
    ```

---

### 4. Service Identifier (SID)

Each diagnostic function in UDS has a Service Identifier (SID), which indicates the specific diagnostic action being requested.

- 0x10: Diagnostic Session Control  
- 0x11: ECU Reset  
- 0x22: Read Data by Identifier  
- 0x14: Clear Diagnostic Information (DTCs)  
- 0x27: Security Access (for accessing protected data)  

Example:  
- 0x11 is the SID for ECU Reset service, which allows the tester to reset an ECU.
  
Request (ECU Reset):
```hex
0x11 0x01  # Request to perform a "Hard Reset" of the ECU
```

---

### 5. Sub-functions

Some services in UDS include sub-functions, which refine or specify particular actions within a broader service.

- ECU Reset (0x11) has sub-functions like:
  - 0x01: Hard Reset
  - 0x02: Key-Off-On Reset (simulates turning the ignition off and on)
  - 0x03: Soft Reset (restarts ECU without affecting data)
  
Example:  
- A Hard Reset can be requested by sending the following frame:
  ```hex
  0x11 0x01  # Service 0x11 with sub-function 0x01 for Hard Reset
  ```

---

### 6. Data Identifier (DID)

A Data Identifier (DID) is a unique identifier for specific data within an ECU. It is used to read or write data to or from an ECU.

- Example:  
  - The VIN of the vehicle could have a DID of `0xF1`.
  - A Calibration Value for an ECU could have a DID of `0xF2`.

Example:  
- Request (Read Data by Identifier) to read the VIN:
  ```hex
  0x22 0xF1  # 0x22 is Read Data by Identifier, and 0xF1 is the DID for VIN
  ```

---

### 7. Negative Response Codes (NRC)

NRCs are used to indicate errors or invalid requests. Some common NRCs are:

- 0x12: Sub-function not supported
- 0x13: Incorrect message length
- 0x22: Conditions not correct (e.g., trying to start a session in an unsupported state)
- 0x33: Security access denied (used when security access is required, but not granted)

Example:  
- If the tester requests a service with an incorrect length, the ECU responds with:
  ```hex
  0x7F 0x22 0x13  # Service 0x22 with NRC 0x13 (Incorrect message length)
  ```

---

### 8. Hexadecimal Notation

All UDS communication is encoded in hexadecimal (base 16) format, often prefixed with `0x`.

- Example:  
  - `0x10`: SID for Diagnostic Session Control  
  - `0x22`: SID for Read Data by Identifier  
  - `0xF1`: Data Identifier for VIN  

Each byte is represented by two hexadecimal characters (e.g., `0x01`, `0x7F`).

---

### 9. Valid and Invalid Requests

UDS defines both valid and invalid requests:
- Valid Requests: Properly formatted requests that conform to the UDS protocol.
- Invalid Requests: Requests that are malformed or unsupported by the ECU.

Example:
- A valid request for reading data by identifier might look like this:
  ```hex
  0x22 0xF1  # Valid request to read the VIN (Data Identifier 0xF1)
  ```

- An invalid request for the same service might look like this:
  ```hex
  0x22 0x00  # Invalid request (0x00 is an unsupported DID)
  ```

---

## UDS Communication Workflow

1. Session Initiation: The tester requests a specific session (e.g., Default or Extended).
   - Request: `0x10 0x02` (Request to switch to a Programming Session)
   
2. Service Request: Once the session is active, the tester can request various diagnostic services (e.g., read data, clear DTCs, etc.).
   - Request: `0x22 0xF1` (Request to read the VIN)

3. Error Handling: If the ECU cannot process the request, it responds with an NRC indicating the error type.
   - Response: `0x7F 0x22 0x13` (Incorrect message length)

4. Session Termination: After

 the diagnostic operations, the session may end, and the ECU returns to the default state.
   - Request: `0x11` (Request for ECU Reset)

---

## Applications of UDS

### 1. Diagnostics
- Reading DTCs: Diagnostic Trouble Codes that indicate system failures.
- Real-time Data: Reading live data from sensors, like engine temperature, throttle position, etc.

### 2. Flashing
- ECU Reprogramming: UDS is often used to flash ECUs with new firmware or software versions, critical for software updates or fixes.

### 3. Control Functions
- Parameter Adjustment: UDS allows for adjusting parameters such as calibration values, sensor thresholds, etc., to optimize system performance.

---

## Conclusion

Understanding the basic terms in UDS is essential for working with modern vehicle diagnostic tools and ECUs. With hexadecimal encoding, service identifiers, and data identifiers, UDS allows precise and effective communication between diagnostic equipment and ECUs. By following the structured format of requests, responses, and error codes, UDS ensures reliable and consistent diagnostics and maintenance.