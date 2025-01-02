---
sidebar_position: 8
---

# Write Memory by Address - 0x3D

## Overview

The *Write Memory by Address* service (SID 0x3D) in Unified Diagnostic Services (UDS) allows a diagnostic tool (client) to write or modify specific regions of memory within an ECU (Electronic Control Unit). This service is often used for tasks such as updating calibration data, modifying ECU configurations, or clearing non-volatile memory.

### Service ID
- **Request SID**: 0x3D
- **Response SID**: 0x7D

### Purpose
This service allows the client to write data to a specific memory location in the ECU. It can be used to modify calibrating values, overwrite configuration data, or clear specific areas in non-volatile memory.

## Frame Format

The *Write Memory by Address* service is structured in both request and response frames. The format is as follows:

### Request Frame

The *Request Frame* for the Write Memory by Address service consists of the following fields:

| Field Name              | Size        | Description                                                     |
|--------------------------|-------------|-----------------------------------------------------------------|
| **Service ID (SID)**     | 1 byte      | The service identifier, `0x3D` for Write Memory by Address.     |
| **Data by Identifier**   | 1 byte      | The Data Identifier (DID) for the memory location to write to.  |
| **Memory Size**          | 1 byte      | The size of the memory region to be written (in bytes).         |
| **Memory Address**       | 2 bytes     | The starting memory address where the data will be written.     |
| **Data Information**     | Variable    | The data to be written to the specified memory address.         |

### Request Frame Example

In this example, we will write the ECU Serial Number (DID = 0xF18C) to a specific memory address.

- **DID (Data by Identifier)**: `0xF18C`
- **Memory Size**: `0x02` (2 bytes)
- **Memory Address**: `0xA0 0x00`
- **Data Information**: `0xFE 0x0C`

The request frame would look like this:

| Field Name              | Value          |
|--------------------------|----------------|
| **Service ID (SID)**     | `0x3D`         |
| **Data by Identifier**   | `0xF1`         |
| **Memory Size**          | `0x8C`         |
| **Memory Address**       | `0x02 0xA0 0x00` |
| **Data Information**     | `0xFE 0x0C`    |

#### Explanation of Fields:
- **Service ID (SID)**: Identifies the Write Memory by Address service.
- **Data by Identifier (DID)**: The Data Identifier that specifies which memory area or parameter is being written to.
- **Memory Size**: The size of the memory area being written, represented in bytes.
- **Memory Address**: The start address in the memory where the data will be written.
- **Data Information**: The actual data to be written to the memory.

### Positive Response Frame

After receiving a valid request, the ECU responds with a *Positive Response Frame* indicating that the write operation was successful. This frame includes the same fields as the request frame:

| Field Name              | Size        | Description                                                     |
|--------------------------|-------------|-----------------------------------------------------------------|
| **Response ID**          | 1 byte      | The response service ID, `0x7D` for Write Memory by Address.    |
| **Data by Identifier**   | 1 byte      | The DID for the written memory region.                          |
| **Memory Size**          | 1 byte      | The size of the memory region written to.                       |
| **Memory Address**       | 2 bytes     | The memory address where the data was written.                  |

**Positive Response Example**:

| Field Name              | Value          |
|--------------------------|----------------|
| **Response ID**          | `0x7D`         |
| **Data by Identifier**   | `0xF1`         |
| **Memory Size**          | `0x8C`         |
| **Memory Address**       | `0x02 0xA0 0x00` |

In this example, the ECU has successfully written the data to the specified memory address and acknowledges the request with the corresponding DID, memory size, and memory address.

### Negative Response Frame

If the ECU encounters an error during the memory write process, such as an invalid address, insufficient memory, or security access issues, it will return a *Negative Response Frame*. This frame includes:

| Field Name            | Size        | Description                                                       |
|------------------------|-------------|-------------------------------------------------------------------|
| **Response ID**        | 1 byte      | The response service ID, `0x7F` for negative responses.           |
| **Service ID (SID)**   | 1 byte      | The service ID that generated the error (in this case, `0x3D`).   |
| **Negative Response Code** | 1 byte  | The specific error code indicating the failure reason.           |

**Negative Response Example**:

| Field Name                  | Value      |
|------------------------------|------------|
| **Response ID**              | `0x7F`     |
| **Service ID (SID)**         | `0x3D`     |
| **Negative Response Code**   | `0x31`     |

In this example, `0x31` indicates a "Write Error" or "Security Access Denied" issue.

## Address and Data Writing Process

The *Write Memory by Address* service allows for writing to both individual and contiguous memory regions. The data is directly written to the specified memory address and can be used to change ECU parameters or perform memory clearing tasks.

### Typical Use Cases
- **Clearing Non-Volatile Memory**: This service can be used to reset certain ECU parameters stored in non-volatile memory, such as calibration data or error logs.
- **Updating Calibration Values**: Technicians or diagnostic tools can modify calibration data directly in memory without requiring additional tools or interfaces.
- **Firmware Updates**: Memory regions that store firmware can be updated using this service (although typically, this would be part of a more specific flashing process).

### Data Integrity and Alignment
When writing data to memory, it's essential to ensure proper alignment of the memory regions and respect the memory size specified. Writing data that exceeds the available memory space or misaligning data can cause errors or corrupt the ECU's memory. It is essential to verify the memory boundaries before performing a write operation.

## Security Access

Just like the *Read Memory by Address* service, *Write Memory by Address* may also require security access. Before data can be written to specific memory regions, the ECU might require the diagnostic tool to authenticate through a security access procedure.

### Example of Security Access

Before writing data to a sensitive memory region, the client might need to use the *Security Access* service (`0x27`) to gain permission. If the ECU denies access due to insufficient security clearance, the negative response (`0x31`) would indicate the need for security credentials.

## Conclusion

The *Write Memory by Address* service (SID 0x3D) provides a powerful method for writing data to specific memory regions within an ECU. By structuring requests and responses correctly and ensuring proper security and memory alignment, this service can be used effectively for ECU calibration, data updates, and memory clearing. It is essential to adhere to the specified message formats and handle potential errors to ensure successful operation and data integrity.

### Key Considerations:
- Verify memory boundaries and alignment to avoid memory corruption.
- Ensure security access is granted before writing sensitive memory regions.
- Handle errors gracefully, particularly those related to access and memory write failures.