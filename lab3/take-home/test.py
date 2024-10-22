import json
import os
import unittest
import subprocess
import shutil

scores = {"scores": {}}
class TestMyFS(unittest.TestCase):
    mount_dir_template = 'mount_tc{}'  # Relative path from the build directory
    root_dir_template = 'root_tc{}'  # Relative path from the build directory
    log_file_template = 'logs/myfs_tc{}.log'  # Relative path from the build directory
    expected_output_dir = '../expected_logs'  # Relative path from the build directory

    def update_scores(self, test_case, score, expr1, expr2):
        if expr1 == expr2:
            scores["scores"][f"test_case_{test_case}"] = score
        else:
            scores["scores"][f"test_case_{test_case}"] = 0

    def run_myfs(self, testcase_number, additional_args=[]):
        """Run the myfs command to mount the FUSE filesystem."""
        command = ["./myfs", self.mount_dir_template.format(testcase_number), self.log_file_template.format(testcase_number), self.root_dir_template.format(testcase_number)] + additional_args
        subprocess.run(command, check=True)

    def run_test_case(self, operations, testcase_number, score, additional_args=[]):
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


        self._compare_logs(testcase_number, score)

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


    def _compare_logs(self, testcase_number, score):
        """Compare the generated log file with the expected log."""
        log_file = self.log_file_template.format(testcase_number)
        expected_log_file = os.path.join(self.expected_output_dir, f'expected_tc{testcase_number}.log')

        with open(log_file, 'r') as log, open(expected_log_file, 'r') as expected:
            log_contents = log.read().strip()
            expected_contents = expected.read().strip()
            self.update_scores(testcase_number, score, log_contents, expected_contents)
            self.assertEqual(log_contents, expected_contents)

    def test_case1(self):
        operations = [
            {'type': 'create', 'name': 'file1.txt'},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!'},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},
            {'type': 'delete', 'name': 'file1.txt'}
        ]
        additional_args = ["4", "8", "16"]  # Example additional arguments for myfs
        self.run_test_case(operations, 1, 10, additional_args)

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
        self.run_test_case(operations, 2, 10, additional_args)

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
        self.run_test_case(operations, 3, 20, additional_args)

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
        self.run_test_case(operations, 4, 20, additional_args)

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
        self.run_test_case(operations, 5, 40, additional_args)

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
        self.run_test_case(operations, 6, 40, additional_args)

    def test_case7(self):
        operations = [
            {'type': 'create', 'name': 'file1.txt'},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Hello\nThere\n'},
            {'type': 'create', 'name': 'file2.txt'},
            {'type': 'write', 'name': 'file2.txt', 'content': '\n\n\nHI\n'},
            {'type': 'create', 'name': 'file3.txt'},
            {'type': 'write', 'name': 'file3.txt', 'content': 'This\nis\na\nTest\n'},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},
            {'type': 'delete', 'name': 'file1.txt'},
            {'type': 'write', 'name': 'file3.txt', 'content': 'This\nis\na\nTest\n'},
            {'type': 'delete', 'name': 'file3.txt'},
            {'type': 'read', 'name': 'file2.txt', 'offset': 0, 'length': 1024},
        ]
        additional_args = ["4", "5", "4"]
        self.run_test_case(operations, 7, 50, additional_args)

    def test_case8(self):
        operations = [
            {'type': 'create', 'name': 'file1.txt'},
            {'type': 'create', 'name': 'file2.txt'},
            {'type': 'create', 'name': 'file3.txt'},
            {'type': 'create', 'name': 'file4.txt'},
            {'type': 'delete', 'name': 'file1.txt'},
            {'type': 'delete', 'name': 'file3.txt'},
            {'type': 'create', 'name': 'file5.txt'},
            {'type': 'create', 'name': 'file6.txt'},

            {'type': 'write', 'name': 'file5.txt', 'content': 'file5'},
            {'type': 'write', 'name': 'file2.txt', 'content': 'file2'},
            {'type': 'read', 'name': 'file2.txt', 'offset': 0, 'length': 1024},
            {'type': 'write', 'name': 'file6.txt', 'content': 'file6'},
            {'type': 'write', 'name': 'file4.txt', 'content': 'file4'},
            {'type': 'read', 'name': 'file4.txt', 'offset': 0, 'length': 1024},
            {'type': 'delete', 'name': 'file5.txt'},
            {'type': 'write', 'name': 'file4.txt', 'content': '\nfile5gone'},
            {'type': 'read', 'name': 'file4.txt', 'offset': 0, 'length': 1024},
        ]
        additional_args = ["4", "5", "5"]
        self.run_test_case(operations, 8, 50, additional_args)

    def test_case9(self):
        operations = [
            {'type': 'create', 'name': 'file1.txt'},
            {'type': 'create', 'name': 'file2.txt'},
            {'type': 'create', 'name': 'file3.txt'},
            {'type': 'create', 'name': 'file4.txt'},
            {'type': 'create', 'name': 'file5.txt'},
            {'type': 'create', 'name': 'file6.txt'},

            {'type': 'write', 'name': 'file1.txt', 'content': 'abcd'},
            {'type': 'write', 'name': 'file1.txt', 'content': 'abc'},
            {'type': 'write', 'name': 'file1.txt', 'content': 'ab'},
            {'type': 'write', 'name': 'file1.txt', 'content': 'a'},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},
        ]
        additional_args = ["1", "1", "1"]
        self.run_test_case(operations, 9, 50, additional_args)

    def test_case10(self):
        operations = [
            {'type': 'create', 'name': 'file1.txt'},
            {'type': 'write', 'name': 'file1.txt', 'content': 'She sells seashells by the seashore\n'},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},
            {'type': 'write', 'name': 'file1.txt', 'content': 'The shells she sells are surely seashells\n'},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},
            {'type': 'write', 'name': 'file1.txt', 'content': 'So if she sells shells on the seashore\n'},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},
            {'type': 'write', 'name': 'file1.txt', 'content': 'How much space left?\n'},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},
            {'type': 'delete', 'name': 'file1.txt'},
        ]
        additional_args = ["10", "20", "5"]
        self.run_test_case(operations, 10, 50, additional_args)

    def test_case11(self):
        operations = [
            {'type': 'create', 'name': 'program.cpp'},
            {'type': 'write', 'name': 'program.cpp', 'content': '#include "program.h"\n'},
            {'type': 'write', 'name': 'program.cpp', 'content': 'using namespace std;\n'},
            {'type': 'write', 'name': 'program.cpp', 'content': 'int main(){\n'},
            {'type': 'write', 'name': 'program.cpp', 'content': '  cout << "Hello World!";\n'},
            {'type': 'read', 'name': 'program.cpp', 'offset': 0, 'length': 1024},
            {'type': 'write', 'name': 'program.cpp', 'content': '  return 0;\n'},
            {'type': 'write', 'name': 'program.cpp', 'content': '}\n'},


            {'type': 'create', 'name': 'hello.py'},
            {'type': 'write', 'name': 'hello.py', 'content': 'print("Hello World!")\n'},
            {'type': 'read', 'name': 'program.cpp', 'offset': 0, 'length': 1024},
            {'type': 'read', 'name': 'hello.py', 'offset': 0, 'length': 1024},

            {'type': 'create', 'name': 'program.h'},
            {'type': 'write', 'name': 'program.h', 'content': '#include<bits/stdc++.h>\n'},
            {'type': 'read', 'name': 'program.h', 'offset': 0, 'length': 1024},

            {'type': 'create', 'name': 'hello.py.h'},
            {'type': 'write', 'name': 'program.h', 'content': '#####################################################\n'},


        ]
        additional_args = ["3", "20", "8"]
        self.run_test_case(operations, 11, 80, additional_args)

if __name__ == "__main__":
    unittest.main(exit=False)

    total = 0
    for i in range(1, 12):
        if "test_case_" + str(i) not in scores["scores"]:
            scores["scores"]["test_case_" + str(i)] = 0
        total += scores["scores"]["test_case_" + str(i)]

    # print(json.dumps({"_presentation": "semantic"}, separators=(',', ': ')))
    # print(json.dumps(scores, separators=(',', ': ')))
    print("Total score: ", total)

    with open("test_results.json", "w") as f:
        f.write(json.dumps({"_presentation": "semantic"}, separators=(',', ': ')))
        f.write("\n")
        f.write(json.dumps(scores, separators=(',', ': ')))
