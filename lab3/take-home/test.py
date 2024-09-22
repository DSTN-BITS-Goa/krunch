import os
import unittest
import subprocess
import shutil

class TestMyFS(unittest.TestCase):
    mount_dir_template = 'mount_tc{}'  # Relative path from the build directory
    root_dir_template = 'root_tc{}'  # Relative path from the build directory
    log_file_template = 'logs/myfs_tc{}.log'  # Relative path from the build directory
    expected_output_dir = '../expected_logs'  # Relative path from the build directory


    def run_myfs(self, testcase_number, additional_args=[]):
        """Run the myfs command to mount the FUSE filesystem."""
        command = ["./myfs", self.mount_dir_template.format(testcase_number), self.log_file_template.format(testcase_number), self.root_dir_template.format(testcase_number)] + additional_args
        subprocess.run(command, check=True)

    def run_test_case(self, operations, testcase_number, additional_args=[]):
        """Runs a test case with specified operations."""
        self.run_myfs(testcase_number, additional_args)  # Start the FUSE filesystem

        for operation in operations:
            try:
                if operation['type'] == 'create':
                    self._create_file(testcase_number, operation['name'])
                    print(f"Created file: {operation['name']}")
                elif operation['type'] == 'read':
                    self._read_file(testcase_number, operation['name'], operation['offset'], operation['length'])
                    print(f"Read file: {operation['name']}")
                elif operation['type'] == 'write':
                    self._write_file(testcase_number, operation['name'], operation['content'])
                    print(f"Wrote to file: {operation['name']}")
                elif operation['type'] == 'delete':
                    self._delete_file(testcase_number, operation['name'])
                    print(f"Deleted file: {operation['name']}")
            except Exception as e:
                print(f"Error during '{operation['type']}' operation on '{operation['name']}' in test case {testcase_number}: {e}")
                continue


        self._compare_logs(testcase_number)

    def _create_file(self, testcase_number, name):
        """Create an empty file."""
        try:
            open(os.path.join(self.mount_dir_template.format(testcase_number), name), 'a').close()  # Create an empty file
        except Exception as e:
            print(f"Failed to create file '{name}' in test case {testcase_number}: {e}")
            # Continue without stopping

    def _read_file(self, testcase_number, name, offset, length):
        """Read a portion of a file at a given offset."""
        try:
            # Open the file
            filepath = os.path.join(self.mount_dir_template.format(testcase_number), name)
            fd = os.open(filepath, os.O_RDONLY)

            # Use os.pread to read from the specified offset
            data = os.pread(fd, length, offset)

            # Close the file descriptor
            os.close(fd)

        except Exception as e:
            print(f"Failed to read file '{name}' in test case {testcase_number}: {e}")

    def _write_file(self, testcase_number, name, content):
        """Write content to an existing file and flush changes immediately using O_SYNC."""
        try:
            file_path = os.path.join(self.mount_dir_template.format(testcase_number), name)
            fd = os.open(file_path, os.O_WRONLY | os.O_APPEND | os.O_SYNC)
            os.write(fd, content.encode())  # os.write requires bytes, hence encode content
            os.close(fd)
        except Exception as e:
            print(f"Failed to write to file '{name}' in test case {testcase_number}: {e}")

    def _delete_file(self, testcase_number, name):
        """Delete a file."""
        try:
            os.remove(os.path.join(self.mount_dir_template.format(testcase_number), name))
        except Exception as e:
            print(f"Failed to delete file '{name}' in test case {testcase_number}: {e}")
            # Continue without stopping


    def _compare_logs(self, testcase_number):
        """Compare the generated log file with the expected log."""
        log_file = self.log_file_template.format(testcase_number)
        expected_log_file = os.path.join(self.expected_output_dir, f'expected_tc{testcase_number}.log')

        with open(log_file, 'r') as log, open(expected_log_file, 'r') as expected:
            log_contents = log.read().strip()
            expected_contents = expected.read().strip()
            self.assertEqual(log_contents, expected_contents)

    def test_case1(self):
        operations = [
            {'type': 'create', 'name': 'file1.txt'},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!'},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},
            {'type': 'delete', 'name': 'file1.txt'}
        ]
        additional_args = ["4", "8", "16"]  # Example additional arguments for myfs
        self.run_test_case(operations, 1, additional_args)

    def test_case2(self):
        operations = [
            {'type': 'create', 'name': 'file2.txt'},
            {'type': 'create', 'name': 'file3.txt'},
            {'type': 'create', 'name': 'file4.txt'},
            {'type': 'write', 'name': 'file2.txt', 'content': 'Welcome!'},
            {'type': 'read', 'name': 'file2.txt', "offset": 0, "length": 1024},
            {'type': 'write', 'name': 'file2.txt', 'content': 'Welcome!'},
            {'type': 'write', 'name': 'file3.txt', 'content': 'Welcome!'},
            {'type': 'read', 'name': 'file2.txt', "offset": 0, "length": 1024},
            {'type': 'delete', 'name': 'file2.txt'},
            {'type': 'write', 'name': 'file3.txt', 'content': 'Welcome!'},
        ]
        additional_args = ["2", "3", "6"]  # Different arguments for this test case
        self.run_test_case(operations, 2, additional_args)

    def test_case3(self):
        operations = [
            {'type': 'create', 'name': 'file5.txt'},
            {'type': 'write', 'name': 'file5.txt', 'content': 'Hello!'},
            {'type': 'read', 'name': 'file5.txt', 'offset': 0, 'length': 1024},
            {'type': 'create', 'name': 'file6.txt'},
            {'type': 'write', 'name': 'file6.txt', 'content': 'Testing!'},
            {'type': 'read', 'name': 'file6.txt', 'offset': 0, 'length': 1024},
            {'type': 'delete', 'name': 'file6.txt'}
        ]
        additional_args = ["5", "10", "8"]
        self.run_test_case(operations, 3, additional_args)

    def test_case4(self):
        operations = [
            {'type': 'create', 'name': 'file7.txt'},
            {'type': 'write', 'name': 'file7.txt', 'content': 'Data Testing!'},
            {'type': 'read', 'name': 'file7.txt', 'offset': 0, 'length': 1024},
            {'type': 'create', 'name': 'file8.txt'},
            {'type': 'write', 'name': 'file8.txt', 'content': 'Another Test!'},
            {'type': 'read', 'name': 'file8.txt', 'offset': 0, 'length': 1024},
            {'type': 'write', 'name': 'file7.txt', 'content': 'Append More Data'},
            {'type': 'delete', 'name': 'file7.txt'},
            {'type': 'delete', 'name': 'file8.txt'}
        ]
        additional_args = ["3", "5", "12"]
        self.run_test_case(operations, 4, additional_args)

    def test_case5(self):
        operations = [
            {'type': 'create', 'name': 'file1.txt'},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Sequential Read Test!'},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Add New Info'},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},
            {'type': 'create', 'name': 'file2.txt'},
            {'type': 'write', 'name': 'file2.txt', 'content': 'Another Sample!'},
            {'type': 'delete', 'name': 'file1.txt'},
        ]
        additional_args = ["3", "5", "4"]  # Example: num_inodes=3, num_data_blocks=5, data_block_size=8
        self.run_test_case(operations, 5, additional_args)

    def test_case6(self):
        operations = [
            {'type': 'create', 'name': 'file1.txt'},
            {'type': 'write', 'name': 'file1.txt', 'content': 'ABcdefg'},
            {'type': 'create', 'name': 'file2.txt'},
            {'type': 'write', 'name': 'file2.txt', 'content': 'CDabc'},
            {'type': 'create', 'name': 'file3.txt'},
            {'type': 'write', 'name': 'file3.txt', 'content': 'EF'},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},
            {'type': 'read', 'name': 'file3.txt', 'offset': 0, 'length': 1024},
            {'type': 'delete', 'name': 'file1.txt'},
            {'type': 'delete', 'name': 'file3.txt'}
        ]
        additional_args = ["10", "5", "2"]
        self.run_test_case(operations, 6, additional_args)


if __name__ == '__main__':
    unittest.main()
