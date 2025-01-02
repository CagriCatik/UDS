---
sidebar_position: 7
---

# Examples - 0x23

Certainly! Below are the implementations of practical examples for **Read Memory by Address (0x23)**, including both the request and response formats. These examples demonstrate the usage of the service in real-world scenarios, where you would send a request to an ECU and receive a response.

## **Example 1: Reading ECU Firmware Version**

In this example, we will read a 4-byte firmware version stored at memory address `0x2000`. The requested memory length is 4 bytes, and we will simulate both a request and a response.

### **Request:**

The request asks the ECU to read 4 bytes starting from memory address `0x2000`. The service identifier `0x23` is used to invoke the **Read Memory by Address** service.

```python
# Request to Read Memory by Address from address 0x2000 for 4 bytes

# Service Identifier: 0x23 (Read Memory by Address)
service_id = 0x23

# Memory Address to Read: 0x2000 (4 bytes)
memory_address = [0x00, 0x00, 0x20, 0x00]

# Length of Data to Read: 4 bytes
length_to_read = [0x00, 0x04]

# Combine everything into the Request Message
request_message = [service_id] + memory_address + length_to_read

# Print the Request Message
print(f"Request Message: {request_message}")
```

### **Request Message Output:**

```plaintext
Request Message: [35, 0, 0, 32, 0, 0, 4]
```

Here, the request consists of:
- **Service Identifier (0x23)**: Indicates that the "Read Memory by Address" service is requested.
- **Memory Address (0x2000)**: Specifies the starting address to read from.
- **Length to Read (4 bytes)**: Specifies that we want to read 4 bytes of data from the starting address.

### **Response:**

After sending the request, the ECU responds with the requested memory data. In this example, let’s assume the firmware version stored at address `0x2000` is `0x01, 0x02, 0x03, 0x04` (a simple 4-byte version number).

```python
# Response from ECU after reading 4 bytes of memory
response_service_id = 0x23  # Response Service Identifier
memory_data = [0x01, 0x02, 0x03, 0x04]  # Data read from the memory
response_code = 0x00  # Positive Response Code (Success)

# Combine everything into the Response Message
response_message = [response_service_id] + memory_data + [response_code]

# Print the Response Message
print(f"Response Message: {response_message}")
```

### **Response Message Output:**

```plaintext
Response Message: [35, 1, 2, 3, 4, 0]
```

Here:
- **Service Identifier (0x23)**: Indicates that the response corresponds to the "Read Memory by Address" service.
- **Memory Data (0x01, 0x02, 0x03, 0x04)**: This is the 4-byte firmware version read from memory at address `0x2000`.
- **Response Code (0x00)**: Indicates a successful operation.

---

## **Example 2: Invalid Memory Address**

This example demonstrates what happens when an invalid memory address is requested. Let's say the ECU does not recognize the address `0xABCDE` (because it's out of range or invalid). The ECU will respond with a **Negative Response Code** (`0x31` - Request Out of Range).

### **Request:**

```python
# Request to Read Memory by Address from address 0xABCDE for 4 bytes

# Service Identifier: 0x23 (Read Memory by Address)
service_id = 0x23

# Invalid Memory Address: 0xABCDE (out of range)
memory_address = [0x0A, 0xBC, 0xDE, 0x00]

# Length of Data to Read: 4 bytes
length_to_read = [0x00, 0x04]

# Combine everything into the Request Message
request_message = [service_id] + memory_address + length_to_read

# Print the Request Message
print(f"Request Message: {request_message}")
```

### **Request Message Output:**

```plaintext
Request Message: [35, 10, 188, 222, 0, 0, 4]
```

Here, the request is attempting to read from the invalid address `0xABCDE`, and it specifies that 4 bytes should be read.

### **Response:**

Since the address is out of range, the ECU will return a **Negative Response Code** (`0x31`), indicating that the request cannot be processed due to the invalid address.

```python
# Response from ECU when memory address is out of range
response_service_id = 0x23  # Response Service Identifier
negative_response_code = 0x31  # Negative Response Code: Request Out of Range

# Combine everything into the Response Message
response_message = [response_service_id] + [negative_response_code]

# Print the Response Message
print(f"Response Message: {response_message}")
```

### **Response Message Output:**

```plaintext
Response Message: [35, 49]
```

Here:
- **Service Identifier (0x23)**: Indicates the service being invoked is **Read Memory by Address**.
- **Response Code (0x31)**: Indicates the request was out of range, meaning the memory address specified (`0xABCDE`) is invalid.

---

## **Example 3: Reading Memory with Security Access Denied**

In this example, the ECU requires security access to read the memory, and the diagnostic tool has not provided the correct credentials or access level. This results in a **Security Access Denied** response (`0x33`).

### **Request:**

```python
# Request to Read Memory by Address from address 0x3000 for 4 bytes (requires security access)

# Service Identifier: 0x23 (Read Memory by Address)
service_id = 0x23

# Memory Address: 0x3000 (4 bytes)
memory_address = [0x00, 0x00, 0x30, 0x00]

# Length of Data to Read: 4 bytes
length_to_read = [0x00, 0x04]

# Combine everything into the Request Message
request_message = [service_id] + memory_address + length_to_read

# Print the Request Message
print(f"Request Message: {request_message}")
```

### **Request Message Output:**

```plaintext
Request Message: [35, 0, 0, 48, 0, 0, 4]
```

Here, the diagnostic tool is attempting to read 4 bytes starting from memory address `0x3000`. However, security access is required to perform this operation.

### **Response:**

Since security access is not granted or provided, the ECU returns a **Negative Response Code** (`0x33` - Security Access Denied).

```python
# Response from ECU when security access is denied
response_service_id = 0x23  # Response Service Identifier
negative_response_code = 0x33  # Negative Response Code: Security Access Denied

# Combine everything into the Response Message
response_message = [response_service_id] + [negative_response_code]

# Print the Response Message
print(f"Response Message: {response_message}")
```

### **Response Message Output:**

```plaintext
Response Message: [35, 51]
```

Here:
- **Service Identifier (0x23)**: Indicates that the service being invoked is **Read Memory by Address**.
- **Response Code (0x33)**: Indicates that the ECU requires security access, and the access level provided by the diagnostic tool is insufficient.

---

## Conclusion

The **Read Memory by Address** service (0x23) is a powerful tool for accessing specific memory areas of an ECU. The examples provided here demonstrate typical usage scenarios, including reading memory, handling invalid addresses, and dealing with security access requirements.
