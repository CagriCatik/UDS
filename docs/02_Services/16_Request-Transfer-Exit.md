---
sidebar_position: 16
---


# Request Transfer Exit - 0x37

The **Request Transfer Exit (0x37)** service is a critical component in the **Unified Diagnostic Services (UDS)** protocol (ISO 14229), designed to terminate an ongoing data transfer session between the client (e.g., diagnostic tool or testing equipment) and the ECU (Electronic Control Unit). This service is used to gracefully exit from the data transfer process, whether the transfer was initiated through **Request Download (0x34)** or **Request Upload (0x35)**, and is typically issued once all data blocks have been successfully transferred using the **Transfer Data (0x36)** service.

The **Request Transfer Exit** service ensures that the transfer process is properly concluded, resources are released, and the ECU is ready for any other diagnostic or programming tasks that may follow.

## **Purpose and Use Cases**

The **Request Transfer Exit (0x37)** service is used to:
- **Terminate data transfer sessions**: Whether the client has uploaded or downloaded data, this service marks the end of the data transfer process.
- **Free resources on the ECU**: After completing the transfer of data, the ECU may need to release allocated memory or resources used during the transfer process.
- **Prevent errors and incomplete transfers**: By sending a **Request Transfer Exit**, the client ensures that the ECU acknowledges the completion of the transfer, preventing any inconsistencies that could arise if the session is left open.
- **Reset the state of the ECU**: After terminating the transfer session, the ECU is reset to a normal state, ready to accept new requests, whether for further diagnostics, reprogramming, or calibration tasks.

The service is critical for maintaining the stability of the ECU after a large data transfer, and it should be issued after the last data block is successfully sent or received.

## **Overview of the Request Transfer Exit (0x37) Service**

The **Request Transfer Exit (0x37)** service does not require any specific data to be sent from the client, other than the **Service Identifier**. Its primary purpose is to signal the end of the transfer session. The service is typically used in conjunction with the **Transfer Data (0x36)** service, which is responsible for the actual data transmission.

Once the data transfer process is complete, the client sends the **Request Transfer Exit (0x37)** to inform the ECU that the session is finished. This service is important in scenarios where the client and ECU are transferring large files or multiple data blocks. Without this termination step, the transfer session could remain open, leading to potential errors, memory leaks, or resource contention.

## **Request Frame Format for Request Transfer Exit (0x37)**

The **Request Transfer Exit (0x37)** service has a simple request frame format. It consists of the **Service Identifier (SID)**, which is always **0x37**. There are no additional parameters or data required in the request frame.

| **Byte Number** | **Parameter Name**          | **Description**                                                      |
|-----------------|-----------------------------|----------------------------------------------------------------------|
| **1**           | **SID (Service Identifier)**| The **Service Identifier** for the **Request Transfer Exit** service, which is always **0x37**. |

This makes the **Request Transfer Exit** a very lightweight request that essentially serves as a signal to the ECU to close the data transfer session.

## **Response Frame Format for Request Transfer Exit (0x37)**

The ECU responds to the **Request Transfer Exit (0x37)** service with a **positive response** or a **negative response**, depending on whether the ECU successfully processes the termination request.

### **Positive Response**

If the ECU successfully terminates the data transfer session, it will respond with a **positive response** indicating that the session has been closed and resources have been freed.

| **Byte Number** | **Parameter Name**           | **Description**                                                                                       |
|-----------------|------------------------------|-------------------------------------------------------------------------------------------------------|
| **1**           | **PCI Length**                | Specifies the length of the response frame.                                                           |
| **2**           | **Response SID**              | The **Service Identifier** for the **Request Transfer Exit** response, which is **0x77** (0x37 + 0x40).|
| **3**           | **Transfer Exit Parameter**  | This field indicates any additional parameters related to the termination of the data transfer. In most cases, it is not used, but some implementations may include a success/failure flag. |

The **Response SID** will always be **0x77**, which is the **Service Identifier** for the **Request Transfer Exit** response. This is a direct match with the **Request Transfer Exit** service identifier **0x37**, with an offset of **0x40**.

### **Negative Response**

In the event that the ECU encounters an issue while attempting to terminate the transfer session (for example, if the session is already closed or the transfer process was incomplete), it will send a **negative response** with an appropriate **Negative Response Code (NRC)**.

| **Byte Number** | **Parameter Name**           | **Description**                                                                                       |
|-----------------|------------------------------|-------------------------------------------------------------------------------------------------------|
| **1**           | **PCI Length**                | Specifies the length of the response frame.                                                           |
| **2**           | **Request SID**               | The **Service Identifier** for the **Request Transfer Exit** service, which is **0x37**.              |
| **3**           | **NRC**                       | The **Negative Response Code (NRC)** indicating why the termination could not be completed.           |

### **Supported Negative Response Codes (NRC)**

| **NRC Value** | **Description**                                                | **Mnemonic** |
|---------------|----------------------------------------------------------------|--------------|
| **0x13**      | Incorrect message length or invalid format                    | IML          |
| **0x24**      | Request sequence error (e.g., attempting to exit when no transfer is active) | RSE          |
| **0x31**      | Request out of range (e.g., invalid session or data range)    | ROOR         |
| **0x33**      | Security access denied (e.g., lacking appropriate permissions) | SAD          |
| **0x70**      | General programming failure (e.g., failure to close the transfer session) | GPF          |

## **Transfer Exit Process**

1. **Completing the Transfer**: After all data blocks have been successfully transferred via the **Transfer Data (0x36)** service, the **Request Transfer Exit (0x37)** service is sent to signal the end of the data transfer session. This is a necessary step to properly conclude the transfer process.
   
2. **Server (ECU) Validation**: Upon receiving the **Request Transfer Exit** message, the ECU checks the status of the transfer session. If the session is still active and no issues are encountered, the ECU sends a **positive response** confirming the termination of the session.

3. **Error Handling**: If there was an error during the transfer process, or if the **Request Transfer Exit** is received prematurely (e.g., before the transfer is complete), the ECU will respond with a **negative response**, and the client may need to resend or handle the termination differently.

4. **Finalization**: Once the **Request Transfer Exit** has been processed, the ECU can free up any resources that were used during the transfer and prepare for other diagnostic, programming, or maintenance tasks.

---

## **Conclusion**

The **Request Transfer Exit (0x37)** service is essential for cleanly ending data transfer sessions between a client and an ECU in the **UDS protocol**. It ensures that resources are freed, and the ECU is prepared for further tasks after completing a data transfer, such as **Request Upload (0x35)** or **Request Download (0x34)**. This service is lightweight and easy to implement but is crucial for maintaining the integrity of the ECU’s operational state. The use of the **Transfer Data (0x36)** service in conjunction with **Request Transfer Exit** ensures a reliable and complete data exchange process, preventing errors and allowing the ECU to handle subsequent requests smoothly.