---
sidebar_position: 6
---

# Read Memory by Address - 0x23 

## Introduction

The **Read Memory by Address** (RMB) service, identified by Service ID (SID) 0x23 in the Unified Diagnostic Services (UDS) protocol, allows a diagnostic tool or client to request data from a specific memory location in an Electronic Control Unit (ECU). This functionality is essential for diagnostics, calibration, and firmware updates, enabling the retrieval of specific memory regions like firmware, configuration settings, or calibration data in automotive ECUs.

The **Read Memory by Address** service supports the retrieval of memory in arbitrary regions, which is important for diagnostic processes that require reading memory areas directly from the ECU to evaluate performance, troubleshoot faults, or validate configurations. This service is integral to the broader suite of UDS services used in automotive diagnostics.

### Service ID

- **Request SID**: 0x23
- **Response SID**: 0x63

### Purpose

The **Read Memory by Address** service enables a client to read a specified range of memory from an ECU, defined by the starting address and the length (in bytes) of the data to be read. This service is widely used for diagnostic tasks, allowing the client to extract data such as calibration data, error logs, or any other ECU memory.

## Frame Format

The **Read Memory by Address** service is carried out by sending a structured message that follows a specific format for both the request and the response frames. Below, we break down the format for each type of frame.

### Request Frame

The **Request Frame** for the Read Memory by Address service consists of the following fields:

| Field Name                          | Size        | Description                                                                                     |
|--------------------------------------|-------------|-------------------------------------------------------------------------------------------------|
| **Service ID (SID)**                 | 1 byte      | The service identifier, `0x23` for Read Memory by Address.                                        |
| **Address and Length Format Identifier** | 1 byte  | The identifier that holds both the memory address and size, split into two parts (lower and upper nibbles). |
| **Memory Size**                      | 2 bytes     | The number of bytes to read from the ECU’s memory.                                               |
| **Memory Address**                   | 2 bytes     | The starting memory address to read from.                                                        |

#### Explanation of Fields

- **Service ID (SID)**: The service ID, `0x23`, identifies the service type.
- **Address and Length Format Identifier**: This field encodes both the memory address and the memory size into a single byte. The lower nibble indicates the address, while the upper nibble indicates the memory size.
- **Memory Size**: This 2-byte field specifies how many bytes of memory the client wants to read.
- **Memory Address**: This 2-byte field contains the starting address in the ECU's memory from where the read operation will begin.

### Request Frame Example

For a request with the following parameters:

- **Starting memory address**: `0x6872` (16-bit address)
- **Memory size**: `0x02` (2 bytes)

The request frame would look like this:

| Field Name                          | Value      |
|--------------------------------------|------------|
| **Service ID (SID)**                 | `0x23`     |
| **Address and Length Format Identifier** | `0x22`     |
| **Memory Size**                      | `0x02`     |
| **Memory Address**                   | `0x68 0x72` |

In the **Address and Length Format Identifier** `0x22`:
- **Lower nibble (0x2)** represents the **memory address** (`0x6872`).
- **Upper nibble (0x2)** represents the **memory size** (2 bytes).

### Response Frame

The ECU will send a response frame after processing the request. There are two types of response frames: positive and negative.

#### Positive Response Frame

A *Positive Response Frame* is sent when the memory read operation is successful. It contains the following fields:

| Field Name        | Size        | Description                                                              |
|--------------------|-------------|--------------------------------------------------------------------------|
| **Response ID**    | 1 byte      | The response service ID, `0x63` for Read Memory by Address.              |
| **Data Record**    | Variable    | The memory data retrieved from the requested address.                    |

#### Positive Response Example

If the ECU successfully reads 4 bytes of data from the memory address `0x6872`, the positive response frame will look like this:

| Field Name        | Value        |
|--------------------|--------------|
| **Response ID**    | `0x63`       |
| **Data Record**    | `0x55 0x0A 0x8C 0x00` |

The ECU has successfully read 4 bytes of memory, starting from `0x6872`, with the data returned as `0x55 0x0A 0x8C 0x00`.

#### Negative Response Frame

A *Negative Response Frame* is returned if the request cannot be fulfilled due to an error, such as invalid memory access, security restrictions, or an out-of-range address. It contains the following fields:

| Field Name                | Size        | Description                                                                  |
|----------------------------|-------------|------------------------------------------------------------------------------|
| **Response ID**            | 1 byte      | The response service ID, `0x7F` for negative responses.                       |
| **Negative Response Code** | 1 byte      | The specific error code indicating the cause of the failure.                 |

#### Negative Response Example

In the case where there is a security access issue (e.g., unauthorized access to a memory region), the response might look like this:

| Field Name                | Value        |
|----------------------------|--------------|
| **Response ID**            | `0x7F`       |
| **Negative Response Code** | `0x23`       |

Here, `0x7F` indicates a negative response, and `0x23` is the response code representing a "Security Access Denied" issue.

## Address and Length Format Identifier

The **Address and Length Format Identifier** is a critical component of the request frame. It encodes both the memory address and the memory size into a single byte. This method optimizes the message format and minimizes the number of fields required in the request frame.

### Breakdown of the Identifier

- **Lower Nibble (bits 0–3)**: Specifies the starting memory address in the ECU.
- **Upper Nibble (bits 4–7)**: Specifies the memory size to be read.

For example:
- If the **Address and Length Format Identifier** is `0x24`, the breakdown would be:
  - **Upper nibble (0x2)**: Represents the **memory address**.
  - **Lower nibble (0x4)**: Represents the **memory size** (4 bytes).

This indicates that the memory to be read starts at address `0x24`, and 4 bytes of memory will be read.

## Security Access

Accessing certain memory regions in an ECU may require security authentication to ensure that unauthorized parties do not manipulate critical systems or configurations. The ECU may require a prior **Security Access** service (typically `0x27`) to authenticate the client before granting memory access.

In case security access is not granted, or if the client fails to authenticate, the ECU will respond with a **Negative Response Frame** containing an error code indicating the failure, such as `0x23` for "Security Access Denied."

### Security Request Frame Example

If security access is required, the client first sends a request for security access using a service like `0x27`. After successful authentication, the client can proceed with the *Read Memory by Address* request.

## Conclusion

The *Read Memory by Address* (RMB) service (SID 0x23) is a vital diagnostic tool for accessing specific memory regions within an ECU. This service is essential for diagnostics, calibration, and firmware verification in automotive ECUs. By understanding the request and response message formats, as well as the role of the Address and Length Format Identifier, technicians can efficiently extract memory data for further analysis.

### Key Considerations:
- Ensure proper **security access** before attempting to read memory.
- The **Address and Length Format Identifier** allows compact encoding of memory address and size.
- Both **positive** and **negative** responses should be properly handled, especially regarding security access and memory errors.

By adhering to the UDS protocol and correctly implementing these frame formats and procedures, diagnostic tools can perform safe and accurate memory reads, enhancing the efficiency of vehicle maintenance and diagnostics.