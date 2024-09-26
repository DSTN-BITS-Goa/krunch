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
                    self._write_file(testcase_number, operation['name'], operation['content'], operation['offset'])
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
        except Exception as e:
            print(f"Failed to read file '{name}' in test case {testcase_number}: {e}")
        finally:
            os.close(fd)
    def _write_file(self, testcase_number, name, content, offset):
        """Write content to an existing file and flush changes immediately using O_SYNC."""
        try:
            file_path = os.path.join(self.mount_dir_template.format(testcase_number), name)
            fd = os.open(file_path, os.O_WRONLY | os.O_SYNC)
            os.pwrite(fd, content.encode(), offset)  # os.write requires bytes, hence encode content
            os.close(fd)
        except Exception as e:
            print(f"Failed to write to file '{name}' in test case {testcase_number}: {e}")
        finally:
            os.close(fd)

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
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 0},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 3},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 9},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 14},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},
            {'type': 'delete', 'name': 'file1.txt'}
        ]
        additional_args = ["4", "8", "16"]  # Example additional arguments for myfs
        self.run_test_case(operations, 1, 10, additional_args)

    def test_case2(self):
        operations = [
            {'type': 'create', 'name': 'file1.txt'},
            {'type': 'create', 'name': 'file2.txt'},

            {'type': 'write', 'name': 'file1.txt', 'content': 'a', 'offset': 0},
            {'type': 'write', 'name': 'file1.txt', 'content': 'b', 'offset': 1},
            {'type': 'write', 'name': 'file1.txt', 'content': 'c', 'offset': 0},
            {'type': 'write', 'name': 'file1.txt', 'content': 'ab', 'offset': 0},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},
            {'type': 'write', 'name': 'file1.txt', 'content': 'd', 'offset': 0},
        ]
        additional_args = ["1", "1", "1"]
        self.run_test_case(operations, 2, 20, additional_args)

    def test_case3(self):
        operations = [
            {'type': 'create', 'name': 'file1.txt'},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 0},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 3},
            {'type': 'create', 'name': 'file2.txt'},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 9},
            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},

            {'type': 'write', 'name': 'file2.txt', 'content': 'Welcome!\nHere', 'offset': 0},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 12},

            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 13},
            {'type': 'write', 'name': 'file2.txt', 'content': 'Welcome!\nHere', 'offset': 10},

            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},

            {'type': 'delete', 'name': 'file1.txt'}
        ]
        additional_args = ["2", "4", "5"]  # Example additional arguments for myfs
        self.run_test_case(operations, 3, 30, additional_args)

    def test_case4(self):
        operations = [
            {'type': 'create', 'name': 'file1.txt'},

            {'type': 'create', 'name': 'file3.txt'},

            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 0},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 8},
            {'type': 'create', 'name': 'file2.txt'},
            {'type': 'write', 'name': 'file2.txt', 'content': 'Welcome!', 'offset': 0},

            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 1},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 2},
            {'type': 'write', 'name': 'file1.txt', 'content': 'Welcome!', 'offset': 5},

            {'type': 'read', 'name': 'file1.txt', 'offset': 0, 'length': 1024},

            {'type': 'delete', 'name': 'file1.txt'},

            {'type': 'write', 'name': 'file2.txt', 'content': 'Welcome!\nHere', 'offset': 0},
            {'type': 'write', 'name': 'file2.txt', 'content': '\n\n', 'offset': 2},

            {'type': 'write', 'name': 'file2.txt', 'content': 'Hello!\n', 'offset': 10},

            {'type': 'read', 'name': 'file2.txt', 'offset': 0, 'length': 1024},
        ]
        additional_args = ["3", "4", "6"]  # Example additional arguments for myfs
        self.run_test_case(operations, 4, 40, additional_args)

if __name__ == "__main__":
    unittest.main(exit=False)
    for i in range(1, 2):
        if "test_case_" + str(i) not in scores["scores"]:
            scores["scores"]["test_case_" + str(i)] = 0

    # print(json.dumps({"_presentation": "semantic"}, separators=(',', ': ')))
    # print(json.dumps(scores, separators=(',', ': ')))

    with open("test_results.json", "w") as f:
        f.write(json.dumps({"_presentation": "semantic"}, separators=(',', ': ')))
        f.write("\n")
        f.write(json.dumps(scores, separators=(',', ': ')))
