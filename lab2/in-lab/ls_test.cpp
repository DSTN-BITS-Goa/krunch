#include <gtest/gtest.h>

#include <string>
#include <vector>

#include "ls.h"

int NUM_TCS = 11;
std::vector<int> scores(20);
#include <fstream>

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

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[0] = passed ? 10 : 0;
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

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[1] = passed ? 10 : 0;
}

TEST_F(LsTest, hindi_hR) {
  Ls lsCommand(false, false, true, true);
  const std::string path = "../data/hindi";
  const Ls::StringMatrix answer = {};

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[2] = passed ? 10 : 0;
}

TEST_F(LsTest, kannada_alRh) {
  Ls lsCommand(true, true, true, true);
  const std::string path = "../data/hindi/kannada";
  const Ls::StringMatrix answer = {
      {"../data/hindi/kannada/.namaskaram_hardlink.txt",
       "../data/hindi/kannada/namaskaram.txt", "FILE"},
  };

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[3] = passed ? 20 : 0;
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

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[4] = passed ? 20 : 0;
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

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[5] = passed ? 20 : 0;
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

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[6] = passed ? 30 : 0;
}

TEST_F(LsTest, hidden_lh) {
  Ls lsCommand(false, true, false, true);
  const std::string path = "../hidden_data";
  const Ls::StringMatrix answer = {
      {"../hidden_data/swapfile", "../hidden_data/swapfile_pc", "FILE"},
  };

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[7] = passed ? 30 : 0;
}

TEST_F(LsTest, abc_aRh) {
  Ls lsCommand(true, false, true, true);
  const std::string path = "../hidden_data/home/abc";
  const Ls::StringMatrix answer = {
      {"../hidden_data/home/abc/.", "../hidden_data/home/abc/.cache/..",
       "../hidden_data/home/abc/Documents/..",
       "../hidden_data/home/abc/Downloads/.."},
      {"../hidden_data/home/abc/.cache", "../hidden_data/home/abc/.cache/."},
      {"../hidden_data/home/abc/.cache/jdk",
       "../hidden_data/home/abc/.cache/jdk1"},
      {"../hidden_data/home/abc/Documents",
       "../hidden_data/home/abc/Documents/.",
       "../hidden_data/home/abc/Documents/temp/.."},
      {"../hidden_data/home/abc/Documents/temp",
       "../hidden_data/home/abc/Documents/temp/."},
      {"../hidden_data/home/abc/Downloads",
       "../hidden_data/home/abc/Downloads/."},
  };

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[8] = passed ? 50 : 0;
}

TEST_F(LsTest, hidden_lRh) {
  Ls lsCommand(false, true, true, true);
  const std::string path = "../hidden_data";
  const Ls::StringMatrix answer = {
      {"../hidden_data/bin/cat.exe", "../hidden_data/home/abc/cat", "FILE"},
      {"../hidden_data/bin/ls", "../hidden_data/etc/ls_etc", "FILE"},
      {"../hidden_data/swapfile", "../hidden_data/swapfile_pc", "FILE"},
  };

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[9] = passed ? 40 : 0;
}

TEST_F(LsTest, hidden_alRh) {
  Ls lsCommand(true, true, true, true);
  const std::string path = "../hidden_data";
  const Ls::StringMatrix answer = {
      {"../hidden_data/.", "../hidden_data/bin/..", "../hidden_data/etc/..",
       "../hidden_data/home/..", "DIRECTORY"},
      {"../hidden_data/bin", "../hidden_data/bin/.", "DIRECTORY"},
      {"../hidden_data/bin/cat.exe", "../hidden_data/home/abc/cat", "FILE"},
      {"../hidden_data/bin/ls", "../hidden_data/etc/ls_etc",
       "../hidden_data/home/abc/Downloads/.ls", "FILE"},
      {"../hidden_data/etc", "../hidden_data/etc/.",
       "../hidden_data/etc/pacman/..", "DIRECTORY"},
      {"../hidden_data/etc/pacman", "../hidden_data/etc/pacman/.", "DIRECTORY"},
      {"../hidden_data/home", "../hidden_data/home/.",
       "../hidden_data/home/abc/..", "DIRECTORY"},
      {"../hidden_data/home/abc", "../hidden_data/home/abc/.",
       "../hidden_data/home/abc/.cache/..",
       "../hidden_data/home/abc/Documents/..",
       "../hidden_data/home/abc/Downloads/..", "DIRECTORY"},
      {"../hidden_data/home/abc/.cache", "../hidden_data/home/abc/.cache/.",
       "DIRECTORY"},
      {"../hidden_data/home/abc/.cache/jdk",
       "../hidden_data/home/abc/.cache/jdk1", "FILE"},
      {"../hidden_data/home/abc/Documents",
       "../hidden_data/home/abc/Documents/.",
       "../hidden_data/home/abc/Documents/temp/..", "DIRECTORY"},
      {"../hidden_data/home/abc/Documents/temp",
       "../hidden_data/home/abc/Documents/temp/.", "DIRECTORY"},
      {"../hidden_data/home/abc/Documents/temp/.swapfile",
       "../hidden_data/swapfile", "../hidden_data/swapfile_pc", "FILE"},
      {"../hidden_data/home/abc/Downloads",
       "../hidden_data/home/abc/Downloads/.", "DIRECTORY"},
  };

  const Ls::StringMatrix result = lsCommand.Run(path);

  bool passed = AreMatricesEqual(answer, result);
  EXPECT_TRUE(passed)
      << "The matrices are not equal!";
    scores[10] = passed ? 100 : 0;
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
