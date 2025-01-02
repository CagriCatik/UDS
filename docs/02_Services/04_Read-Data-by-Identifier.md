---
sidebar_position: 4
---

# Read Data By Identifier - 0x22

## Introduction

The **Read Data By Identifier** (RDBI) service, identified by **0x22**, is an integral part of the **Unified Diagnostic Services (UDS)** protocol, which is outlined in **ISO 14229**. This service is used to request specific data from an ECU (Electronic Control Unit) by providing an identifier corresponding to the desired data or parameter. The ability to read data from the ECU is crucial for diagnostics, vehicle maintenance, ECU calibration, and software validation.

The service allows for the retrieval of various data types, such as:
- **ECU Software Version**
- **Calibration Parameters**
- **Sensor Data** (e.g., engine temperature, fuel pressure)
- **Vehicle Performance Metrics** (e.g., speed, RPM)

### Purpose and Importance of RDBI

The RDBI service plays a vital role in the automotive and ECU development lifecycle. It enables service technicians, engineers, and diagnostic tools to access critical data that supports:
- ECU parameter monitoring during development and testing.
- Firmware and software version validation.
- Real-time data monitoring during in-service diagnostics and troubleshooting.

---

### 2. "Read Data By Identifier" Service (0x22)

The **Read Data By Identifier (0x22)** service is one of the core diagnostic services defined by the UDS protocol. It allows diagnostic tools to request specific pieces of data from the ECU by sending a **Data Identifier**. This identifier indicates the data or parameter to be retrieved.

#### 2.1. Service Flow

1. **Service Request**:
   - A diagnostic tool sends a request to the ECU with the service identifier (`0x22`) and a **Data Identifier**. 
   - The **Data Identifier** specifies the exact data or parameter the tool wants to retrieve.
  
2. **Service Response**:
   - The ECU responds with the requested data or a **Negative Response** if the request cannot be processed.
  
   **Success Response**: The ECU sends the requested data.
   **Negative Response**: If the ECU cannot fulfill the request, an error code is returned, such as when the identifier is unsupported.

#### 2.2. Request Format

The format of the request message is as follows:

| Byte Position | Field             | Description                                              |
|---------------|-------------------|----------------------------------------------------------|
| 1             | Service ID        | Always `0x22` for **Read Data By Identifier**.           |
| 2 and beyond  | Data Identifier   | The identifier for the data to be read from the ECU. This can be one or more bytes. |

Example Request for Software Version (identifier `0x01`):

```
0x22 0x01
```

Where:
- `0x22` is the service ID for **Read Data By Identifier**.
- `0x01` is the identifier for the **Software Version**.

Example Request for Vehicle Speed (identifier `0x02`):

```
0x22 0x02
```

Where:
- `0x22` is the service ID for **Read Data By Identifier**.
- `0x02` is the identifier for the **Vehicle Speed**.

#### 2.3. Response Format

The format of the response message is as follows:

| Byte Position | Field             | Description                                               |
|---------------|-------------------|-----------------------------------------------------------|
| 1             | Service ID        | Always `0x62` for the response to **Read Data By Identifier**. |
| 2             | Data Identifier   | The identifier that corresponds to the requested data.    |
| 3 and beyond  | Data              | The actual data corresponding to the requested identifier. |
| Optional      | Negative Response | If the ECU cannot fulfill the request, an error code is returned. |

##### 2.3.1. Example Response 1: Software Version

If the requested **identifier** is `0x01` (software version), the ECU might respond as follows:

Request:

```
0x22 0x01
```

Response:

```
0x62 0x01 0x01 0x00 0x02 0x03
```

Where:
- `0x62` is the response service ID, indicating a successful **Read Data By Identifier**.
- `0x01` is the identifier for the software version.
- `0x01 0x00 0x02 0x03` represents the software version, which could correspond to version `1.0.2.3`.

##### 2.3.2. Example Response 2: Vehicle Speed

If the requested **identifier** is `0x02` (vehicle speed), the ECU might respond as follows:

Request:

```
0x22 0x02
```

Response:

```
0x62 0x02 0x00 0x64
```

Where:
- `0x62` is the response service ID.
- `0x02` is the identifier for the vehicle speed.
- `0x00 0x64` represents the vehicle speed in hexadecimal (`0x64` = `100` km/h in decimal).

##### 2.3.3. Negative Response Example

If the ECU doesn't support the requested identifier (e.g., `0x99`), it may return a **Negative Response** indicating an error.

Request:

```
0x22 0x99
```

Response:

```
0x7F 0x22 0x11
```

Where:
- `0x7F` indicates a **Negative Response**.
- `0x22` is the service ID for **Read Data By Identifier**.
- `0x11` is the error code, which could indicate "Service Not Supported" or "Data Identifier Not Available."

---

### 3. Data Identifiers

In UDS, each piece of data or parameter within an ECU is identified by a **Data Identifier**. These identifiers are unique for each data point and can be either **standardized** or **manufacturer-specific**.

#### 3.1. Standardized Identifiers

ISO 14229 defines a set of **standardized data identifiers** for commonly accessed parameters. Some examples include:

| Data Identifier | Description                              |
|-----------------|------------------------------------------|
| `0x01`          | ECU Software Version                     |
| `0x02`          | Vehicle Speed                            |
| `0x03`          | Engine RPM                               |
| `0x04`          | Coolant Temperature                      |
| `0x05`          | Fuel Pressure                            |
| `0x06`          | Airbag Status                            |
| `0x07`          | Battery Voltage                          |

These identifiers are consistent across different vehicle makes and models and can be used for general diagnostic purposes.

#### 3.2. Manufacturer-Specific Identifiers

In addition to the standardized identifiers, many manufacturers define their own proprietary data identifiers for specialized parameters. These may relate to calibration data, diagnostic logs, or specific performance metrics for certain ECUs or vehicle models.

For example:
- `0xF1A1` might represent **Vehicle Configuration Data** specific to a manufacturer.
- `0xF1A2` could represent **Proprietary Calibration Data** for an ECU model.

Since these identifiers are not standardized, they typically require specific knowledge of the manufacturer's documentation or the ECU’s Diagnostic Information Database (DID) to decode.

---

### 4. Applications and Use Cases

The **Read Data By Identifier** service has numerous applications in vehicle diagnostics, testing, and ECU development.

#### 4.1. Vehicle Diagnostics

- **Retrieving Diagnostic Trouble Codes (DTCs)**: RDBI can be used to access fault codes from the ECU, which can assist technicians in troubleshooting vehicle issues.
- **Real-Time Monitoring**: The service can also be used to monitor live data, such as coolant temperature, engine RPM, and tire pressure, to assess vehicle performance in real-time.

**Example**: Retrieve coolant temperature (identifier `0x04`):

Request:

```
0x22 0x04
```

Response:

```
0x62 0x04 0x01 0x10  // 16°C
```

#### 4.2. ECU Software and Configuration Updates

- **Validating ECU Software Versions**: Before performing an ECU reprogramming or update, it is important to retrieve the current software version to ensure compatibility.
- **Calibration Verification**: RDBI can be used to verify calibration data before or after an ECU reprogramming.

**Example**: Retrieve the ECU's software version before an update (identifier `0x01`):

Request:

```
0x22 0x01
```

Response:

```
0x62 0x01 0x01 0x00 0x02 0x03  // Version: 1.0.2.3
```

#### 4.3. Real-Time Data Access

RDBI is used for accessing real-time data during dynamic testing, where parameters such as **vehicle speed**, **engine RPM**, or sensor data are needed for live vehicle assessments.

**Example**: Retrieve real-time vehicle speed (identifier `0x02`):

Request:

```
0x22 0x02
```

Response:

```
0x62 0x02 0x00 0x64  // Vehicle Speed = 100 km/h
```

---

### 5. Error Handling

Error handling is a critical aspect of using the **Read Data By Identifier** service. Various **Negative Response Codes** are defined to indicate different types of errors that may occur during communication.

#### 5.1. Common Negative Response Codes

| Error Code | Description                                      |
|------------|------------------------------------------------

--|
| `0x11`     | Service Not Supported                            |
| `0x12`     | Sub-function Not Supported                       |
| `0x22`     | Conditions Not Correct                          |
| `0x24`     | Request Out of Range                             |
| `0x31`     | Incorrect Identifier                            |
| `0x7F`     | General Reject (any other undefined error)      |

For example, if a **Negative Response** is received with the code `0x11`, it indicates that the requested data identifier is not supported by the ECU.

---

### 6. Conclusion

The **Read Data By Identifier** (0x22) service is a powerful tool for retrieving specific data from ECUs, whether for real-time diagnostics, software validation, or testing. By utilizing the correct **Data Identifiers**, users can access a wide range of parameters that aid in vehicle maintenance, calibration, and performance monitoring. This service plays a critical role in the overall **Unified Diagnostic Services (UDS)** protocol, ensuring that vehicle and ECU diagnostics remain efficient and accurate.

