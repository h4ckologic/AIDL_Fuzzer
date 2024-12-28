import itertools
import subprocess
import sys
import logging
from typing import Generator


class FuzzingLogger:
    def _init_(self, log_file: str = 'fuzzing_results.log'):
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(_name_)

    def log(self, level: str, message: str):
        log_method = getattr(self.logger, level, self.logger.info)
        log_method(message)


class AIDLFuzzer:
    def _init_(self, service_name: str, max_code: int = 1024, max_args: int = 5):
        self.service_name = service_name
        self.max_code = max_code
        self.max_args = max_args
        self.logger = FuzzingLogger()
        self.parcels = {
            "i32": [1, 0, 65535, 0xfffffffe, 0xffffffff, -1, 2147483647, -2147483648, 123, 456, -789],
            "i64": [0xfffffffffffffffe, 0xffffffffffffffff, 1, 0, -1, 9223372036854775807, -9223372036854775808, 9876543210, -1234567890],
            "f": [-1.0, 3.141592, 1.0, 0.0, float('inf'), float('-inf'), float('nan'), 1.23, -4.56],
            "d": [0xff, 0xfffffffe, -1.0, 3.141592653589793, 1.0, 0.0, float('inf'), float('-inf'), float('nan'), 2.718281828459045, -3.141592653589793],
            "s16": ["3%%n%%x%%s%s%%n1", "A"10, "A "*4, "\xff\xfff\xff\xff\xff\xff\xff\xff\xfc", "", "NormalString", "\uFFFF"*10, "SpecialChars!@#$%^&()", "LongString"*10],
            "bool": [True, False],
            "array": ["i32 1 2 3", "i64 1 2 3", "f 1.0 2.0 3.0", "d 1.0 2.0 3.0", "s16 'A' 'B' 'C'", "bool true false"],
            "byte_buffer": ["ByteBuffer.wrap(new byte[]{1, 2, 3})", "ByteBuffer.wrap(new byte[]{})", "ByteBuffer.wrap(new byte[]{0x00, 0x7F, (byte)0x80, (byte)0xFF})"],
            "nested_parcel": ["i32 1 s16 'Nested String'", "d 2.718 array 'i32 4 5 6'"]
        }

    def generate_fuzz_commands(self, code: int, args_count: int) -> Generator[str, None, None]:
        args_schemas = itertools.combinations_with_replacement(self.parcels.keys(), args_count)
        for args_schema in args_schemas:
            for arg_values in itertools.product(*(self.parcels[arg_type] for arg_type in args_schema)):
                str_args = " ".join(f"{arg_type} {arg_value}" for arg_type, arg_value in zip(args_schema, arg_values))
                yield f"service call {self.service_name} {code} {str_args}"

    def execute_command(self, command: str):
        self.logger.log('info', f"Executing command: {command}")
        try:
            result = subprocess.run(['adb', 'shell', command],
                                    check=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True,
                                    timeout=10)
            self.logger.log('info', f"Command output: {result.stdout}")
        except subprocess.TimeoutExpired:
            self.logger.log('error', f"Command timed out: {command}")
        except subprocess.CalledProcessError as e:
            self.logger.log('error', f"Error executing command: {e.stderr}")
            if 'OutOfMemoryError' in e.stderr:
                self.logger.log('critical', f"OutOfMemoryError encountered: {e.stderr}")

    def start_fuzzing(self):
        for code in range(1, self.max_code + 1):
            for args_count in range(1, self.max_args + 1):
                for fuzz_command in self.generate_fuzz_commands(code, args_count):
                    self.execute_command(fuzz_command)


if _name_ == "_main_":
    if len(sys.argv) > 1:
        service_name = sys.argv[1]
        fuzzer = AIDLFuzzer(service_name)
        fuzzer.start_fuzzing()
    else:
        print(f"Usage: {sys.argv[0]} <service_name>")