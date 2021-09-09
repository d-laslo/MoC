#pragma once
#include <vector>
#include <numeric>
#include <map>


const int M = 20;
const int C = 20;
const int K = 20;

void ciphertext_probability_distribution(const std::vector<std::vector<std::map<std::string, int>>>&table, const std::map<std::string, std::vector<double>>& prob, std::vector<double>& result);