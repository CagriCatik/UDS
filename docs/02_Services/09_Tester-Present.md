---
sidebar_position: 9
---

# Tester Present Service - 0x03

## Introduction

The **Tester Present** service is a fundamental diagnostic service defined in the **Unified Diagnostic Services (UDS)** protocol, standardized under **ISO 14229**. UDS is extensively utilized in the automotive industry for **ECU (Electronic Control Unit)** diagnostics, enabling communication between diagnostic testers (tools) and vehicle ECUs. The Tester Present service, identified by **Service ID 0x03**, plays a critical role in maintaining active and stable communication sessions between the tester and the ECU, especially during complex diagnostic operations.

### Key Points:
- **Service ID**: 0x03 (Tester Present)
- **Standard**: ISO 14229 (UDS)
- **Primary Purpose**: Maintain ECU in a non-default diagnostic session.
- **Common Use Cases**: Programming, routine control, calibration, and extended diagnostic operations.

## Purpose of the Tester Present Service

The primary purpose of the **Tester Present** service is to ensure that the ECU remains in a **non-default diagnostic session**, such as an **extended session** or a **programming session**. These non-default sessions provide access to advanced diagnostic and control functionalities that are not available in the **default session**. Without periodic Tester Present requests, the ECU may automatically revert to the default session after a predefined timeout, disrupting ongoing diagnostic procedures.

### Objectives:
- **Session Maintenance**: Keeps the ECU in an active non-default session.
- **Communication Assurance**: Confirms the continued presence of the tester to prevent session timeout.
- **Operational Stability**: Ensures uninterrupted execution of complex diagnostic tasks.

### Use Case Scenario:
During a firmware update or calibration of a vehicle component, the ECU must remain in an extended session to accept programming commands. The Tester Present service sends periodic signals to the ECU to affirm that the diagnostic tester is still engaged, preventing the ECU from timing out and reverting to the default session, which would abort the update process.

## UDS Diagnostic Sessions Overview

Understanding the Tester Present service requires familiarity with the various **Diagnostic Sessions** defined in UDS. Diagnostic sessions determine the level of access and functionalities available for diagnostic operations.

### Common Diagnostic Sessions:
1. **Default Session (0x01)**:
   - **Description**: The initial session upon ECU startup or reset.
   - **Capabilities**: Basic diagnostic functions such as reading fault codes.
   - **Timeout**: Typically short, requiring periodic Tester Present requests to maintain or transition to another session.

2. **Programming Session (0x02)**:
   - **Description**: Allows reprogramming of the ECU firmware.
   - **Capabilities**: Access to memory writing, firmware upload/download.
   - **Security**: Often requires authentication via the **Security Access** service before entry.

3. **Extended Diagnostic Session (0x03)**:
   - **Description**: Provides extended diagnostic functionalities.
   - **Capabilities**: Advanced diagnostic services, including complex data manipulation and extended routine controls.
   - **Usage**: Often used during in-depth vehicle diagnostics and component testing.

4. **Safety System Diagnostic Session (0x04)**:
   - **Description**: Reserved for safety-critical diagnostics.
   - **Capabilities**: High-security operations, often related to vehicle safety systems.

### Transitioning Between Sessions:
- **Session Control**: Managed using the **Diagnostic Session Control** service (**Service ID 0x10**), which initiates a transition to the desired session.
- **Role of Tester Present**: Once in a non-default session, the Tester Present service ensures the session remains active by preventing timeout-induced reversion to the default session.

## Tester Present Service Details

### Service Identification:
- **Service ID**: `0x03`
- **Description**: Maintains the ECU in a non-default diagnostic session by signaling the tester's continued presence.

### Sub-functions:
1. **0x00**: Tester Present without suppressing the positive response.
2. **0x80**: Tester Present with suppression of the positive response.

### Detailed Functionality:

#### Sub-function 0x00: Tester Present with Positive Response
- **Purpose**: Sends a Tester Present request and expects a positive acknowledgment from the ECU.
- **Operation**:
  - **Tester Action**: Sends a Tester Present request with sub-function `0x00`.
  - **ECU Response**: Returns a positive response echoing the Service ID and sub-function.
- **Use Case**: Standard maintenance of the diagnostic session where acknowledgment of each request is necessary for logging or verification purposes.

#### Sub-function 0x80: Tester Present with Suppressed Response
- **Purpose**: Sends a Tester Present request without expecting any response from the ECU.
- **Operation**:
  - **Tester Action**: Sends a Tester Present request with sub-function `0x80`.
  - **ECU Response**: Suppresses the positive response, sending no acknowledgment.
- **Use Case**: Reduces network traffic and processing overhead when frequent Tester Present messages are required, such as during lengthy programming sessions.

### Request and Response Frame Structures

#### Request Frame:
- **Service ID**: `0x03`
- **Sub-function**: `0x00` or `0x80`
- **Data Parameters**: None

**Example**:
```
| Service ID (1 byte) | Sub-function (1 byte) |
|---------------------|-----------------------|
|        0x03         |         0x00          |
```

#### Positive Response Frame (for Sub-function 0x00):
- **Service ID**: `0x43` (Service ID + 0x40)
- **Sub-function**: Echoed sub-function `0x00`
- **Data**: None

**Example**:
```
| Response ID (1 byte) | Sub-function (1 byte) |
|----------------------|-----------------------|
|        0x43          |         0x00          |
```

#### No Response (for Sub-function 0x80):
- **Operation**: No response frame is sent by the ECU.

### Negative Response Handling

If the **Tester Present** request is malformed or uses an unsupported sub-function, the ECU may respond with a **Negative Response Code (NRC)**. Common NRCs include:

- **0x11**: **Service Not Supported** – The ECU does not support the Tester Present service.
- **0x22**: **Incorrect Message Length** – The request does not conform to the expected format.
- **0x33**: **Response Pending** – The ECU is busy and cannot process the request immediately.

**Negative Response Frame Structure**:
```
| Negative Response ID (1 byte) | Original Service ID + 0x40 (1 byte) | NRC (1 byte) |
|--------------------------------|---------------------------------------|--------------|
|             0x7F               |                0x43                   |    0x22      |
```

### Timing Considerations

- **Request Interval**: Tester Present requests must be sent at intervals shorter than the ECU's session timeout period, typically specified in the ECU's diagnostic settings or communicated during session control.
- **Session Timeout**: If the Tester Present requests are not received within the timeout period, the ECU may revert to the default session automatically.

### Best Practices:
- **Consistent Timing**: Ensure that Tester Present requests are sent consistently and within the required intervals to maintain session integrity.
- **Error Handling**: Implement robust error handling to manage negative responses and re-establish sessions if necessary.
- **Resource Management**: Use Sub-function `0x80` when possible to minimize unnecessary network traffic and ECU processing load during high-frequency Tester Present messaging.

## Service Call and Communication Flow

### Activation of Tester Present Service

1. **Initiate Non-Default Session**:
   - The tester sends a **Diagnostic Session Control** request (`0x10`) to transition the ECU into a non-default session (e.g., extended or programming session).
   
2. **Maintain Session**:
   - Once in the non-default session, the tester must periodically send **Tester Present** requests (`0x03`) to maintain the session.

### Communication Sequence:

#### Example: Maintaining an Extended Diagnostic Session

1. **Enter Extended Session**:
   - **Request**:
     ```
     | Service ID | Sub-function |
     |-----------|--------------|
     |   0x10    |     0x03     |
     ```
   - **Positive Response**:
     ```
     | Response ID | Sub-function |
     |-------------|--------------|
     |    0x50     |     0x03     |
     ```

2. **Send Tester Present Request**:
   - **Request**:
     ```
     | Service ID | Sub-function |
     |-----------|--------------|
     |   0x03    |     0x00     |
     ```
   - **Positive Response**:
     ```
     | Response ID | Sub-function |
     |-------------|--------------|
     |    0x43     |     0x00     |
     ```

3. **Continue Periodic Tester Present Requests**:
   - **Request** (Suppressed Response):
     ```
     | Service ID | Sub-function |
     |-----------|--------------|
     |   0x03    |     0x80     |
     ```
   - **Response**:
     - No response sent by the ECU.

4. **Complete Diagnostic Operations**:
   - Perform necessary diagnostic or programming tasks while maintaining the session with periodic Tester Present requests.

### Communication Flow Diagram

```
Tester                        ECU
  |                             |
  |---- Diagnostic Session Control (0x10) ---->|
  |                             |
  |<--- Positive Response (0x50) -------------|
  |                             |
  |---- Tester Present (0x03, 0x00) ---------->|
  |                             |
  |<--- Positive Response (0x43, 0x00) --------|
  |                             |
  |---- Tester Present (0x03, 0x80) ---------->|
  |                             |
  |<--- No Response ----------------------------|
  |                             |
  |          ... Continued ...                |
```

## Handling Diagnostic Sessions

### Default Session (0x01)
- **Characteristics**:
  - Initial session upon ECU power-up or reset.
  - Limited diagnostic capabilities.
  - Does not require Tester Present messages to maintain.
- **Typical Operations**:
  - Reading basic diagnostic trouble codes (DTCs).
  - Retrieving ECU status information.

### Non-Default Sessions (e.g., Extended Session 0x03, Programming Session 0x02)
- **Characteristics**:
  - Provide access to advanced diagnostic services.
  - Require periodic Tester Present messages to prevent session timeout.
- **Maintenance**:
  - **Periodic Tester Present Requests**: Sent at intervals shorter than the ECU's session timeout.
  - **Sub-function Selection**: Use `0x00` for acknowledgment or `0x80` to suppress responses based on operational needs.

### Transitioning Between Sessions

1. **Exit Current Session**:
   - To transition back to the default session, send a **Diagnostic Session Control** request with Service ID `0x10` and sub-function `0x01`.
   
2. **Handle Session Termination**:
   - Upon session termination, the ECU ceases to require Tester Present messages, and the tester can switch to default session operations.

## Typical Usage of Tester Present

### Scenario 1: Routine Control Operation

**Context**: Adjusting calibration values or configuring a vehicle component requires the ECU to remain in an extended diagnostic session.

**Steps**:
1. **Enter Extended Session**: Send Diagnostic Session Control (`0x10` with sub-function `0x03`).
2. **Maintain Session**: Periodically send Tester Present (`0x03` with sub-function `0x00`).
3. **Perform Routine Control**: Execute calibration or configuration commands.
4. **End Operation**: Optionally, revert to default session if necessary.

### Scenario 2: Programming ECU Firmware

**Context**: Updating the ECU firmware necessitates a stable programming session to prevent interruptions.

**Steps**:
1. **Enter Programming Session**: Send Diagnostic Session Control (`0x10` with sub-function `0x02`).
2. **Authenticate**: Complete any required security access procedures.
3. **Maintain Session**: Send Tester Present (`0x03` with sub-function `0x80`) to reduce network traffic.
4. **Upload Firmware**: Transmit the firmware data to the ECU.
5. **Verify and Complete**: Confirm successful programming and optionally return to default session.

### Scenario 3: Preventing Session Timeout

**Context**: Prolonged diagnostic operations, such as security access or extensive routine controls, risk session timeout.

**Steps**:
1. **Enter Non-Default Session**: Initiate the required diagnostic session.
2. **Maintain Session**: Continuously send Tester Present (`0x03` with appropriate sub-function) within the ECU's timeout period.
3. **Execute Operations**: Perform the necessary extended diagnostic tasks without interruption.
4. **Conclude Session**: Optionally revert to the default session after completing operations.

## Real-Time Example: Wiper Motor Calibration

**Scenario**: Recalibrating a wiper motor due to a timer mismatch requires maintaining the ECU in an extended session to ensure uninterrupted execution of the calibration routine.

### Step-by-Step Process:

1. **Initiate Extended Session**:
   - **Request**:
     ```
     | Service ID | Sub-function |
     |-----------|--------------|
     |   0x10    |     0x03     |
     ```
   - **ECU Response**:
     ```
     | Response ID | Sub-function |
     |-------------|--------------|
     |    0x50     |     0x03     |
     ```

2. **Start Tester Present Requests**:
   - **Initial Request**:
     ```
     | Service ID | Sub-function |
     |-----------|--------------|
     |   0x03    |     0x00     |
     ```
   - **ECU Response**:
     ```
     | Response ID | Sub-function |
     |-------------|--------------|
     |    0x43     |     0x00     |
     ```

3. **Continue Periodic Tester Present Requests**:
   - **Subsequent Requests** (using Sub-function `0x80` to minimize responses):
     ```
     | Service ID | Sub-function |
     |-----------|--------------|
     |   0x03    |     0x80     |
     ```
   - **ECU Response**:
     - No response sent.

4. **Execute Wiper Motor Calibration Routine**:
   - **Perform Calibration**: Send specific routine control commands to recalibrate the wiper motor.
   - **Monitor Progress**: Ensure calibration commands are acknowledged and completed successfully.

5. **Maintain Session Throughout Calibration**:
   - **Continue Sending Tester Present Requests** at defined intervals to prevent session timeout.

6. **Complete Calibration and Terminate Session**:
   - **End Calibration**: Confirm successful calibration.
   - **Exit Extended Session** (optional):
     ```
     | Service ID | Sub-function |
     |-----------|--------------|
     |   0x10    |     0x01     |
     ```
   - **ECU Response**:
     ```
     | Response ID | Sub-function |
     |-------------|--------------|
     |    0x50     |     0x01     |
     ```

### Summary:
By utilizing the Tester Present service, the diagnostic tester ensures that the ECU remains in the extended session throughout the wiper motor calibration process, preventing unintended session termination and ensuring the calibration is executed without interruption.

## Security Considerations

While the Tester Present service is essential for maintaining diagnostic sessions, it can also be exploited if not properly secured. Unauthorized access to the Tester Present service could potentially prevent legitimate ECU operations or maintain unauthorized sessions.

### Security Best Practices:
- **Authentication**: Require authentication via the **Security Access** service before allowing non-default sessions.
- **Session Management**: Implement robust session timeout mechanisms to minimize the risk of unauthorized prolonged sessions.
- **Access Control**: Restrict the Tester Present service to authenticated and authorized diagnostic testers.
- **Monitoring**: Log and monitor Tester Present requests to detect and respond to suspicious activities.

## Comparison with Similar UDS Services

### Diagnostic Session Control (0x10)
- **Purpose**: Initiates or terminates diagnostic sessions.
- **Relation to Tester Present**: Tester Present is used to maintain sessions initiated by Diagnostic Session Control.

### Communication Control (0x28)
- **Purpose**: Manages communication parameters, such as enabling or disabling specific communication channels.
- **Relation to Tester Present**: While Communication Control manages communication parameters, Tester Present ensures the continuity of the diagnostic session over those communication channels.

### Security Access (0x27)
- **Purpose**: Provides authentication mechanisms to access secured diagnostic services.
- **Relation to Tester Present**: Security Access is often a prerequisite for entering non-default sessions that require the use of Tester Present.

## Conclusion

The **Tester Present** service is an indispensable component of the UDS protocol, ensuring the stability and continuity of non-default diagnostic sessions essential for advanced ECU operations. By periodically signaling the ECU's continued engagement, Tester Present prevents unintended session timeouts, facilitating uninterrupted diagnostic activities such as programming, calibration, and routine controls.
