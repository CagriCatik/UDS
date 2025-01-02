# Log File Handling

---

## Overview

Log File Handling in CAPL ensures that diagnostic data and test results are stored persistently for future analysis and traceability. This approach complements the trace window, which provides real-time feedback but lacks the permanence needed for detailed reporting or debugging.

---

## Purpose

1. Persistence: Store critical information about communication events, responses, and errors in a retrievable format.
2. Debugging: Enable detailed post-test analysis of diagnostic sessions.
3. Traceability: Create logs for compliance, auditing, or long-term records.

---

## How It Works

CAPL provides the `writeToLog` function to log messages into a file. You can define the log file's name, format the log content, and include dynamic values (e.g., message IDs, service identifiers, and timestamps).

---

## Implementation

### 1. Basic Log Example

```capl
on message 0x1E8 { // Assuming 0x1E8 is the ECU response ID
  writeToLog("logfile.txt", "Response received: ID=0x1E8, Byte1=0x%X, Byte2=0x%X", this.byte(1), this.byte(2));
}
```

Explanation:
- `logfile.txt`: Specifies the file name where logs will be stored.
- `"Response received: ID=0x1E8, Byte1=0x%X, Byte2=0x%X"`: The log message with placeholders for dynamic data.
- `this.byte(1)` and `this.byte(2)`: Data extracted from the incoming message.

---

### 2. Log with Timestamps

To include timestamps for each logged event:

```capl
variables {
  char timeStr[20];
}

on message 0x1E8 {
  getSystemTimeStr(timeStr);
  writeToLog("logfile.txt", "[%s] Response: ID=0x1E8, Byte1=0x%X, Byte2=0x%X", timeStr, this.byte(1), this.byte(2));
}
```

Explanation:
- `getSystemTimeStr(timeStr)`: Retrieves the current system time as a string.
- `[%s]`: Formats the timestamp into the log entry.

---

### 3. Log for Specific Events

Use conditional statements to log only specific types of responses (e.g., Negative Response Codes - NRC).

```capl
on message 0x1E8 {
  if (this.byte(1) == 0x7F) { // Check for Negative Response
    int nrc = this.byte(2);  // Extract the NRC
    writeToLog("logfile.txt", "NRC received: 0x%X for Service: 0x%X", nrc, this.byte(1));
  } else {
    writeToLog("logfile.txt", "Positive Response received for Service: 0x%X", this.byte(1));
  }
}
```

Explanation:
- Filters and logs only negative or positive responses for diagnostic clarity.

---

### 4. Cyclic Logging

To log data periodically, use a timer:

```capl
variables {
  char timeStr[20];
}

on timer logTimer {
  getSystemTimeStr(timeStr);
  writeToLog("logfile.txt", "[%s] Cyclic Event: Tester Present Sent", timeStr);
}

on start {
  setTimerCyclic("logTimer", 2000); // Log every 2 seconds
}

on stop {
  cancelTimer("logTimer");
}
```

Explanation:
- A cyclic timer ensures periodic entries in the log file.
- Useful for monitoring recurring events like Tester Present requests.

---

## Best Practices

1. Organize Log Files:
   - Use distinct file names for each session (e.g., `session_<timestamp>.txt`).
   - Separate log files for different services or modules.

2. Include Contextual Information:
   - Log relevant message IDs, bytes, and timestamps.
   - Provide meaningful descriptions (e.g., "Service 0x10: Programming Session Started").

3. Error Management:
   - Highlight errors or unexpected events using tags like `[ERROR]` or `[WARNING]`.

4. Log Rotation:
   - Implement log rotation to manage file sizes and prevent overwriting.

---

## Benefits

- Traceability: Ensures that all diagnostic interactions are recorded for compliance or debugging.
- Debugging Efficiency: Logs provide granular details that simplify issue resolution.
- Automated Analysis: Log files can be parsed programmatically to generate reports or identify anomalies.

---

## Use Case Example

Scenario: Logging the Tester Present service's activity along with timestamps.

Implementation:

```capl
variables {
  char timeStr[20];
  message testerPresentMessage;
}

on start {
  // Initialize Tester Present Message
  testerPresentMessage.id = 0x1E0;
  testerPresentMessage.dlc = 8;
  testerPresentMessage.byte(0) = 0x02;
  testerPresentMessage.byte(1) = 0x3E;
  testerPresentMessage.byte(2) = 0x00;

  setTimerCyclic("testerPresentLogTimer", 2000); // Log every 2 seconds
}

on timer testerPresentLogTimer {
  getSystemTimeStr(timeStr);
  writeToLog("logfile.txt", "[%s] Tester Present sent: ID=0x1E0", timeStr);
  output(testerPresentMessage);
}

on stop {
  cancelTimer("testerPresentLogTimer");
}
```

Expected Log Output:

```
[2025-01-01 10:00:00] Tester Present sent: ID=0x1E0
[2025-01-01 10:00:02] Tester Present sent: ID=0x1E0
[2025-01-01 10:00:04] Tester Present sent: ID=0x1E0
```

---

## Conclusion

Log File Handling in CAPL enhances the traceability, debugging, and analysis of UDS diagnostic sessions. By implementing structured, timestamped logs, you can ensure a robust and efficient testing workflow.