cmake_minimum_required(VERSION 3.10)

# Project information
project(MyFuseFileSystem VERSION 1.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Find FUSE3 library
find_package(PkgConfig REQUIRED)
pkg_check_modules(FUSE3 fuse3 REQUIRED)

# Include FUSE3 headers
include_directories(${FUSE3_INCLUDE_DIRS})

add_executable(myfs myfs.cpp)

# Link FUSE3 library
target_link_libraries(myfs ${FUSE3_LIBRARIES})

# Add post-build message
add_custom_command(TARGET myfs POST_BUILD
        COMMAND echo "Build complete. Run './myfs /path/to/mountpoint' to mount the FUSE filesystem.")
