#pragma once
#include <vector>
#include <numeric>
#include <algorithm>
#include <map>
#include <random>
#include "defines.hpp"


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

u_int64_t bayes_function(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob,
    u_int64_t ciphertext_index
);

u_int64_t bayes_function(
    const std::vector<std::vector<double>>& cond_plt_cpht_dist,
    u_int64_t ciphertext_index
);

u_int64_t stohastic_function(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob,
    u_int64_t ciphertext_index
);

u_int64_t stohastic_function(
    const std::vector<std::vector<double>>& cond_plt_cpht_dist,
    u_int64_t ciphertext_index
);

void generate_distribution(
    const std::vector<std::vector<double>>& cond_plt_cpht_dist, 
    u_int64_t ciphertext_index, 
    std::vector<double>& distribution
);