# Lab 3: Take Home

## Known Issues

- In `myfs_write` the buffer being passed is not consistent all the time. Use `size` to get the size of the buffer. If you try to manually calculate it you might get different values depending on the buffer passed at that time

## Usage

To test your solution:

```bash
    # Creates an executable named `myfs`
    cd PATH/TO/lab3/take-home
    mkdir build
    cd build
    cmake ..
    make run_tests
```
- This will create a `mount_tc{i}` and `root_tc{i}` folder for all the tescases in the `build` directory and then run each testcase on their respective folders
- The logs for each testcase will be stored in `logs/myfs_tc{i}.log` which you can view
- After the test is done the `mount_tc{i}` and `root_tc{i}` folders will be unmounted deleted

Note: make sure after you run the tests that `mount_tc{i}` and `root_tc{i}` folders are unmounted and deleted. The Makefile should automatically handle it, but incase of any errors manually make these changes
```bash
    # Unmount and delete the folders
    fusermount -u mount_tc{i}
    rm -rf mount_tc{i} root_tc{i}
```

## Background

In this lab you will be exploring the basics of [FUSE](https://github.com/libfuse/libfuse)

- First install the latest version (3.16.2) of FUSE on your system
- Go through the basics of FUSE and what it is used for
- Read the descriptions of the file system operations it [supports](https://github.com/libfuse/libfuse/blob/master/include/fuse.h#L317)
- A few tutorials to help you understand FUSE
  - https://www.cs.nmsu.edu/~pfeiffer/fuse-tutorial/
  - https://maastaar.net/fuse/linux/filesystem/c/2016/05/21/writing-a-simple-filesystem-using-fuse/
  - [FUSE Video demo](https://www.youtube.com/watch?v=aMlX2x5N9Ak)
- to install fuse3 on ubuntu
```bash
    sudo apt-get install fuse3 libfuse3-dev
```
## Starter code

- You are given a starter implementation of a simple FUSE file system that mirrors a given folder
- The implementation handles creating/reading/writing/deleting files and directories
- The private_data field of the `fuse_context` stores the following internal structures
  - `logfile`: A file pointer to the log file
  - `rootdir`: A file pointer to the root directory being mirrored
  - `NUM_INODES`: The number of inodes in the file system
  - `NUM_DATA_BLOCKS`: The number of data blocks in the file system
  - `DATA_BLOCK_SIZE`: The size of each data block
  - `inodes`: An array of inodes
    - An inode struct consists of a vector that stores the indices of the data_blocks that the file occupies
  - `data_blocks`: An array of data blocks
    - A data block struct consists of a char array of size `DATA_BLOCK_SIZE` that stores the data of the file
  - `inode_bitmap`: A bitmap that stores the free/allocated status of inodes
  - `data_block_bitmap`: A bitmap that stores the free/allocated status of data blocks
  - `path_to_inode_map`: A map that stores the path to inode mapping

- Additionaly some helper functions have been given
  - `log_fuse_context`: Logs the contents of the fuse_context
  - `log_msg`: Logs a message to the log file
    - This function is very useful for debugging any errors
    - Example usage: `log_msg("Reading Inode %d for file %s\n", i, path)`

- Usage:
```bash
    myfs [FUSE and mount options] mount_point log_file root_dir num_inodes num_data_blocks data_block_size
```

## Question

- In the take-home we assumed that only append writes are given in `myfs_write`
- For this lab modify `myfs_write` to handle writes at any offset
- All writes should be considered as overwrites