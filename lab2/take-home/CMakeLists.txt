cmake_minimum_required(VERSION 3.10)
project(krunch-private)

# Set C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Fetch Google Test
include(FetchContent)
FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG        main
)
FetchContent_MakeAvailable(googletest)

# Add the Ls class source files
add_executable(ls_test
        ls.cpp
        ls_test.cpp
)

# Link Google Test
target_link_libraries(ls_test
        gtest_main
        pthread
)

# Add a custom target to run tests
add_custom_target(run_tests
        COMMAND ls_test
        DEPENDS ls_test
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

# Define the root directory where the folder structure will be created
set(TEST_DATA_DIR "${CMAKE_SOURCE_DIR}/data")

# Custom command to create the folder structure with Indian language names
add_custom_target(create_test_data ALL
    # Create the directory structure with Indian language names
    COMMAND ${CMAKE_COMMAND} -E make_directory "${TEST_DATA_DIR}/hindi/tamil/telugu"
    COMMAND ${CMAKE_COMMAND} -E make_directory "${TEST_DATA_DIR}/marathi/assamese"
    COMMAND ${CMAKE_COMMAND} -E make_directory "${TEST_DATA_DIR}/bengali/malayalam"

    # Create regular files with "hello" in different Indian languages
    COMMAND ${CMAKE_COMMAND} -E touch "${TEST_DATA_DIR}/namaste.txt"
    COMMAND ${CMAKE_COMMAND} -E touch "${TEST_DATA_DIR}/hindi/vanakkam.txt"
    COMMAND ${CMAKE_COMMAND} -E touch "${TEST_DATA_DIR}/hindi/tamil/namaskaram.txt"

    # Create hidden files
    COMMAND ${CMAKE_COMMAND} -E touch "${TEST_DATA_DIR}/hindi/tamil/.hidden_file1"
    COMMAND ${CMAKE_COMMAND} -E touch "${TEST_DATA_DIR}/hindi/tamil/.hidden_file2"

    # Create symbolic links
    COMMAND ${CMAKE_COMMAND} -E create_symlink "${TEST_DATA_DIR}/hindi/tamil/namaskaram.txt" "${TEST_DATA_DIR}/hindi/tamil/telugu/link_to_namaskaram.txt"
    COMMAND ${CMAKE_COMMAND} -E create_symlink "${TEST_DATA_DIR}/hindi" "${TEST_DATA_DIR}/hindi/tamil/link_to_hindi"

    COMMENT "Creating shortened test data folder structure with updated files"
)

# Ensure the test data is created before running tests
add_dependencies(run_tests create_test_data)

# Add a test target to be used with CTest
enable_testing()
add_test(NAME LsTests COMMAND ls_test)

# Ensure that `make` will build and run tests
add_dependencies(run_tests ls_test)
