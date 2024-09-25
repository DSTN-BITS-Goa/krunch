#ifndef _PARAMS_H_
#define _PARAMS_H_

#define FUSE_USE_VERSION 31

#define _GNU_SOURCE

#include <cstring>
#include <map>
#include <string>
#include <vector>

// DO NOT CHANGE THIS STRUCT
struct inode {
    // stories indices of data blocks associated with this inode
    std::vector<int> blocks;
};

// DO NOT CHANGE THIS STRUCT
struct data_block {
    char *data;

    // Constructor
    data_block(int size) {
        data = new char[size];
        std::fill(data, data + size, 0);  // Initialize with zeros
    }

    // Destructor
    ~data_block() {
        delete[] data;
    }

};

// DO NOT CHANGE THIS STRUCT
struct myfs_state {
    int NUM_DATA_BLOCKS;
    int NUM_INODES;
    int DATA_BLOCK_SIZE;

    FILE *logfile;
    char *rootdir;

    // list of pre allocated data blocks and inodes
    std::vector<data_block*> data_blocks;
    std::vector<inode*> inodes;

    // bitmaps to keep track of free inodes and data blocks
    std::vector<bool> inode_bitmap;
    std::vector<bool> data_block_bitmap;

    // map to keep track of inodes associated with a path
    std::map<std::string, int> path_to_inode;
    // Constructor
    myfs_state(FILE *log, const char *root, int num_inodes, int num_data_blocks, int data_block_size)
        : NUM_DATA_BLOCKS(num_data_blocks), NUM_INODES(num_inodes), DATA_BLOCK_SIZE(data_block_size), logfile(log) {

        // Allocate and initialize data blocks
        for (int i = 0; i < NUM_DATA_BLOCKS; ++i) {
            data_blocks.push_back(new data_block(DATA_BLOCK_SIZE));
        }

        // Allocate and initialize inodes
        for (int i = 0; i < NUM_INODES; ++i) {
            inodes.push_back(new inode());
        }

        inode_bitmap.assign(NUM_INODES, false);
        data_block_bitmap.assign(NUM_DATA_BLOCKS, false);

        // Allocate and initialize root directory
        rootdir = new char[strlen(root) + 1];
        strcpy(rootdir, root);
    }

    // Destructor
    ~myfs_state() {
        // Free data blocks
        for (auto block : data_blocks) {
            delete block;
        }

        // Free inodes
        for (auto node : inodes) {
            delete node;
        }

        // Free root directory memory
        delete[] rootdir;

        // Close the logfile (if needed)
        if (logfile != nullptr) {
            fclose(logfile);
        }
    }

};

// Define the MYFS_DATA macro to access the myfs_state object
#define MYFS_DATA ((struct myfs_state *) fuse_get_context()->private_data)

#endif
