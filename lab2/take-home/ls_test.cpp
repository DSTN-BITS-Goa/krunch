#include <gtest/gtest.h>

#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include "ls.h"

int NUM_TCS = 12;
std::vector<int> scores(20);

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

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[0] = passed ? 10 : 0;
}

TEST_F(LsTest, l) {
  Ls lsCommand(false, true, false);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {{"../data/bengali", "DIRECTORY"},
                                   {"../data/hindi", "DIRECTORY"},
                                   {"../data/marathi", "DIRECTORY"},
                                   {"../data/namaste.txt", "FILE"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[1] = passed ? 10 : 0;
}

TEST_F(LsTest, a) {
  Ls lsCommand(true, false, false);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {
      {"../data/."},     {"../data/.."},      {"../data/bengali"},
      {"../data/hindi"}, {"../data/marathi"}, {"../data/namaste.txt"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[2] = passed ? 10 : 0;
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

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[3] = passed ? 20 : 0;
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

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[4] = passed ? 20 : 0;
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

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[5] = passed ? 20 : 0;
}

TEST_F(LsTest, al) {
  Ls lsCommand(true, true, false);
  const std::string path = "../data";
  const Ls::StringMatrix answer = {
      {"../data/.", "DIRECTORY"},       {"../data/..", "DIRECTORY"},
      {"../data/bengali", "DIRECTORY"}, {"../data/hindi", "DIRECTORY"},
      {"../data/marathi", "DIRECTORY"}, {"../data/namaste.txt", "FILE"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[6] = passed ? 30 : 0;
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

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[7] = passed ? 50 : 0;
}

TEST_F(LsTest, aR_hidden) {
  Ls lsCommand(true, false, true);
  const std::string path = "../hidden_data/etc";
const Ls::StringMatrix answer = {{"../hidden_data/etc/."},
                                 {"../hidden_data/etc/.."},
                                 {"../hidden_data/etc/.bashrcetc_history"},
                                 {"../hidden_data/etc/.pacmanrc"},
                                 {"../hidden_data/etc/pacman"},
                                 {"../hidden_data/etc/pacman/."},
                                 {"../hidden_data/etc/pacman/.."},
                                 {"../hidden_data/etc/pacman/pacman.conf"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[8] = passed ? 50 : 0;
}

TEST_F(LsTest, lR_hidden) {
  Ls lsCommand(false, true, true);
  const std::string path = "../hidden_data/home/abc";
  const Ls::StringMatrix answer = {
      {"../hidden_data/home/abc/Documents", "DIRECTORY"},
      {"../hidden_data/home/abc/Documents/hello.c", "FILE"},
      {"../hidden_data/home/abc/Documents/temp", "DIRECTORY"},
      {"../hidden_data/home/abc/Documents/temp/hello.cpp", "FILE"},
      {"../hidden_data/home/abc/Documents/temp/hello.java", "FILE"},
      {"../hidden_data/home/abc/Downloads", "DIRECTORY"},
      {"../hidden_data/home/abc/Downloads/assignment.pdf", "FILE"},
      {"../hidden_data/home/abc/Downloads/random.jpeg", "FILE"},
      {"../hidden_data/home/abc/RanDOM.c", "FILE"},
      {"../hidden_data/home/abc/hello.cpp", "SOFTLINK"},
      {"../hidden_data/home/abc/ls", "SOFTLINK"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[9] = passed ? 50 : 0;
}

TEST_F(LsTest, al_hidden) {
  Ls lsCommand(true, true, false);
  const std::string path = "../hidden_data/home/abc";
  const Ls::StringMatrix answer = {
      {"../hidden_data/home/abc/.", "DIRECTORY"},
      {"../hidden_data/home/abc/..", "DIRECTORY"},
      {"../hidden_data/home/abc/.bash_history", "FILE"},
      {"../hidden_data/home/abc/.cache", "DIRECTORY"},
      {"../hidden_data/home/abc/Documents", "DIRECTORY"},
      {"../hidden_data/home/abc/Downloads", "DIRECTORY"},
      {"../hidden_data/home/abc/RanDOM.c", "FILE"},
      {"../hidden_data/home/abc/hello.cpp", "SOFTLINK"},
      {"../hidden_data/home/abc/ls", "SOFTLINK"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[10] = passed ? 50 : 0;
}

TEST_F(LsTest, alR_hidden) {
  Ls lsCommand(true, true, true);
  const std::string path = "../hidden_data";
  const Ls::StringMatrix answer = {
      {"../hidden_data/.", "DIRECTORY"},
      {"../hidden_data/..", "DIRECTORY"},
      {"../hidden_data/bin", "DIRECTORY"},
      {"../hidden_data/bin/.", "DIRECTORY"},
      {"../hidden_data/bin/..", "DIRECTORY"},
      {"../hidden_data/bin/cat.exe", "FILE"},
      {"../hidden_data/bin/ls", "FILE"},
      {"../hidden_data/etc", "DIRECTORY"},
      {"../hidden_data/etc/.", "DIRECTORY"},
      {"../hidden_data/etc/..", "DIRECTORY"},
      {"../hidden_data/etc/.bashrcetc_history", "SOFTLINK"},
      {"../hidden_data/etc/.pacmanrc", "FILE"},
      {"../hidden_data/etc/pacman", "DIRECTORY"},
      {"../hidden_data/etc/pacman/.", "DIRECTORY"},
      {"../hidden_data/etc/pacman/..", "DIRECTORY"},
      {"../hidden_data/etc/pacman/pacman.conf", "FILE"},
      {"../hidden_data/home", "DIRECTORY"},
      {"../hidden_data/home/.", "DIRECTORY"},
      {"../hidden_data/home/..", "DIRECTORY"},
      {"../hidden_data/home/abc", "DIRECTORY"},
      {"../hidden_data/home/abc/.", "DIRECTORY"},
      {"../hidden_data/home/abc/..", "DIRECTORY"},
      {"../hidden_data/home/abc/.bash_history", "FILE"},
      {"../hidden_data/home/abc/.cache", "DIRECTORY"},
      {"../hidden_data/home/abc/.cache/.", "DIRECTORY"},
      {"../hidden_data/home/abc/.cache/..", "DIRECTORY"},
      {"../hidden_data/home/abc/.cache/jdk", "FILE"},
      {"../hidden_data/home/abc/Documents", "DIRECTORY"},
      {"../hidden_data/home/abc/Documents/.", "DIRECTORY"},
      {"../hidden_data/home/abc/Documents/..", "DIRECTORY"},
      {"../hidden_data/home/abc/Documents/hello.c", "FILE"},
      {"../hidden_data/home/abc/Documents/temp", "DIRECTORY"},
      {"../hidden_data/home/abc/Documents/temp/.", "DIRECTORY"},
      {"../hidden_data/home/abc/Documents/temp/..", "DIRECTORY"},
      {"../hidden_data/home/abc/Documents/temp/.gitignore", "FILE"},
      {"../hidden_data/home/abc/Documents/temp/hello.cpp", "FILE"},
      {"../hidden_data/home/abc/Documents/temp/hello.java", "FILE"},
      {"../hidden_data/home/abc/Downloads", "DIRECTORY"},
      {"../hidden_data/home/abc/Downloads/.", "DIRECTORY"},
      {"../hidden_data/home/abc/Downloads/..", "DIRECTORY"},
      {"../hidden_data/home/abc/Downloads/assignment.pdf", "FILE"},
      {"../hidden_data/home/abc/Downloads/random.jpeg", "FILE"},
      {"../hidden_data/home/abc/RanDOM.c", "FILE"},
      {"../hidden_data/home/abc/hello.cpp", "SOFTLINK"},
      {"../hidden_data/home/abc/ls", "SOFTLINK"},
      {"../hidden_data/swapfile", "FILE"}};

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[11] = passed ? 100 : 0;
}

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  int result = RUN_ALL_TESTS();

  // Manually construct JSON in one line
  std::ostringstream jsonOutput;

  // Write _presentation line
  jsonOutput << "{\"_presentation\":\"semantic\"}\n";

  // Write results line
  jsonOutput << "{\"scores\":{";

  for (size_t i = 0; i < NUM_TCS; ++i) {
    jsonOutput << "\"test_case_" << i + 1 << "\": " << scores[i];
    if (i != NUM_TCS - 1) {
      jsonOutput << ",";
    }
  }

  jsonOutput << "}}";

  // Write JSON to a file
  std::ofstream outFile("test_results.json");
  outFile << jsonOutput.str();
  outFile.close();

  return 0;
}