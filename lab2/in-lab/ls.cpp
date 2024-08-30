#include "ls.h"

#include <iostream>

Ls::Ls()
    : a_(false), l_(false), R_(false), h_(false) {}  // Do NOT change this line

Ls::Ls(bool a, bool l, bool R, bool h)
    : a_(a), l_(l), R_(R), h_(h) {}  // Do NOT change this line

// Do NOT change this method
void Ls::Print(const StringMatrix& strings) {
  for (const auto& row : strings) {
    for (size_t i = 0; i < row.size(); ++i) {
      std::cout << row[i];
      if (i != row.size() - 1)  // Skip space after the last element
        std::cout << " ";
    }
    std::cout << std::endl;
  }
}

Ls::StringMatrix Ls::Run(const std::string& path) {
  StringMatrix result;

  // TODO: Implement this function

  Print(result);
  return result;
}