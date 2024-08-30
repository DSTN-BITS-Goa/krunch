# Lab 2: In Lab

> Warning:
>
> The lab will be auto-graded
> Do NOT make any changes to [`CMakeLists.txt`](CMakeLists.txt) or [`ls_test.cpp`](ls_test.cpp)

## Usage

To test your solution:

```bash
    cd PATH/TO/lab2/in-lab
    mkdir build
    cd build
    cmake ..
    make run_tests
```

> NOTE:
> `make run_tests` must be run from within the `build/` directory

## Question

### Question 1

In this lab, you will be implementing the `-h` flag for `ls.cpp`

> Warning:
> The constructors of the `Ls` class has been modified to account for the new `h` flag.
> Ensure that your in-lab implementation is consistent with the new constructors, and the `h_` variable declaration

> Note:
> The paths expected in [`ls_test.cpp`](ls_test.cpp) are relative to the `build/` directory

#### Flags

##### `-h`

List files that are hardlinked to each other in the directory. Group the hardlinked files together in a single row `StringMatrix`.
The file names in a single row must be sorted in lexicographical order. The rows must also be sorted in lexicographical order amongst themselves.

```text
hardlink1_relative_file_path_to_file1 harlink1_relative_file_path_to_file2 hardlink1_relative_file_path_to_file3
hardlink2_relative_file_path_to_file4 hardlink2_relative_file_path_to_file5
...
```

###### `-hl`

if `-hl` is supplied as a flag, the output should be in the following format.
Only the file paths should be sorted in lexicographical order and the FILE_TYPE must be the last element in the row

```text
hardlink1_relative_file_path_to_file1 hardlink1_relative_file_path_to_file2 hardlink1_relative_file_path_to_file3 FILE_TYPE
hardlink2_relative_file_path_to_file4 hardlink2_relative_file_path_to_file5 FILE_TYPE
...
```

> Refer to [`ls_test.cpp`](ls_test.cpp) for examples.

> NOTE: Your implementation will be tested on combinations of flags as well.
>
> Eg: `ls -ahlR` and `ls -lhRa` would recursively list all files that have more than one hard link including hidden
> files in long format
>
> WARNING:
> Ensure that rows of `StringMatrix` returned by `Ls::Run()` are arranged in lexicographical order
