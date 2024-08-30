#ifndef LS_H
#define LS_H

#include <string>  // Do NOT change this line
#include <tuple>
#include <vector>  // Do NOT change this line

class Ls {
  // Do NOT change this line
 public:
  using LsEntry = std::tuple<std::string, char>;  // (name, type)
  using StringMatrix =
      std::vector<std::vector<std::string> >;  // Do NOT change this line

  Ls();                                // Do NOT change this line
  Ls(bool a, bool l, bool R, bool h);  // Do NOT change this line

  Ls::StringMatrix Run(const std::string &path);  // Do NOT change this line

 private:
  bool a_;  // Do NOT change this line
  bool l_;  // Do NOT change this line
  bool R_;  // Do NOT change this line
  bool h_;  // Do NOT change this line

  std::vector<LsEntry> ScanDirectory(const std::string &path);

  std::vector<LsEntry> ScanDirectoryRecursive(const std::string &path);

  StringMatrix ProcessEntries(std::vector<LsEntry> &entries);

  void Print(const StringMatrix &strings);  // Do NOT change this line
};

#endif  // LS_H
