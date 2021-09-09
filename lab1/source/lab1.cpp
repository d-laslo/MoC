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
    // indexes: [plaintext_index][ciphertext_index]
    std::vector<std::vector<double>>& result
)
{
    for (u_int64_t plt_indx = 0; plt_indx < M; plt_indx++) {
        result.push_back({});
        auto& curr_plt = *prev(result.end());
        for (auto cpht_indx: table) {
            curr_plt.push_back(
                prob.at("plaintext")[plt_indx] * std::accumulate(cpht_indx.begin(), cpht_indx.end(), 0.,
                [&prob, plt_indx](double result, const std::map<std::string, int>& index)
                {
                    return  ((u_int64_t)index.at("plaintext") == plt_indx ? result + prob.at("key")[index.at("key")] : result);
                }
            ));
        }
    }
}


void probability_distribution_plaintext_under_condition_ciphertext(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob, 
    // indexes: [plaintext_index][ciphertext_index]
    std::vector<std::vector<double>>& result
)
{
    std::vector<double> cpht_dist;
    ciphertext_probability_distribution(table, prob, cpht_dist);

    std::vector<std::vector<double>> plt_cpht_dist;
    plaintext_ciphertext_probability_distribution(table, prob, plt_cpht_dist);

    for (auto cpht_distr_on_plt : plt_cpht_dist) {
        result.push_back({});
        auto& curr_plt = *prev(result.end());
        for (u_int64_t cpht_indx = 0; cpht_indx < C; cpht_indx++) {
            curr_plt.push_back(cpht_distr_on_plt[cpht_indx] / cpht_dist[cpht_indx]);
        }
    }
}