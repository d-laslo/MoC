#pragma once
#include <vector>
#include <numeric>
#include <map>


const u_int64_t M = 20;
const u_int64_t C = 20;
const u_int64_t K = 20;

void ciphertext_probability_distribution(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob, 
    std::vector<double>& result
);

void plaintext_ciphertext_probability_distribution(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob, 
    // indexes: [plaintext_index][ciphertext_index]
    std::vector<std::vector<double>>& result
);

void probability_distribution_plaintext_under_condition_ciphertext(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob, 
    // indexes: [plaintext_index][ciphertext_index]
    std::vector<std::vector<double>>& result
);