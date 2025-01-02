---
sidebar_position: 11
---

# Read Scaling Data by Identifier - 0x24

## Introduction to Scaling Data

In automotive diagnostics, scaling data refers to a set of parameters or constants used to convert raw sensor data (often in analog form) into meaningful digital values. Sensors in vehicles generate raw signals, such as voltage levels or current readings, which are typically used to represent physical quantities like temperature, pressure, speed, or other environmental factors. To interpret these values correctly, a scaling process is applied to convert them into their actual physical representations.

For instance, an analog sensor might output a voltage value that corresponds to a temperature range, but in order to convert that raw voltage into a usable temperature value (e.g., in degrees Celsius or Fahrenheit), a scaling formula is required. This formula might involve constants that adjust the raw data to reflect accurate measurements.

The Read Scaling Data by Identifier service (Service 0x24) in the Unified Diagnostic Services (UDS) protocol is used to retrieve the scaling data associated with a specific data identifier (DID). This allows the diagnostic tool to understand how raw sensor data should be interpreted and scaled into meaningful values.

## Service Overview

- Service ID (SID): 0x24
- Service Name: Read Scaling Data by Identifier
- Purpose: Retrieves the scaling data for a specific data identifier (DID) from an ECU.
- Response IDs:
  - Positive Response ID (SID 0x64): Contains the scaling data for the requested identifier.
  - Negative Response ID (SID 0x7F): Indicates errors, such as when the requested scaling data is unavailable.

This service is crucial in situations where the diagnostic tool needs to interpret sensor data or other types of information in a standard way, based on predefined scaling rules.

## Request and Response Structure

### Request Format (Client to Server)

When the client (e.g., a diagnostic tool) sends a request to the ECU, it must include the Service ID (SID) 0x24, followed by the Data Identifier (DID) that corresponds to the data whose scaling information is needed.

Example of a Request Frame:
```
0x24 0xF1 0x90
```
- 0x24: Service ID (Read Scaling Data by Identifier)
- 0xF1 0x90: Data Identifier (DID), which represents the specific data record in the ECU whose scaling information is being requested.

### Positive Response Format (Server to Client)

If the ECU has successfully retrieved the scaling data for the requested identifier, it will return a positive response. The response includes the Service ID (SID) 0x64 and the scaling data associated with the DID.

Example of a Positive Response Frame:
```
0x64 0xF1 0x90 0x6F 0x62
```
- 0x64: Response ID (indicating a positive response).
- 0xF1 0x90: The Data Identifier (DID) echoing back the requested data.
- 0x6F 0x62: The scaling data, which includes key information about the scaling factors used for the given DID.

### Negative Response Format (Server to Client)

If the ECU cannot provide the requested scaling data, it will return a negative response. This typically occurs if the scaling data does not exist for the requested DID or if the conditions for the request are not met.

Example of a Negative Response Frame:
```
0x7F 0x24 0x22
```
- 0x7F: Response ID (indicating a negative response).
- 0x24: The original Service ID (Read Scaling Data by Identifier).
- 0x22: Negative Response Code, indicating that the condition for retrieving the scaling data was not correct (e.g., the data identifier does not support scaling).

## Understanding Scaling Data

The scaling data returned in the response provides the constants or rules used to convert raw data into usable values. Typically, the scaling data will indicate:
1. Data Type: Whether the data is stored as an ASCII string, binary value, or other types.
2. Scaling Factors: Constants or factors that help scale or convert the raw data.
3. Data Length: The size of the data (in bytes) and the total number of data bytes involved.

### Example of Scaling Data Interpretation

In the following example, the scaling data returned is 0x6F 0x62:

```
Scaling Data: 0x6F 0x62
```

Interpretation:
- 0x6F:
  - 6: Indicates that the value is in ASCII format.
  - F: Represents the total number of bytes, which is 15 bytes in this case (this could be for a VIN or a similar string of data).
  
- 0x62:
  - 6: Again, indicates that the value is ASCII.
  - 2: Refers to 2 leftover bytes, representing the remaining portion of the VIN (or a similar string), indicating that the total length is 15 bytes, and 2 bytes are allocated here.

Thus, this scaling data suggests that the VIN (Vehicle Identification Number) is stored as an ASCII string of 15 bytes.

## Examples of Practical Scenarios

### Scenario 1: Requesting Scaling Data for Sensor Values

A vehicle diagnostic tool requests the scaling data for an engine temperature sensor. The scaling data could define how the raw sensor voltage values (e.g., between 0V and 5V) are mapped to temperature values (e.g., between -40°C and 150°C).

- Request:
  ```
  0x24 0xF2 0xA1
  ```
- Response:
  ```
  0x64 0xF2 0xA1 0x6F 0x65
  ```

In this case, the scaling data indicates that the sensor value is represented in ASCII format, with specific scaling factors (e.g., the voltage-to-temperature mapping) provided in the following bytes.

### Scenario 2: Error Condition when Scaling Data is Unavailable

If the client requests scaling data for a calibration date data identifier that does not have any scaling data associated with it, the ECU might return a negative response.

- Request:
  ```
  0x24 0xF3 0xA2
  ```

- Response:
  ```
  0x7F 0x24 0x22
  ```

Here, 0x22 indicates the error "Condition Not Correct", which implies that no scaling data is available for the requested data identifier.

## Best Practices in Using Read Scaling Data by Identifier

1. Data Validation: Before requesting scaling data, ensure that the Data Identifier (DID) corresponds to a valid data type for scaling. Not all DIDs will have scaling data.
  
2. Interpretation of Scaling Data: Be sure to properly interpret the scaling data based on the provided format (e.g., ASCII, binary) and understand how it relates to the raw sensor data.

3. Handling Errors: Implement robust error handling for situations where scaling data is not available or when negative responses are returned. This might involve retrying with a different DID or handling specific error codes (e.g., 0x22).

4. Standardization of Units: When scaling data is used to convert physical quantities, ensure that the diagnostic tool or system is aware of the scaling constants and unit conversions required to properly interpret the data.

## Conclusion

The Read Scaling Data by Identifier service (0x24) is a key diagnostic service in UDS that enables the retrieval of scaling data associated with specific identifiers. By understanding and applying scaling factors, diagnostic tools can convert raw sensor data into meaningful physical measurements. This service is crucial for interpreting vehicle data in standard formats, allowing for proper diagnostics and vehicle maintenance. Proper understanding and implementation of this service is essential for developers and engineers working with automotive ECUs and diagnostic systems.