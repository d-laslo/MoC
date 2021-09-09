#include "../headers/lab1.hpp"

void ciphertext_probability_distribution(const std::vector<std::vector<std::map<std::string, int>>>& table, const std::map<std::string, std::vector<double>>& prob, std::vector<double>& result)
{
    for (u_int64_t i = 0; i < table.size(); i++) {
        result.push_back(std::accumulate(table[i].begin(), table[i].end(), 0.,
            [&prob](double result, const std::map<std::string, int>& index)
            {
                return result + prob.at("key")[index.at("key")] * prob.at("plaintext")[index.at("plaintext")];
            }
        ));
    }
}