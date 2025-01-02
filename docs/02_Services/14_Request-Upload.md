---
sidebar_position: 14
---


# Request Upload - 0x35

The **Request Upload (0x35)** service is one of the core services in the **Unified Diagnostic Services (UDS)** protocol (ISO 14229), enabling the client (typically a diagnostic tool or test equipment) to initiate the transfer of data from an ECU (Electronic Control Unit) to the client. The **Request Upload (0x35)** service is widely used in automotive diagnostics and service environments to retrieve diagnostic data, ECU logs, configuration files, or other data stored in the ECU’s memory.

This service is essential for scenarios where data needs to be extracted from the ECU for analysis, troubleshooting, diagnostics, or reprogramming. It complements the **Request Download (0x34)** service, which is used for uploading data **to** the ECU, whereas **Request Upload** is specifically for **extracting** data from the ECU.

## **Purpose and Use Cases**

The **Request Upload (0x35)** service is employed when the client needs to retrieve data stored in the ECU, making it one of the most useful services for diagnostics and ECU configuration. Typical use cases include:

- **Diagnostic Data Retrieval**: Extracting error codes, fault logs, or other diagnostic information from the ECU.
- **ECU Logs**: Uploading log files for analysis or troubleshooting of ECU behavior.
- **Configuration Data**: Retrieving configuration or calibration data from the ECU to check current settings or backup configuration.
- **Firmware or Software Retrieval**: In some cases, it may be used to upload firmware or software from the ECU for analysis, especially during reverse engineering or diagnostic procedures.

The **Request Upload** service allows for efficient extraction of relevant data for diagnostics or software maintenance, making it indispensable for service centers, test labs, and OEMs.

## **Overview of the Request Upload (0x35) Service**

The **Request Upload (0x35)** service is initiated by the client to request that the ECU upload specific data from its memory to the client. The client provides a memory address where the data is stored, along with the size of the data to be transferred. The ECU validates the request and responds by transmitting the data in sequential blocks. The data transfer proceeds in a series of requests and responses until the entire block of data is uploaded.

The service requires that the client and ECU communicate in a way that ensures the correct transfer of data, even for large files or multiple data segments.

## **Request Frame Format for Request Upload (0x35)**

The **Request Upload** frame contains several parameters, including the memory address and the size of the data to be uploaded. Below is the detailed breakdown of the frame format:

| **Byte Number** | **Parameter Name**               | **Description**                                                                                                                                             |
|-----------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1**           | **SID (Service Identifier)**     | This is the service identifier for the **Request Upload** service, which is always **0x35**.                                                              |
| **2**           | **Data Format Identifier**       | A 1-byte value specifying the encryption and compression methods for the data transfer.                                                                 |
|                 |                                   | - **Higher nibble** (bits 7-4): Compression method                                                                                                           |
|                 |                                   | - **Lower nibble** (bits 3-0): Encryption method                                                                                                           |
|                 |                                   | If the value is **0x00**, it indicates no encryption or compression is used.                                                                               |
| **3**           | **Address and Length Format Identifier** | A 1-byte field specifying the size of the memory address and memory size fields.                                                                         |
|                 |                                   | - **Higher nibble** (bits 7-4): Number of bytes of the **Memory Size** parameter.                                                                         |
|                 |                                   | - **Lower nibble** (bits 3-0): Number of bytes of the **Memory Address** parameter.                                                                      |
| **4–7**         | **Memory Address**                | Specifies the starting address in the ECU’s memory from which the data will be uploaded. This is a 4-byte value.                                           |
| **8–11**        | **Memory Size**                   | A 4-byte field specifying the size of the data block that is to be uploaded from the ECU’s memory.                                                           |

### **Data Format Identifier Details**

The **Data Format Identifier** defines how the data is handled during the upload process. It specifies the compression and encryption methods to be applied to the data, as defined by the OEM. The field is structured as follows:

- **Higher nibble** (bits 7-4): Compression method (e.g., **0x01** for compression type 1).
- **Lower nibble** (bits 3-0): Encryption method (e.g., **0x01** for encryption type 1).
- **Value of 0x00**: No compression or encryption applied.

For example, if the **Data Format Identifier** is **0x11**, this would indicate **compression method 1** and **encryption method 1**.

### **Address and Length Format Identifier**

The **Address and Length Format Identifier** specifies how the memory address and size fields are encoded. It ensures that the client and ECU correctly interpret the sizes of the memory address and data block.

- **Higher nibble** (bits 7-4): Specifies the number of bytes in the **Memory Size** field.
- **Lower nibble** (bits 3-0): Specifies the number of bytes in the **Memory Address** field.

For instance, if the **higher nibble** is **0x04**, the **Memory Size** is a 4-byte value, and if the **lower nibble** is **0x04**, the **Memory Address** is also a 4-byte value.

## **Response Frame Format for Request Upload (0x35)**

Once the **Request Upload (0x35)** service is received by the ECU, it processes the request and prepares to upload the requested data. The ECU responds with a **positive** or **negative** response, based on whether the request was successfully processed.

### **Positive Response**

If the ECU successfully accepts the upload request, it sends a **positive response** frame with the following structure:

| **Byte Number** | **Parameter Name**               | **Description**                                                                                                                                             |
|-----------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1**           | **PCI Length**                    | Specifies the length of the response frame.                                                                                                                |
| **2**           | **Response SID**                  | The **Service Identifier** for the response. For a **Request Upload** response, this is always **0x75** (0x35 + 0x40).                                     |
| **3**           | **Length Format Identifier**      | A 1-byte value specifying the length of the **Max Number of Block Length** parameter.                                                                 |
| **4**           | **Max Number of Block Length**    | A 2-byte field indicating the maximum number of bytes the client can expect to receive in each data block.                                                      |

The **Max Number of Block Length** indicates how many bytes the client can expect in each data block, guiding the client on how to structure the data upload.

### **Negative Response**

If the ECU cannot process the **Request Upload** request (due to incorrect parameters, invalid memory address, or other conditions), it sends a **negative response** containing the **Negative Response Code (NRC)**.

| **Byte Number** | **Parameter Name**               | **Description**                                                                                                                                             |
|-----------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1**           | **PCI Length**                    | Specifies the length of the response frame.                                                                                                                |
| **2**           | **Request SID**                   | The **Service Identifier** for the **Request Upload** service, which is always **0x35**.                                                                |
| **3**           | **NRC**                           | The **Negative Response Code (NRC)** that indicates why the request was rejected.                                                                        |

### **Supported Negative Response Codes (NRC)**

| **NRC Value** | **Description**                                               | **Mnemonic**      |
|---------------|---------------------------------------------------------------|-------------------|
| **0x13**      | Incorrect message length or invalid format                   | IML               |
| **0x22**      | Conditions not correct (e.g., invalid parameters)             | CNC               |
| **0x31**      | Request out of range (e.g., invalid memory address or size)   | ROOR              |
| **0x33**      | Security access denied (e.g., insufficient permissions)        | SAD               |
| **0x70**      | General programming failure (e.g., hardware issues)           | GPF               |

---

## **Request Upload Process**

1. **Initiating the Request**: The client sends a **Request Upload (0x35)** frame, specifying the memory address, memory size, and data format information. The client may also specify encryption or compression options as per the OEM's requirements.
   
2. **Server Validation**: Upon receiving the request, the ECU validates the memory address, size, and format of the requested data. If everything is valid, the ECU prepares the data for upload. If validation fails (e.g., invalid address or size), the ECU sends a **negative response** with the appropriate **NRC**.
   
3. **Data Transfer**: Once the validation step is complete, the ECU responds with a **positive response** indicating the maximum number of bytes that can be transferred in each block. The client then begins receiving the data in blocks, based on the **Max Number of Block Length**.
   
4. **Completion**: After the entire data block has been uploaded, the ECU processes the data and completes the transfer. If the transfer was successful, the ECU sends

 a **positive confirmation**. The **Request Transfer Exit (0x37)** service can be used to terminate the data upload session.

---

## **Conclusion**

The **Request Upload (0x35)** service is a key component of the UDS protocol, enabling clients to retrieve data from an ECU. It is commonly used for extracting diagnostic data, error logs, or configuration files. The service allows for efficient block-based data transfer, with mechanisms in place for ensuring that data is correctly uploaded from the ECU to the client. Proper error handling through **negative response codes** ensures robustness in the event of issues during the upload process. When combined with the **Transfer Data (0x36)** service, the **Request Upload (0x35)** service forms an essential tool for automotive diagnostics, maintenance, and configuration tasks.