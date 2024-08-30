#include "ls.h"

#include <gtest/gtest.h>

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

bool AreMatricesEqual(const Ls::StringMatrix &mat1,
                      const Ls::StringMatrix &mat2) {
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

TEST_F(LsTest, hindi_l) {
  Ls lsCommand(false, true, true, false);
  const std::string path = "../data/hindi";
  const Ls::StringMatrix answer = {
      {"../data/hindi/kannada", "DIRECTORY"},
      {"../data/hindi/kannada/namaskaram.txt", "FILE"},
      {"../data/hindi/tamil", "DIRECTORY"},
      {"../data/hindi/tamil/telugu", "DIRECTORY"},
      {"../data/hindi/tamil/telugu/kannada_swagatha_hardlink.txt", "FILE"},
      {"../data/hindi/vanakkam.txt", "FILE"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, hindi_haR) {
  Ls lsCommand(true, false, true, true);
  const std::string path = "../data/hindi";
  const Ls::StringMatrix answer = {
      {"../data/hindi/.", "../data/hindi/kannada/..", "../data/hindi/tamil/.."},
      {"../data/hindi/kannada", "../data/hindi/kannada/."},
      {"../data/hindi/kannada/.namaskaram_hardlink.txt",
       "../data/hindi/kannada/namaskaram.txt"},
      {"../data/hindi/tamil", "../data/hindi/tamil/.",
       "../data/hindi/tamil/telugu/.."},
      {"../data/hindi/tamil/.hidden_file1",
       "../data/hindi/tamil/telugu/kannada_swagatha_hardlink.txt"},
      {"../data/hindi/tamil/telugu", "../data/hindi/tamil/telugu/."}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, hindi_hR) {
  Ls lsCommand(false, false, true, true);
  const std::string path = "../data/hindi";
  const Ls::StringMatrix answer = {};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, kannada_alRh) {
  Ls lsCommand(true, true, true, true);
  const std::string path = "../data/hindi/kannada";
  const Ls::StringMatrix answer = {
      {"../data/hindi/kannada/.namaskaram_hardlink.txt",
       "../data/hindi/kannada/namaskaram.txt", "FILE"},
  };

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, hindi_hlaR) {
  Ls lsCommand(true, true, true, true);
  const std::string path = "../data/hindi";
  const Ls::StringMatrix answer = {
      {"../data/hindi/.", "../data/hindi/kannada/..", "../data/hindi/tamil/..",
       "DIRECTORY"},
      {"../data/hindi/kannada", "../data/hindi/kannada/.", "DIRECTORY"},
      {"../data/hindi/kannada/.namaskaram_hardlink.txt",
       "../data/hindi/kannada/namaskaram.txt", "FILE"},
      {"../data/hindi/tamil", "../data/hindi/tamil/.",
       "../data/hindi/tamil/telugu/..", "DIRECTORY"},
      {"../data/hindi/tamil/.hidden_file1",
       "../data/hindi/tamil/telugu/kannada_swagatha_hardlink.txt", "FILE"},
      {"../data/hindi/tamil/telugu", "../data/hindi/tamil/telugu/.",
       "DIRECTORY"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, data_lRh) {
  Ls lsCommand(false, true, true, true);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {
      {"../data/bengali/namaskaram_hardlink.txt",
       "../data/hindi/kannada/namaskaram.txt", "FILE"},
      {"../data/hindi/vanakkam.txt", "../data/marathi/vanakkam_hardlink.txt",
       "FILE"},
      {"../data/marathi/assamese/namaste_hardlink.txt", "../data/namaste.txt",
       "FILE"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}

TEST_F(LsTest, data_alhR) {
  Ls lsCommand(true, true, true, true);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {
      {"../data/.", "../data/bengali/..", "../data/hindi/..",
       "../data/marathi/..", "DIRECTORY"},
      {"../data/bengali", "../data/bengali/.", "../data/bengali/malayalam/..",
       "DIRECTORY"},
      {"../data/bengali/malayalam", "../data/bengali/malayalam/.", "DIRECTORY"},
      {"../data/bengali/malayalam/swagatham.txt",
       "../data/hindi/tamil/telugu/.malayalam_swagatham_hardlink.txt", "FILE"},
      {"../data/bengali/namaskaram_hardlink.txt",
       "../data/hindi/kannada/.namaskaram_hardlink.txt",
       "../data/hindi/kannada/namaskaram.txt", "FILE"},
      {"../data/hindi", "../data/hindi/.", "../data/hindi/kannada/..",
       "../data/hindi/tamil/..", "DIRECTORY"},
      {"../data/hindi/kannada", "../data/hindi/kannada/.", "DIRECTORY"},
      {"../data/hindi/tamil", "../data/hindi/tamil/.",
       "../data/hindi/tamil/telugu/..", "DIRECTORY"},
      {"../data/hindi/tamil/.hidden_file1",
       "../data/hindi/tamil/telugu/kannada_swagatha_hardlink.txt", "FILE"},
      {"../data/hindi/tamil/telugu", "../data/hindi/tamil/telugu/.",
       "DIRECTORY"},
      {"../data/hindi/vanakkam.txt", "../data/marathi/vanakkam_hardlink.txt",
       "FILE"},
      {"../data/marathi", "../data/marathi/.", "../data/marathi/assamese/..",
       "DIRECTORY"},
      {"../data/marathi/assamese", "../data/marathi/assamese/.", "DIRECTORY"},
      {"../data/marathi/assamese/namaste_hardlink.txt", "../data/namaste.txt",
       "FILE"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  EXPECT_TRUE(AreMatricesEqual(answer, result))
      << "The matrices are not equal!";
}
