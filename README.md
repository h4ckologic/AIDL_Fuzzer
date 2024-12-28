# AIDL Fuzzer

The AIDL Fuzzer is a Python-based fuzzing tool that tests AIDL (Android Interface Definition Language) services for security vulnerabilities and robustness. It generates and executes various fuzzing commands by systematically manipulating method arguments and parcel types.

## Features
- Fuzzes AIDL services by systematically testing all parcel types and value combinations.
- Supports a wide range of parcel types such as integers, floating points, strings, booleans, arrays, and nested parcels.
- Logs all executed commands and their results for analysis.
- Handles errors such as timeouts and exceptions gracefully.
- Configurable parameters for maximum method codes and argument counts.

## Requirements
- Python 3.7 or higher
- Android Debug Bridge (ADB) installed and configured
- A connected Android device or emulator with debugging enabled

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/h4ckologic/AIDL_Fuzzer.git
   cd AIDL_Fuzzer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Command-Line Usage
To run the fuzzer, use the following command:
```bash
python aidl_fuzzer.py <service_name>
```

- `<service_name>`: The name of the AIDL service to fuzz.

Example:
```bash
python aidl_fuzzer.py android.hardware.audio.IAudioService
```

### Configurable Parameters
You can configure the following parameters in the `AIDLFuzzer` class:
- **`max_code`**: Maximum method code to fuzz (default: 1024).
- **`max_args`**: Maximum number of arguments per method (default: 5).

### Output
Logs will be saved in a file named `fuzzing_results.log` in the same directory as the script. This includes:
- Commands executed
- Command output
- Errors encountered during fuzzing

### Example Log Entry
```
2024-12-28 12:00:00 - INFO - Executing command: service call android.hardware.audio.IAudioService 42 i32 1 f 3.14
2024-12-28 12:00:01 - INFO - Command output: Result: Parcel(00000000 'NO_ERROR')
2024-12-28 12:00:10 - ERROR - Command timed out: service call android.hardware.audio.IAudioService 42 s16 "LongString"
```

## Code Structure
- **`FuzzingLogger`**: Handles logging of fuzzing activities.
- **`AIDLFuzzer`**: Main class responsible for generating fuzz commands, executing them, and handling results.
- **`generate_fuzz_commands`**: Generates all possible combinations of arguments for a given method code.
- **`execute_command`**: Executes a single fuzzing command via ADB and logs the results.
- **`start_fuzzing`**: Orchestrates the fuzzing process by iterating over method codes and argument combinations.

## Parcel Types and Values
The fuzzer supports the following parcel types and their respective values:
- **`i32`**: Various integers including edge cases (e.g., `0`, `-1`, `2147483647`, `-2147483648`)
- **`i64`**: Large integers and edge cases (e.g., `0`, `-1`, `9223372036854775807`)
- **`f`**: Floats including special cases (`NaN`, `Infinity`, `-Infinity`)
- **`d`**: Doubles with precision edge cases
- **`s16`**: Strings with special characters, long lengths, and edge cases
- **`bool`**: Boolean values (`True`, `False`)
- **`array`**: Arrays of various parcel types
- **`byte_buffer`**: Byte buffers with different contents
- **`nested_parcel`**: Nested parcels with multiple arguments

## Error Handling
- **Timeouts**: If a command execution exceeds 10 seconds, it is logged as a timeout error.
- **ADB Errors**: ADB-specific errors such as `OutOfMemoryError` are logged and categorized.

## Limitations
- Requires ADB and a connected Android device/emulator.
- Fuzzing coverage depends on the maximum method code and argument count configured.

## Contributing
Feel free to contribute by opening issues or submitting pull requests. Please ensure your contributions follow the existing code structure and include appropriate test cases.

## Acknowledgments
This tool was developed to aid in the security testing of AIDL services and is inspired by fuzzing methodologies for IPC services.

---

Happy Fuzzing!

