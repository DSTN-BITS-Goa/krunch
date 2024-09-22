cmake_minimum_required(VERSION 3.20)

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

# Add the executable
add_executable(myfs myfs.cpp)

# Link FUSE3 library
target_link_libraries(myfs ${FUSE3_LIBRARIES})

# Create test directories manually
set(MOUNT_DIR1 ${CMAKE_BINARY_DIR}/mount_tc1)
set(ROOT_DIR1 ${CMAKE_BINARY_DIR}/root_tc1)
set(MOUNT_DIR2 ${CMAKE_BINARY_DIR}/mount_tc2)
set(ROOT_DIR2 ${CMAKE_BINARY_DIR}/root_tc2)
set(MOUNT_DIR3 ${CMAKE_BINARY_DIR}/mount_tc3)
set(ROOT_DIR3 ${CMAKE_BINARY_DIR}/root_tc3)
set(MOUNT_DIR4 ${CMAKE_BINARY_DIR}/mount_tc4)
set(ROOT_DIR4 ${CMAKE_BINARY_DIR}/root_tc4)
set(MOUNT_DIR5 ${CMAKE_BINARY_DIR}/mount_tc5)
set(ROOT_DIR5 ${CMAKE_BINARY_DIR}/root_tc5)
set(MOUNT_DIR6 ${CMAKE_BINARY_DIR}/mount_tc6)
set(ROOT_DIR6 ${CMAKE_BINARY_DIR}/root_tc6)

add_custom_command(
        OUTPUT ${MOUNT_DIR1} ${ROOT_DIR1} ${MOUNT_DIR2} ${ROOT_DIR2}
        ${MOUNT_DIR3} ${ROOT_DIR3} ${MOUNT_DIR4} ${ROOT_DIR4}
        ${MOUNT_DIR5} ${ROOT_DIR5} ${MOUNT_DIR6} ${ROOT_DIR6}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${MOUNT_DIR1}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${ROOT_DIR1}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${MOUNT_DIR2}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${ROOT_DIR2}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${MOUNT_DIR3}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${ROOT_DIR3}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${MOUNT_DIR4}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${ROOT_DIR4}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${MOUNT_DIR5}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${ROOT_DIR5}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${MOUNT_DIR6}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${ROOT_DIR6}
        COMMENT "Creating test directories"
)


# Add a custom target to ensure directories are created before tests
add_custom_target(create_test_dirs ALL DEPENDS
        ${MOUNT_DIR1}
        ${ROOT_DIR1}
        ${MOUNT_DIR2}
        ${ROOT_DIR2}
        ${MOUNT_DIR3}
        ${ROOT_DIR3}
        ${MOUNT_DIR4}
        ${ROOT_DIR4}
        ${MOUNT_DIR5}
        ${ROOT_DIR5}
        ${MOUNT_DIR6}
        ${ROOT_DIR6}
)

# Add custom target to handle the entire test process
add_custom_target(run_tests
        DEPENDS myfs create_test_dirs
        COMMAND ${CMAKE_COMMAND} -E echo "Running tests..."
        COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/logs
        COMMAND python ${CMAKE_SOURCE_DIR}/test.py || true
        COMMAND ${CMAKE_COMMAND} -E echo "Unmounting and removing directories..."
        COMMAND fusermount -u ${MOUNT_DIR1} || true
        COMMAND fusermount -u ${MOUNT_DIR2} || true
        COMMAND fusermount -u ${MOUNT_DIR3} || true
        COMMAND fusermount -u ${MOUNT_DIR4} || true
        COMMAND fusermount -u ${MOUNT_DIR5} || true
        COMMAND fusermount -u ${MOUNT_DIR6} || true
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${MOUNT_DIR1} || true
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${ROOT_DIR1} || true
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${MOUNT_DIR2} || true
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${ROOT_DIR2} || true
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${MOUNT_DIR3} || true
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${ROOT_DIR3} || true
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${MOUNT_DIR4} || true
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${ROOT_DIR4} || true
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${MOUNT_DIR5} || true
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${ROOT_DIR5} || true
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${MOUNT_DIR6} || true
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${ROOT_DIR6} || true
)

# Ensure myfs is built before running tests
add_dependencies(run_tests myfs)
