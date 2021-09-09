#include "../headers/lab1.hpp"

void ciphertext_probability_distribution(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob, 
    std::vector<double>& result
)
{
    for (auto cpht_indx: table) {
        result.push_back(std::accumulate(cpht_indx.begin(), cpht_indx.end(), 0.,
            [&prob](double result, const std::map<std::string, int>& index)
            {
                return result + prob.at("key")[index.at("key")] * prob.at("plaintext")[index.at("plaintext")];
            }
        ));
    }
}

void plaintext_ciphertext_probability_distribution(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob, 
    // indexes: [plaintext_index][cipphertext_index]
    std::vector<std::vector<double>>& result
)
{
    for (u_int64_t plt_indx = 0; plt_indx < M; plt_indx++) {
        result.push_back({});
        auto& tmp = result[plt_indx];
        for (auto cpht_indx: table) {
            tmp.push_back(
                prob.at("plaintext")[plt_indx] * std::accumulate(cpht_indx.begin(), cpht_indx.end(), 0.,
                [&prob, plt_indx](double result, const std::map<std::string, int>& index)
                {
                    return  ((u_int64_t)index.at("plaintext") == plt_indx ? result + prob.at("key")[index.at("key")] : result);
                }
            ));
        }
    }
}