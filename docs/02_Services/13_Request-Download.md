---
sidebar_position: 13
---


# Request Download - 0x34

The **Request Download (0x34)** service is one of the foundational services in the **Unified Diagnostic Services (UDS)** protocol (ISO 14229). It plays a critical role in enabling data transfer from the client (diagnostic tool or test equipment) to the ECU (Electronic Control Unit). This service is essential for operations such as **software updates**, **firmware flashing**, and **calibration data management**. It allows a client to send data (typically software or configuration files) to the ECU, where it is written to the specified memory location.

The **Request Download** service is used primarily when the client needs to write data to the ECU’s memory, whether for software updates, flashing firmware, or performing calibration or configuration tasks. The data is transferred in blocks, and each block is written to the ECU’s memory sequentially.

## **Purpose and Use Cases**

The **Request Download (0x34)** service is used when the client needs to upload data to the ECU, typically in the following scenarios:
- **Firmware/Software Updates**: Flashing or updating the ECU’s firmware or software with new code.
- **Calibration**: Uploading calibration data for sensor tuning or other ECU parameters.
- **Configuration Data**: Writing configuration data to the ECU to enable or disable certain features or change settings.
- **Diagnostic Data Upload**: In some cases, uploading diagnostic data for analysis.

While the **Request File Transfer (0x38)** service is used for systems with a file system, the **Request Download** service operates at a lower level, dealing with raw memory blocks, and is typically used when the ECU does not have a complex file system.

## **Overview of the Request Download (0x34) Service**

The **Request Download** service is initiated by the client to request the download of data to the ECU. The client specifies the memory location where the data should be written, as well as the size of the data to be transferred. Upon receiving the request, the ECU validates the parameters, allocates memory if necessary, and prepares for the actual data transfer. The data is transferred in blocks, and the ECU responds to the client to indicate whether the transfer was successful.

This service is particularly crucial in automotive diagnostic scenarios where the ECU needs to be reprogrammed or updated, and it requires careful handling of memory addresses and sizes to avoid overwriting critical data.

## **Request Frame Format for Request Download (0x34)**

The request frame for the **Request Download (0x34)** service contains several parameters, including the **memory location**, **data size**, and **data format information**. Below is the detailed breakdown of the frame format:

| **Byte Number** | **Parameter Name**               | **Description**                                                                                                                                             |
|-----------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1**           | **SID (Service Identifier)**     | This is the service identifier for the **Request Download** service, which is always **0x34**.                                                              |
| **2**           | **Data Format Identifier**       | A 1-byte value specifying the encryption and compression methods for the data transfer.                                                                 |
|                 |                                   | - **Higher nibble** (bits 7-4): Compression method                                                                                                           |
|                 |                                   | - **Lower nibble** (bits 3-0): Encryption method                                                                                                           |
|                 |                                   | If the value is **0x00**, it indicates no encryption or compression is used.                                                                               |
| **3**           | **Address and Length Format Identifier** | A 1-byte field specifying the size of the memory address and memory size fields.                                                                         |
|                 |                                   | - **Higher nibble** (bits 7-4): Number of bytes of the **Memory Size** parameter.                                                                         |
|                 |                                   | - **Lower nibble** (bits 3-0): Number of bytes of the **Memory Address** parameter.                                                                      |
| **4–7**         | **Memory Address**                | Specifies the starting address of the memory in the ECU where the data should be written. This is a 4-byte value.                                           |
| **8–11**        | **Memory Size**                   | A 4-byte field specifying the size of the data block that is to be written to the ECU’s memory.                                                             |

### **Data Format Identifier Details**

The **Data Format Identifier** indicates how the data is to be processed during the download operation. This includes specifying whether the data is compressed or encrypted, based on the OEM's specifications. The field is structured as follows:

- **Higher nibble** (bits 7-4): Compression method (defined by the OEM).
- **Lower nibble** (bits 3-0): Encryption method (defined by the OEM).
- **Value of 0x00**: No compression or encryption applied.

For example, a value of **0x11** would indicate **compression method 1** and **encryption method 1**.

### **Address and Length Format Identifier**

The **Address and Length Format Identifier** defines how many bytes the memory address and memory size will occupy. This ensures that both the memory address and the data size are properly interpreted during the transfer. The field is split into two parts:

- **Higher nibble**: Specifies the size of the **Memory Size** field in bytes.
- **Lower nibble**: Specifies the size of the **Memory Address** field in bytes.

For example, if the **higher nibble** is **0x04**, it means the **Memory Size** is a 4-byte field, and if the **lower nibble** is **0x04**, the **Memory Address** is also a 4-byte field.

## **Response Frame Format for Request Download (0x34)**

Once the ECU receives the **Request Download** request, it processes the parameters and prepares for the download. The ECU responds with either a **positive** or **negative response**.

### **Positive Response**

If the ECU successfully accepts the download request, it will send a **positive response** with the following frame structure:

| **Byte Number** | **Parameter Name**               | **Description**                                                                                                                                             |
|-----------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1**           | **PCI Length**                    | Specifies the length of the response frame.                                                                                                                |
| **2**           | **Response SID**                  | The **Service Identifier** for the response. For a **Request Download** response, this is always **0x74** (0x34 + 0x40).                                    |
| **3**           | **Length Format Identifier**      | A 1-byte value that specifies the length of the **Max Number of Block Length** parameter.                                                                 |
| **4**           | **Max Number of Block Length**    | A 2-byte field indicating the maximum number of bytes the client can send in the next transfer block.                                                      |

The **Max Number of Block Length** indicates how many data bytes the client should expect in each transfer block, and this is vital for proper block-based transfer.

### **Negative Response**

If the ECU cannot process the **Request Download** request (due to incorrect parameters, invalid memory address, or other conditions), it sends a **negative response** containing the **Negative Response Code (NRC)**.

| **Byte Number** | **Parameter Name**               | **Description**                                                                                                                                             |
|-----------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1**           | **PCI Length**                    | Specifies the length of the response frame.                                                                                                                |
| **2**           | **Request SID**                   | The **Service Identifier** for the **Request Download** service, which is always **0x34**.                                                                |
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

## **Request Download Process**

1. **Initiating the Request**: The client sends a **Request Download (0x34)** frame, specifying the memory address, memory size, and data format information. The client may also specify encryption or compression options depending on the requirements.
   
2. **Server Validation**: Upon receiving the request, the ECU validates the memory address, size, and format of the data. If everything is valid, the ECU prepares the memory for the download. If validation fails (e.g., invalid address or size), the ECU sends a **negative response** with an appropriate **NRC**.
   
3. **Data Transfer**: After the validation step, the ECU responds with a **positive response** that includes the maximum block length for the data. The client then begins sending the data in blocks according to the **Max Number of Block Length**.
   
4. **Completion**: Once all the data is transferred, the ECU processes the data and writes it to memory. If the transfer was successful, the ECU sends a **positive confirmation**. The **Request Transfer Exit (0x37)** service can be used to terminate the data transfer session.

---

## **Conclusion**

The **Request Download (0x34)**

 service is essential for transferring data from a client to an ECU in a controlled manner. It is used in various scenarios, including firmware updates, calibration, and software flashing. The service works by specifying memory locations and data sizes, ensuring that the data is correctly written to the ECU’s memory. Proper error handling through **negative response codes** ensures robustness during the data transfer process. Combined with the **Transfer Data (0x36)** service, the **Request Download (0x34)** service forms the backbone of ECU data management, enabling efficient and reliable updates and configuration changes.