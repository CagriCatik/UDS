---
sidebar_position: 5
---

# Write Data By Identifier - 0x2E

## Introduction

The **Write Data By Identifier (0x2E)** service is an essential diagnostic function defined within the Unified Diagnostic Services (UDS) protocol, as per ISO 14229. This service is used primarily to write or modify data stored in an Electronic Control Unit (ECU) based on a unique identifier. UDS services, such as the **Write Data By Identifier**, facilitate the management of configuration settings, calibration data, software updates, and other parameters that are stored in the ECU’s non-volatile memory.

By allowing targeted data modification, this service ensures that only specified data is written, minimizing the risk of accidental corruption of other parameters or unintended side effects within the ECU. As such, the service plays a crucial role in vehicle diagnostics, repair, and maintenance tasks.

---

## UDS Request and Response Structure

### Request Message Format

The message format for a **Write Data By Identifier (0x2E)** request is as follows:

- **Service ID** (1 byte): The identifier for the service. For this service, the value is always `0x2E`.
- **Data Identifier (DID)** (2 bytes): A unique identifier used to specify the location of the data within the ECU’s memory or configuration.
- **Data to Write** (N bytes): The actual data to be written to the ECU, corresponding to the provided Data Identifier. This can vary in length, depending on the type of data.

#### Example

Consider a scenario where a technician needs to write a new engine calibration value:

```
[0x2E] [0x1234] [0x00000005]
```

Where:
- `0x2E` is the service ID for **Write Data By Identifier**.
- `0x1234` is the **Data Identifier** corresponding to the engine calibration data.
- `0x00000005` is the **new data value** to be written.

This request would instruct the ECU to update its configuration with the new value of `0x00000005` at the memory location identified by `0x1234`.

### Response Message Format

The response message for a **Write Data By Identifier** service consists of the following elements:

- **Service ID** (1 byte): This will match the request’s service ID (`0x2E`).
- **Response Code** (1 byte): The response code indicates the result of the write operation. This could either be a **positive response** or a **negative response** (NRC), with the latter indicating specific errors.

#### Examples of Response Codes

- **Positive Response (0x00)**: The write operation was successful.
- **Negative Response Codes (NRCs)**: If the write operation fails, the ECU will return an appropriate error code. Several NRCs can be returned, depending on the cause of failure.

---

## Negative Response Codes (NRCs)

Negative Response Codes (NRCs) indicate why the write operation could not be completed. Understanding these codes is crucial for diagnosing issues during a **Write Data By Identifier** operation. Below are some of the most common NRCs encountered:

### Common Negative Response Codes (NRCs)

1. **0x11 - Service Not Supported**
   - **Description**: This response indicates that the ECU does not support the requested service, either due to firmware limitations or an unsupported version.
   - **Scenario**: The diagnostic tool sends a request to an ECU that does not have the **Write Data By Identifier** functionality enabled.
   - **Example**: Request:
     ```
     [0x2E] [0x1234] [0x00000005]
     ```
     Response:
     ```
     [0x2E] [0x11]
     ```

2. **0x12 - Subfunction Not Supported**
   - **Description**: This error occurs when the Data Identifier is valid, but the operation for that specific identifier is not supported. For instance, writing to a read-only memory area or a protected configuration would trigger this error.
   - **Scenario**: Attempting to write to a protected memory area or read-only register.
   - **Example**: Request:
     ```
     [0x2E] [0x5678] [0x12345678]
     ```
     Response:
     ```
     [0x2E] [0x12]
     ```

3. **0x21 - General Programming Failure**
   - **Description**: This error signifies a general failure during the write operation, often due to internal ECU issues such as invalid data format, memory corruption, or resource conflicts.
   - **Scenario**: The ECU fails to process the write request due to an internal error such as a checksum failure.
   - **Example**: Request:
     ```
     [0x2E] [0x9876] [0xabcdef01]
     ```
     Response:
     ```
     [0x2E] [0x21]
     ```

4. **0x22 - Conditions Not Correct**
   - **Description**: The operation could not be completed because the ECU is in an inappropriate state. For example, the ECU might need to be in a specific diagnostic session to perform write operations.
   - **Scenario**: Attempting to write to the ECU when it is not in the correct session or has not granted necessary security access.
   - **Example**: Request:
     ```
     [0x2E] [0x1234] [0x00000001]
     ```
     Response:
     ```
     [0x2E] [0x22]
     ```

5. **0x31 - Request Out of Range**
   - **Description**: This response is returned when the data sent in the request exceeds the allowable range for the specified Data Identifier. This can occur if the data size or value is too large for the designated memory space.
   - **Scenario**: Sending data that exceeds the expected size or is otherwise invalid for the Data Identifier.
   - **Example**: Request:
     ```
     [0x2E] [0x5678] [0xabcdef0123456789]
     ```
     Response:
     ```
     [0x2E] [0x31]
     ```

6. **0x33 - Security Access Denied**
   - **Description**: This code indicates that the ECU requires security authentication (password or key) before proceeding with the operation, and the tester has not provided the required credentials.
   - **Scenario**: The diagnostic tool has not completed a security access procedure.
   - **Example**: Request:
     ```
     [0x2E] [0x2345] [0x0001]
     ```
     Response:
     ```
     [0x2E] [0x33]
     ```

7. **0x35 - Request Not Accepted**
   - **Description**: This error code indicates that the ECU is unable to accept the write request due to reasons like memory limitations, system status, or internal constraints.
   - **Scenario**: The ECU is in a locked state, or the requested operation is not feasible due to an internal condition such as resource constraints.
   - **Example**: Request:
     ```
     [0x2E] [0x1234] [0x00000005]
     ```
     Response:
     ```
     [0x2E] [0x35]
     ```

---

## Realistic Examples of Write Data By Identifier

### Example 1: Successful Calibration Write

- **Scenario**: A technician is updating the engine calibration in an ECU as part of a maintenance task.
- **Request**:
  ```
  [0x2E] [0x1234] [0x00000005]
  ```
- **Response**:
  ```
  [0x2E] [0x00]
  ```
- **Explanation**: The ECU successfully updated the calibration data located at `0x1234` with the new value `0x00000005`.

---

### Example 2: Write Denied Due to Incorrect Session

- **Scenario**: The technician attempts to write data, but the ECU is in an incorrect session mode (non-programming session).
- **Request**:
  ```
  [0x2E] [0x1234] [0x00000005]
  ```
- **Response**:
  ```
  [0x2E] [0x22]
  ```
- **Explanation**: The ECU rejected the write operation because it was not in a valid programming session.

---

## Best Practices and Security Considerations

### Session Management

Ensure that the ECU is in the correct diagnostic session before initiating any write operation. For example, the diagnostic session may need to be switched to a programming or special session mode using the **Diagnostic Session Control (0x10)** service.

### Data Validation

Always validate the Data Identifier (DID) and the format of the data being written. The data must conform to the specifications for the given DID, including size and value range. This helps avoid issues such as **Request Out of Range (0x31)** or **Subfunction Not Supported (0x12)** errors.

### Security Access

Some ECUs require security access prior to writing sensitive data such as calibration parameters or software updates. Ensure that the necessary security challenge-response procedure is completed before attempting to write to secured areas. Failure to do so will result in **Security Access Denied (0x33)**.

### Error Handling

Prepare for negative response codes by implementing appropriate error handling and recovery strategies. Diagnostic tools should provide clear feedback to the technician in case of

 an error, including guidance on resolving common issues like session mismatches or unsupported operations.

---

## Conclusion

The **Write Data By Identifier (0x2E)** service is a critical UDS service used to modify ECU data. Understanding the request and response structures, as well as the associated negative response codes, is essential for efficiently using this service in vehicle diagnostics. By adhering to best practices like session management, data validation, and security procedures, technicians can ensure reliable and safe ECU data modification during diagnostics and maintenance.