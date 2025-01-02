---
sidebar_position: 12
---


# Request File Transfer - 0x38

The **Request File Transfer (0x38)** service is a sophisticated mechanism in the **Unified Diagnostic Services (UDS)** protocol (ISO 14229), designed to facilitate file-based data transfer between a client (e.g., diagnostic tool) and an ECU (Electronic Control Unit). Unlike traditional byte transfer methods, the **Request File Transfer (0x38)** service is optimized for systems that operate with file systems, such as those using Linux or embedded operating systems, where files are the primary units of data storage. This service provides a structured approach to downloading and uploading files to and from the ECU, allowing operations like file addition, replacement, deletion, and reading of files or directories.

In addition to transferring application files, the **Request File Transfer (0x38)** service is used to interact with the file system on the ECU, which can be crucial for tasks like software updates, firmware flashing, and configuration data management.

## **Purpose and Use Cases**

The **0x38 service** is often used when dealing with ECUs that support a file system (e.g., Linux-based ECUs). It offers an alternative to the **Request Download (0x34)** and **Request Upload (0x35)** services, which are based on memory block transfers and are better suited for ECUs without a file system.

Key use cases for the **Request File Transfer (0x38)** service include:
- **Over-the-Air (OTA) Software Updates**: Allows downloading of new software or firmware to ECUs with a file system.
- **Data Logging**: Uploading logs or configuration files from the ECU to a diagnostic tool.
- **Calibration Data Management**: Uploading or downloading calibration files for ECU tuning or diagnostics.
- **Firmware Flashing**: Replacing existing firmware or adding new firmware files to the ECU.

## **Overview of the Request File Transfer (0x38) Service**

The **0x38** service is initiated by the client to request a file-based transfer from the ECU. The client sends a request specifying the desired operation (add, delete, replace, or read files) along with the file information. Once the server (ECU) processes the request, it responds with either a positive or negative response based on the validity of the operation.

This service is typically used in conjunction with the **Transfer Data (0x36)** service, which handles the actual file data transfer, and the **Request Transfer Exit (0x37)** service, which terminates the file transfer session.

## **Request Frame Format for Request File Transfer (0x38)**

The request frame for the **Request File Transfer (0x38)** service contains several parameters that are required to identify the file operation, specify the file to be transferred, and provide details about its size and format. Below is the detailed format:

| **Byte Number** | **Parameter Name**         | **Description**                                                                                                                                           |
|-----------------|----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1**           | **SID (Service Identifier)** | This is the service identifier for the **Request File Transfer** service. It is always **0x38**.                                                       |
| **2**           | **Mode of Operation (MOP)**  | Defines the operation to be performed on the file or directory. Possible values:                                                                        |
|                 |                            | - **0x01**: Add File                                                                                                                                      |
|                 |                            | - **0x02**: Delete File                                                                                                                                   |
|                 |                            | - **0x03**: Replace File                                                                                                                                  |
|                 |                            | - **0x04**: Read File                                                                                                                                     |
|                 |                            | - **0x05**: Read Directory                                                                                                                                 |
| **3-4**         | **File Path and Name Length**| A 2-byte value indicating the length of the **File Path and Name** in bytes.                                                                            |
| **5 to (5 + n - 1)** | **File Path and Name**      | Specifies the file or directory path in the ECU’s file system. This value is encoded in ASCII. The number of bytes is defined by **File Path and Name Length**.|
| **5 + n**       | **Data Format Identifier**  | A 1-byte value specifying the data format (compression and encryption) for the file:                                                                   |
|                 |                            | - **Higher nibble**: Compression method (bits 7-4)                                                                                                      |
|                 |                            | - **Lower nibble**: Encryption method (bits 3-0)                                                                                                        |
| **5 + n + 1**   | **File Size Parameter Length** | A 1-byte field that specifies the length of the **File Size Uncompressed** and **File Size Compressed** parameters.                                         |
| **5 + n + 2 to (5 + n + 2 + k - 1)** | **File Size Uncompressed** | A 2-byte value that specifies the uncompressed file size in bytes (if applicable).                                                                 |
| **5 + n + 2 + k to (5 + n + 1 + 2k)** | **File Size Compressed**    | A 2-byte value that specifies the compressed file size in bytes (if applicable).                                                                   |

### **Mode of Operation Details**

The **Mode of Operation (MOP)** parameter defines what kind of operation is being performed on the file or directory. The client sets this parameter based on the desired action:

| **MOP Value** | **Description**                                                                                     |
|---------------|-----------------------------------------------------------------------------------------------------|
| **0x01**      | **Add File**: Adds a file to the specified location in the ECU’s file system.                      |
| **0x02**      | **Delete File**: Deletes the specified file from the ECU’s file system.                            |
| **0x03**      | **Replace File**: Replaces an existing file in the ECU’s file system with the new file.            |
| **0x04**      | **Read File**: Reads the contents of the specified file from the ECU and uploads it to the client.  |
| **0x05**      | **Read Directory**: Reads the contents of the specified directory and uploads the directory contents. |

## **Response Frame Format for Request File Transfer (0x38)**

The ECU responds to the **Request File Transfer (0x38)** request with a response frame. There are two possible responses: **positive** and **negative**. The response frame structure is as follows:

| **Byte Number** | **Parameter Name**              | **Description**                                                                                                                                           |
|-----------------|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1**           | **PCI Length**                   | Specifies the length of the response frame.                                                                                                               |
| **2**           | **Response SID**                 | The Service Identifier for the response, which is **0x78** (0x38 + 0x40).                                                                               |
| **3**           | **Mode of Operation (MOP)**      | Echoes the **Mode of Operation** parameter from the request frame.                                                                                      |
| **4**           | **Length Data Format Identifier**| Specifies the length of the **Max Number of Block Length** parameter.                                                                                   |
| **5**           | **Max Number of Block Length**   | Indicates the maximum number of data bytes to be sent in each transfer block.                                                                           |
| **6**           | **Data Format Identifier**       | Echoes the **Data Format Identifier** parameter from the request frame.                                                                                 |
| **7**           | **File Size or Directory Info Length** | Specifies the length of the **File Size Uncompressed** or **Directory Info Length** (if applicable).                                                      |
| **8**           | **File Size Uncompressed**       | Specifies the size of the uncompressed file in bytes (if applicable).                                                                                   |
| **9**           | **File Size Compressed**         | Specifies the size of the compressed file in bytes (if applicable).                                                                                   |

### **Negative Response**

If the ECU cannot process the file transfer request, it sends a **negative response** frame containing the **Negative Response Code (NRC)**. Common reasons for a negative response include invalid file paths, unsupported file operations, or security access issues.

| **Byte Number** | **Parameter Name** | **Description**                                                                                                                                           |
|-----------------|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1**           | **PCI Length**       | Specifies the length of the response frame.                                                                                                               |
| **2**           | **Request SID**      | The Service Identifier for the **Request File Transfer** service, which is **0x38**.                                                                    |
| **3**           | **NRC**               | The **Negative Response Code** indicating why the request was rejected.                                                                                 |

### **Supported Negative Response Codes (NRC)**

| **NRC Value** | **Description**                                                   | **Mnemonic**  |
|---------------|-------------------------------------------------------------------|---------------|
| **0x13**      | Incorrect message length or invalid format                       | IML           |
| **0x22**      | Condition not correct (e.g., invalid path or file system error)   | CNC           |
| **0x31**      | Request out of range (e.g., invalid file path or size mismatch)  | ROOR          |
| **0x33**      | Security access denied (e.g., insufficient permissions)           | SAD           |
| **0x70**      | Upload/download not accepted (e.g., hardware or memory failure)   | UDN           |

---

## **File Transfer Process**

1. **Initiating a Request**: The client sends a **Request File Transfer (0x38)** message to the ECU specifying the file operation, file path, data format, and file size information.


   
2. **Server Validation**: Upon receiving the request, the ECU validates the file operation (e.g., ensuring the file exists for a read operation, or there is space to add or replace a file). If validation fails, a **negative response** is sent with an appropriate **NRC**.
   
3. **Data Transfer**: If the request is valid, the **Transfer Data (0x36)** service is used to send or receive the file data in blocks. Each block is processed sequentially, and the block sequence counter is incremented to track the progress.

4. **Completion**: After the data transfer is complete, the **Request Transfer Exit (0x37)** service can be used to terminate the file transfer session.

---

## **Conclusion**

The **Request File Transfer (0x38)** service provides a robust and efficient method for file-based data exchange in UDS-compliant ECUs, especially those with file systems. It is versatile, supporting operations such as file addition, replacement, deletion, and reading, which are essential for modern automotive applications like software updates, calibration, and data logging. The service’s structured approach, including the **Transfer Data (0x36)** and **Request Transfer Exit (0x37)** services, ensures reliable and secure file handling between the client and ECU.