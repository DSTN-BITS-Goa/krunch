#include "ls.h"

#include <dirent.h>
#include <gtest/gtest.h>

#include <memory>
#include <string>
#include <vector>

class LsTest : public ::testing::Test {
 protected:
  void SetUp() override {
    // Set up test data or mocks if necessary
  }

  void TearDown() override {
    // Clean up after tests if necessary
  }
};

bool AreMatricesEqual(const Ls::StringMatrix& mat1,
                      const Ls::StringMatrix& mat2) {
  // Check if the sizes of the matrices are the same
  if (mat1.size() != mat2.size()) return false;

  // Check if each row has the same size and elements
  for (size_t i = 0; i < mat1.size(); ++i) {
    if (mat1[i].size() != mat2[i].size()) return false;

    for (size_t j = 0; j < mat1[i].size(); ++j)
      if (mat1[i][j] != mat2[i][j]) return false;
  }

  // If all checks pass, the matrices are equal
  return true;
}

TEST_F(LsTest, Basic) {
  Ls lsCommand(false, false, false);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {{"../data/bengali"},
                                   {"../data/hindi"},
                                   {"../data/marathi"},
                                   {"../data/namaste.txt"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, l) {
  Ls lsCommand(false, true, false);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {{"../data/bengali", "DIRECTORY"},
                                   {"../data/hindi", "DIRECTORY"},
                                   {"../data/marathi", "DIRECTORY"},
                                   {"../data/namaste.txt", "FILE"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, a) {
  Ls lsCommand(true, false, false);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {
      {"../data/."},     {"../data/.."},      {"../data/bengali"},
      {"../data/hindi"}, {"../data/marathi"}, {"../data/namaste.txt"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, R) {
  Ls lsCommand(false, false, true);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {
      {"../data/bengali"},
      {"../data/bengali/malayalam"},
      {"../data/hindi"},
      {"../data/hindi/tamil"},
      {"../data/hindi/tamil/link_to_hindi"},
      {"../data/hindi/tamil/namaskaram.txt"},
      {"../data/hindi/tamil/telugu"},
      {"../data/hindi/tamil/telugu/link_to_namaskaram.txt"},
      {"../data/hindi/vanakkam.txt"},
      {"../data/marathi"},
      {"../data/marathi/assamese"},
      {"../data/namaste.txt"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, lR) {
  Ls lsCommand(false, true, true);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {
      {"../data/bengali", "DIRECTORY"},
      {"../data/bengali/malayalam", "DIRECTORY"},
      {"../data/hindi", "DIRECTORY"},
      {"../data/hindi/tamil", "DIRECTORY"},
      {"../data/hindi/tamil/link_to_hindi", "SOFTLINK"},
      {"../data/hindi/tamil/namaskaram.txt", "FILE"},
      {"../data/hindi/tamil/telugu", "DIRECTORY"},
      {"../data/hindi/tamil/telugu/link_to_namaskaram.txt", "SOFTLINK"},
      {"../data/hindi/vanakkam.txt", "FILE"},
      {"../data/marathi", "DIRECTORY"},
      {"../data/marathi/assamese", "DIRECTORY"},
      {"../data/namaste.txt", "FILE"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, aR) {
  Ls lsCommand(true, false, true);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {
      {"../data/."},
      {"../data/.."},
      {"../data/bengali"},
      {"../data/bengali/."},
      {"../data/bengali/.."},
      {"../data/bengali/malayalam"},
      {"../data/bengali/malayalam/."},
      {"../data/bengali/malayalam/.."},
      {"../data/hindi"},
      {"../data/hindi/."},
      {"../data/hindi/.."},
      {"../data/hindi/tamil"},
      {"../data/hindi/tamil/."},
      {"../data/hindi/tamil/.."},
      {"../data/hindi/tamil/.hidden_file1"},
      {"../data/hindi/tamil/.hidden_file2"},
      {"../data/hindi/tamil/link_to_hindi"},
      {"../data/hindi/tamil/namaskaram.txt"},
      {"../data/hindi/tamil/telugu"},
      {"../data/hindi/tamil/telugu/."},
      {"../data/hindi/tamil/telugu/.."},
      {"../data/hindi/tamil/telugu/link_to_namaskaram.txt"},
      {"../data/hindi/vanakkam.txt"},
      {"../data/marathi"},
      {"../data/marathi/."},
      {"../data/marathi/.."},
      {"../data/marathi/assamese"},
      {"../data/marathi/assamese/."},
      {"../data/marathi/assamese/.."},
      {"../data/namaste.txt"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, al) {
  Ls lsCommand(true, true, false);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {
      {"../data/.", "DIRECTORY"},       {"../data/..", "DIRECTORY"},
      {"../data/bengali", "DIRECTORY"}, {"../data/hindi", "DIRECTORY"},
      {"../data/marathi", "DIRECTORY"}, {"../data/namaste.txt", "FILE"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, alR) {
  Ls lsCommand(true, true, true);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {
      {"../data/.", "DIRECTORY"},
      {"../data/..", "DIRECTORY"},
      {"../data/bengali", "DIRECTORY"},
      {"../data/bengali/.", "DIRECTORY"},
      {"../data/bengali/..", "DIRECTORY"},
      {"../data/bengali/malayalam", "DIRECTORY"},
      {"../data/bengali/malayalam/.", "DIRECTORY"},
      {"../data/bengali/malayalam/..", "DIRECTORY"},
      {"../data/hindi", "DIRECTORY"},
      {"../data/hindi/.", "DIRECTORY"},
      {"../data/hindi/..", "DIRECTORY"},
      {"../data/hindi/tamil", "DIRECTORY"},
      {"../data/hindi/tamil/.", "DIRECTORY"},
      {"../data/hindi/tamil/..", "DIRECTORY"},
      {"../data/hindi/tamil/.hidden_file1", "FILE"},
      {"../data/hindi/tamil/.hidden_file2", "FILE"},
      {"../data/hindi/tamil/link_to_hindi", "SOFTLINK"},
      {"../data/hindi/tamil/namaskaram.txt", "FILE"},
      {"../data/hindi/tamil/telugu", "DIRECTORY"},
      {"../data/hindi/tamil/telugu/.", "DIRECTORY"},
      {"../data/hindi/tamil/telugu/..", "DIRECTORY"},
      {"../data/hindi/tamil/telugu/link_to_namaskaram.txt", "SOFTLINK"},
      {"../data/hindi/vanakkam.txt", "FILE"},
      {"../data/marathi", "DIRECTORY"},
      {"../data/marathi/.", "DIRECTORY"},
      {"../data/marathi/..", "DIRECTORY"},
      {"../data/marathi/assamese", "DIRECTORY"},
      {"../data/marathi/assamese/.", "DIRECTORY"},
      {"../data/marathi/assamese/..", "DIRECTORY"},
      {"../data/namaste.txt", "FILE"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}