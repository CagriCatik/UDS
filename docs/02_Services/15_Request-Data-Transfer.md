---
sidebar_position: 15
---


# Transfer Data - 0x36

The **Transfer Data (0x36)** service is a crucial component of the **Unified Diagnostic Services (UDS)** protocol (ISO 14229) used to facilitate the actual transfer of data between a client (e.g., a diagnostic tool or test equipment) and an ECU (Electronic Control Unit). This service works in conjunction with the **Request Download (0x34)** and **Request Upload (0x35)** services, where **Request Download** initiates a transfer of data to the ECU and **Request Upload** retrieves data from the ECU. The **Transfer Data (0x36)** service handles the transfer of the data itself in blocks.

The **Transfer Data** service is responsible for ensuring that data is correctly sent and received during both **upload** and **download** operations. It provides an efficient way to manage the flow of large datasets, dividing them into manageable blocks for sequential transfer. This service includes features for managing block sequences and supporting error detection during the transfer process, ensuring data integrity.

## **Purpose and Use Cases**

The **Transfer Data (0x36)** service is utilized for both uploading and downloading data between the client and the ECU, following the initiation of a **Request Download (0x34)** or **Request Upload (0x35)** service. Typical use cases include:

- **Firmware Flashing**: When downloading a new firmware or software image to an ECU.
- **Data Upload**: Uploading diagnostic data, logs, or configuration information from the ECU to the diagnostic tool.
- **Calibration**: Transferring calibration data to or from the ECU.
- **Over-the-Air (OTA) Updates**: Enabling the transfer of large files or software updates to an ECU.

The **Transfer Data** service allows for the **sequential transfer of data blocks**, providing an efficient way to handle large volumes of data, especially in scenarios where the memory block sizes are large or the data is too large to be handled in a single transmission.

## **Overview of the Transfer Data (0x36) Service**

The **Transfer Data (0x36)** service is responsible for the actual transmission of data that was requested either to be uploaded or downloaded in the **Request Upload (0x35)** or **Request Download (0x34)** service. The data is transmitted in sequential blocks, with each block being acknowledged by the ECU. The blocks are sent and received based on the **Block Sequence Counter**.

This service helps manage the flow of data by handling the transfer of blocks and ensuring that the data can be properly reconstructed after transmission. Error handling mechanisms, such as retransmitting blocks when errors are detected, are also built into the service.

## **Request Frame Format for Transfer Data (0x36)**

The **Transfer Data (0x36)** request frame format consists of several parameters required to initiate the data transfer. Below is the detailed breakdown of the frame format:

| **Byte Number** | **Parameter Name**               | **Description**                                                                                                                                             |
|-----------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1**           | **SID (Service Identifier)**     | The **Service Identifier** for the **Transfer Data** service, which is always **0x36**. This signifies the start of a data transfer.                       |
| **2**           | **Block Sequence Counter**       | A 1-byte value used to track the sequence of the data blocks being transferred. It starts at **0x01** for the first block and increments by 1 for each subsequent block. If the counter reaches **0xFF**, it wraps back to **0x00**. |
| **3**           | **Transfer Request Parameter Record** | Contains additional information necessary for the transfer, including how the data should be processed, such as the maximum block size, or the compression/encryption method to be used (if applicable). |

### **Block Sequence Counter Details**

The **Block Sequence Counter** is used to ensure that the data is transmitted in the correct sequence. The client starts the transfer with **0x01**, and for each subsequent block of data, the counter is incremented. This sequence allows both the client and the ECU to track which blocks have been transmitted and which remain to be sent. The block sequence counter also helps detect missing or out-of-order blocks, facilitating error recovery.

## **Response Frame Format for Transfer Data (0x36)**

The **Transfer Data (0x36)** service response indicates the status of the data transfer. The ECU will send either a **positive** or **negative** response depending on whether the transfer was successful or if there was an issue. The response format is as follows:

| **Byte Number** | **Parameter Name**               | **Description**                                                                                                                                             |
|-----------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1**           | **PCI Length**                    | Specifies the length of the response frame.                                                                                                                |
| **2**           | **Response SID**                  | The **Service Identifier** for the response. For a **Transfer Data** response, this is always **0x76** (0x36 + 0x40).                                       |
| **3**           | **Block Sequence Counter**        | A 1-byte value that mirrors the **Block Sequence Counter** in the request frame. This tells the client which data block is being processed.               |
| **4**           | **Transfer Response Parameter Record** | Contains parameters necessary for processing the transfer, such as the size of the data block and any further instructions for managing the transfer. |

### **Positive Response**

A **positive response** indicates that the ECU has successfully received the data block and can continue the transfer. The **Block Sequence Counter** in the response matches the block sequence from the request, confirming the successful reception of that block.

- The **Transfer Response Parameter Record** may include any additional details, such as the maximum block size for subsequent transfers or any additional status information.

### **Negative Response**

If the ECU encounters an error while processing the data, it will send a **negative response** with an appropriate **Negative Response Code (NRC)**. This could occur if the data is not valid, the memory allocation fails, or there is a sequence mismatch.

| **Byte Number** | **Parameter Name**               | **Description**                                                                                                                                             |
|-----------------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1**           | **PCI Length**                    | Specifies the length of the response frame.                                                                                                                |
| **2**           | **Request SID**                   | The **Service Identifier** for the **Transfer Data** service, which is always **0x36**.                                                                    |
| **3**           | **NRC**                           | The **Negative Response Code (NRC)** indicating why the transfer failed.                                                                                  |

### **Supported Negative Response Codes (NRC)**

| **NRC Value** | **Description**                                                     | **Mnemonic**      |
|---------------|---------------------------------------------------------------------|-------------------|
| **0x13**      | Incorrect message length or invalid format                         | IML               |
| **0x24**      | Request sequence error (e.g., invalid block sequence)              | RSE               |
| **0x31**      | Request out of range (e.g., invalid memory address or block size)  | ROOR              |
| **0x33**      | Security access denied (e.g., permission issues)                   | SAD               |
| **0x71**      | Transfer data suspended (e.g., error in data transfer size)        | TDS               |
| **0x72**      | General programming failure (e.g., hardware issues during transfer) | GPF               |
| **0x73**      | Wrong block sequence counter (e.g., mismatch in expected order)    | WBSC              |
| **0x92/0x93** | Voltage too high/low (e.g., out-of-range voltage during transfer)  | VTH/VTL           |

## **Transfer Data Process**

1. **Initiating the Transfer**: The **Transfer Data (0x36)** service is initiated after either a **Request Download (0x34)** or **Request Upload (0x35)** service has been successfully processed. The first data block is transferred with the initial **Block Sequence Counter** value set to **0x01**.
   
2. **Data Block Transfer**: Each block of data is sent from the client to the ECU (for download) or from the ECU to the client (for upload), with the **Block Sequence Counter** being incremented after each successful block transfer. The ECU responds with either a positive acknowledgment or a negative error response based on whether the transfer was successful.

3. **Error Handling**: If any errors occur (such as a missing block or sequence mismatch), the ECU may return a **negative response**, and the client must handle retransmission of the data block or adjust the transfer sequence as necessary.

4. **Completion**: Once all blocks of data have been transferred, the client and ECU can confirm the completion of the transfer. The **Request Transfer Exit (0x37)** service can be used to terminate the session, ensuring that the transfer process is properly finalized.

---

## **Conclusion**

The **Transfer Data (0x36)** service is a vital part of the UDS protocol, enabling the actual movement of data between the client and ECU. Whether performing software updates, uploading diagnostic logs, or transferring large calibration datasets, this service ensures that the data is transferred efficiently in sequential blocks. Error handling, block sequencing, and data integrity are core aspects of this service, making it indispensable for reliable and secure data exchange in automotive diagnostics, service, and maintenance. Combined with the **Request Download (0x34)** and **Request Upload (0x35)** services, the **Transfer Data (0x36)** service provides the foundation for comprehensive data management in UDS-enabled systems.