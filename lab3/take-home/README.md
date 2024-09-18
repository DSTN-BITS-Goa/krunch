# Lab 3: Take Home

## Usage

We've provided a simple CMake to compile your code:

```bash
    # Creates an executable named `myfs`
    cd PATH/TO/lab3/take-home
    mkdir build
    cd build
    cmake ..
    make
```

Note: This has not been tested thoroughly, so you may compile in your own way if you prefer.

## Background

In this lab you will be exploring the basics of [FUSE](https://github.com/libfuse/libfuse)

- First install the latest version (3.16.2) of FUSE on your system
- Go through the basics of FUSE and what it is used for
- Read the descriptions of the file system operations it [supports](https://github.com/libfuse/libfuse/blob/master/include/fuse.h#L317)
- A few tutorials to help you understand FUSE
  - https://www.cs.nmsu.edu/~pfeiffer/fuse-tutorial/
  - https://maastaar.net/fuse/linux/filesystem/c/2016/05/21/writing-a-simple-filesystem-using-fuse/
  - [FUSE Video demo](https://www.youtube.com/watch?v=aMlX2x5N9Ak)

## Question

- Implement a simple FUSE file system that mirrors the root file system of your machine. The file system should be mounted at a specified directory and should be able to handle creating/reading/writing/deleting files and directories
- Create your implementation in `myfs.cpp`
(Hint: Check out the [examples](https://github.com/libfuse/libfuse/tree/master/example) folder in the FUSE repository)
