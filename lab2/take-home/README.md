# Lab 2: Take Home

> Warning:
>
> The lab will be auto-graded
> Do NOT make any changes to [`CMakeLists.txt`](CMakeLists.txt) or [`ls_test.cpp`](ls_test.cpp)

## Usage

To test your solution:

```bash
    cd PATH/TO/lab2/take-home
    mkdir build
    cd build
    cmake ..
    make run_tests
```

> NOTE:
> `make run_tests` must be run from within the `build/` directory

## Question

### Question 1

In this lab, you will be implementing a simplified version of the [`ls`](https://man7.org/linux/man-pages/man1/ls.1.html) command

You will be implementing the `Ls` class. Refer to the [`ls.h`](ls.h) file for the class definition.
Note that all lines can be modified, unless otherwise specified in the comments.

`Ls::Run(path)` prints out and returns the contents of the directory specified by `path` in the format specified by the flags.

`Ls::Print()` has already been implemented for you. Feel free to use this as you see fit.

`StringMatrix` represents a 2-D matrix of `std::string`'s.

#### Output

The basic implementation of `Ls::Run(path)` should return a `StringMatrix` of all files located in `path` with the following format:

```text
relative_file_path_to_file1
relative_file_path_to_file2
...
```

> Note:
> The paths expected in [`ls_test.cpp`](ls_test.cpp) are relative to the `build/` directory

##### Flags

###### `-a`

List all entries **including hidden files** (files that start with a `.`). The basic ls command does not list hidden files.

###### `-l`

List in long format. Long format consists of both the **filename and filetype**.

```text
relative_file_path_to_file1 FILE1_TYPE
relative_file_path_to_file2 FILE2_TYPE
...
```

The following `FILE_TYPE`'s are expected:

1. `DIRECTORY` for directories
2. `SOFTLINK` for soft links
3. `FILE` for everything else

###### `-R`

List **recursively**.

> Refer to [`ls_test.cpp`](ls_test.cpp) for examples.
>

> NOTE: Your implementation will be tested on combinations of flags as well.
>
> Eg: `ls -alR` and `ls -lRa` would recursively list all files including hidden files in long format
> WARNING:
> Ensure that rows of `StringMatrix` returned by `Ls::Run()` are sorted in lexicographical order

### Question 2

- Read about the [`strace`](https://strace.io/) command along with some examples
- Compare the output of `strace` on your implementation of `Ls` with that of the actual `ls` command
- There is no written submission for this. This may be discussed during the in-lab component.
