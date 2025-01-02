# Clear DTC Information - 0x14



## **1. Introduction**
The **Clear Diagnostic Information (Service 0x14)** is a key diagnostic service in the **Unified Diagnostic Services (UDS)** protocol. It allows a diagnostic tool (or client) to instruct the ECU (Electronic Control Unit) to erase Diagnostic Trouble Codes (DTCs) from its memory. Clearing DTCs is essential in ensuring that the vehicle’s diagnostic system accurately reflects the current status of its components, especially after a fault has been identified and repaired. This service, however, only clears the fault codes in the ECU’s memory and does not address the underlying issues that caused the faults.

In this documentation, we will explore the purpose, operation, response behaviors, potential issues, and examples of how **Service 0x14** works in real-world scenarios.

---

## **2. Purpose of Service 0x14: Clear Diagnostic Information**
The purpose of Service 0x14 is to remove **Diagnostic Trouble Codes (DTCs)** from the ECU's non-volatile memory (NVM) once the underlying issues causing the faults have been identified and rectified. This ensures that once a fault is fixed, it is no longer reported as an active issue.

Key points to note:
- **Service 0x14 clears DTCs**, which are stored diagnostic fault codes.
- It **does not fix** the issues that caused the DTCs. The underlying fault must be corrected first (e.g., fixing a faulty brake sensor before clearing a brake-related DTC).
- **Clearing DTCs helps maintain accurate vehicle diagnostic information**, preventing unnecessary fault indications and ensuring system health.

---

## **3. Supported Data Types for Clearing**
Service 0x14 can clear various types of diagnostic data stored in the ECU. These include:

- **DTC Status Byte**: Indicates the status of a DTC (active, pending, stored, etc.).
- **Snapshot Data**: Records the condition of the system when the fault occurred, such as temperature, speed, or pressure.
- **Extended Data**: Includes additional fault-specific data like first and most recent flags, counters, timers, etc.
- **Other DTC-Specific Data**: Other information tied to a particular DTC that is stored for diagnostics.

However, it is essential to note that **permanent DTCs**, which indicate unresolved or critical faults, cannot be cleared by Service 0x14. These are typically stored in non-volatile memory (NVM) and can only be cleared through specific reprogramming processes.

---

## **4. How Service 0x14 Works**
### **4.1 Request Frame Format**
The diagnostic tool sends a request frame to the ECU to clear specific DTCs. The request frame consists of the **Service ID (0x0x14)** followed by the DTC(s) to be cleared.

**Example Request Frame**:
```
0x14 A1 B2 C3
```
Where:
- `0x14`: Service ID for "Clear Diagnostic Information".
- `A1 B2 C3`: The DTCs to be cleared (in hexadecimal format).

The request frame can contain one or more DTCs. It may also request clearing all stored DTCs by sending a value like `FF FF FF` for all DTCs.

### **4.2 Response Frame Format**
Upon receiving the request, the ECU sends a response frame back to the diagnostic tool.

- **Positive Response**: If the DTCs are successfully cleared, the ECU sends a **positive response** (`54`).
  
  **Example Positive Response**:
  ```
  54
  ```

- **Negative Response**: If there is an error (such as an invalid DTC or unsupported request), the ECU sends a **negative response** with an appropriate **Negative Response Code (NRC)**.
  
  **Example Negative Response**:
  ```
  7F 0x14 31
  ```
  Where:
  - `7F`: Indicates a negative response.
  - `0x14`: Service ID for "Clear Diagnostic Information".
  - `31`: NRC for "Request Out of Range" (e.g., requesting DTCs that are not supported by the ECU).

---

## **5. Real-World Examples**
### **5.1 Example 1: Clearing a Specific DTC**
Consider a situation where a vehicle has a fault in the **brake system**, and the diagnostic tool identifies the DTC `A1 B2 C3` related to the brake failure. After fixing the underlying fault (e.g., replacing a faulty sensor), the technician can send the following request to clear the DTC:
```
0x14 A1 B2 C3
```

**Response**:
The ECU responds with `54`, indicating that the DTC has been successfully cleared.

### **5.2 Example 2: Clearing All DTCs**
In some cases, the technician may want to clear all stored DTCs after addressing multiple issues in the vehicle. The request frame would be:
```
0x14 FF FF FF
```

**Response**:
The ECU responds with `54`, indicating that all stored DTCs have been cleared.

---

## **6. Limitations of Service 0x14**
While **Service 0x14** is useful for clearing DTCs, it is crucial to understand its limitations:

### **6.1 Permanent DTCs**
Some faults are **permanent** and are stored in **non-volatile memory (NVM)**. These DTCs cannot be cleared by Service 0x14 unless the issue is resolved and, in some cases, the ECU needs to be **reprogrammed**.

- **Example**: A serious engine fault (e.g., a failed fuel injector) may trigger a permanent DTC. Even if the DTC is cleared using Service 0x14, it may reappear unless the fault is corrected.

### **6.2 Mirror Memory**
ECUs often store DTCs in **mirror memory** for historical reference. This memory stores duplicate copies of the DTCs (one in RAM and one in EEPROM). When Service 0x14 is used to clear the DTC, the **original memory** (e.g., EEPROM) is cleared, but the **mirror memory** in RAM may still retain the fault data until explicitly cleared.

- **Example**: If a DTC `A1 B2 C3` is cleared from the EEPROM memory, the mirror memory in RAM may still contain the DTC until another diagnostic operation clears it.

### **6.3 Power Interruptions**
If there is a power interruption (e.g., the vehicle battery is disconnected) during the clearing process, it may prevent the DTCs from being cleared correctly. In such cases, the ECU may need to be reinitialized or the process retried.

- **Example**: If the technician sends the request to clear DTCs but disconnects the battery during the process, the ECU may not clear the DTCs. Once the power is restored, the fault may still be present in memory.

---

## **7. Negative Responses and Errors**
If there are issues with the request or if the DTC is unsupported, the ECU will respond with a **Negative Response Code (NRC)**.

### **Common NRCs in Service 0x14**:
- **31 (Request Out of Range)**: This occurs when the diagnostic tool requests a DTC that is outside the range supported by the ECU.
  - **Example**: Requesting DTCs that do not exist or are outside the acceptable range.

- **72 (General Programming Failure)**: This error occurs if there is an issue while attempting to erase a DTC.
  - **Example**: Attempting to clear a DTC that cannot be erased due to a hardware issue or memory failure.

---

## **8. Best Practices for Clearing DTCs**
To effectively use **Service 0x14**, follow these best practices:
1. **Fix the Fault First**: Always ensure the underlying fault has been fixed before clearing the DTCs. Simply clearing the DTC without fixing the issue will not resolve the problem and may result in inaccurate diagnostics.
   
2. **Clear Mirror Memory**: Be aware that **mirror memory** may not be automatically cleared. If necessary, use other diagnostic services to clear the mirror memory.

3. **Avoid Power Interruptions**: Minimize the risk of power loss during the clearing process to ensure that DTCs are successfully removed.

4. **Check for Permanent DTCs**: If the DTC is permanent, it may require ECU reprogramming or further corrective actions to be fully cleared.

---

## **9. Conclusion**
Service 0x14, **Clear Diagnostic Information**, is a powerful tool in the UDS protocol for clearing DTCs after resolving vehicle faults. It is crucial for maintaining accurate diagnostic information and ensuring the vehicle’s systems are properly monitored. However, it is not a repair tool and does not address the root causes of the faults. By understanding the service's capabilities, limitations, and correct usage, technicians can ensure that the vehicle’s diagnostic system remains accurate and functional.

 