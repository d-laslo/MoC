#include "../headers/lab1.hpp"

void ciphertext_probability_distribution(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob, 
    std::vector<double>& result
)
{
    for (auto cpht_indx: table) {
        result.push_back(std::accumulate(ALL(cpht_indx), 0.,
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
                prob.at("plaintext")[plt_indx] * std::accumulate(ALL(cpht_indx), 0.,
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


u_int64_t bayes_function(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob,
    u_int64_t ciphertext_index
)
{
    std::vector<std::vector<double>> cond_plt_cpht_dist;
    probability_distribution_plaintext_under_condition_ciphertext(table, prob, cond_plt_cpht_dist);

    return bayes_function(cond_plt_cpht_dist, ciphertext_index);
}


u_int64_t bayes_function(
    const std::vector<std::vector<double>>& cond_plt_cpht_dist,
    u_int64_t ciphertext_index
)
{
    return (std::max_element(ALL(cond_plt_cpht_dist), [ciphertext_index](auto a, auto b)
        {
            return (a[ciphertext_index] < b[ciphertext_index]);
        }
    ) - cond_plt_cpht_dist.begin());
}


u_int64_t stohastic_function(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob,
    u_int64_t ciphertext_index
)
{
    std::vector<std::vector<double>> cond_plt_cpht_dist;
    probability_distribution_plaintext_under_condition_ciphertext(table, prob, cond_plt_cpht_dist);

    return stohastic_function(cond_plt_cpht_dist, ciphertext_index);
}


u_int64_t stohastic_function(
    const std::vector<std::vector<double>>& cond_plt_cpht_dist,
    u_int64_t ciphertext_index
)
{
    std::vector<double> distribution;
    generate_distribution(cond_plt_cpht_dist, ciphertext_index, distribution);

    std::random_device rd;
    std::mt19937 gen(rd());
    std::discrete_distribution<> d(ALL(distribution));

    return d(gen);
}


void generate_distribution(
    const std::vector<std::vector<double>>& cond_plt_cpht_dist, 
    u_int64_t ciphertext_index, 
    std::vector<double>& distribution
)
{
    auto max = (*std::max_element(ALL(cond_plt_cpht_dist), [ciphertext_index](auto a, auto b) 
    {
        return a[ciphertext_index] < b[ciphertext_index];
    }))[ciphertext_index];

    auto max_num = std::accumulate(ALL(cond_plt_cpht_dist), 0, [ciphertext_index, max](auto a, auto b)
    {
        return a + (b[ciphertext_index] == max ? 1 : 0);
    });

    for (const auto& plt : cond_plt_cpht_dist) {
        distribution.push_back(plt[ciphertext_index] == max ? 1. / max_num : 0);
    }
}


void bayes_matrix(
    const std::vector<std::vector<double>>& cond_plt_cpht_dist,
    std::vector<std::vector<double>>& bayes_matrix
)
{
    bayes_matrix = std::move(std::vector<std::vector<double>> (cond_plt_cpht_dist.size(), std::vector<double> (cond_plt_cpht_dist[0].size(), 0)));

    for (u_int64_t cpht_index = 0; cpht_index < cond_plt_cpht_dist[0].size(); cpht_index++) {
        bayes_matrix[bayes_function(cond_plt_cpht_dist, cpht_index)][cpht_index] = 1;
    }
    // transpose(bayes_matrix);
}


void stohastic_matrix(
    const std::vector<std::vector<double>>& cond_plt_cpht_dist,
    std::vector<std::vector<double>>& stohastic_matrix
)
{
    for(u_int64_t i = 0; i < cond_plt_cpht_dist[0].size(); i++)
    {
        std::vector<double> tmp;
        generate_distribution(cond_plt_cpht_dist, i, tmp);
        stohastic_matrix.push_back(std::move(tmp));
    }
    transpose(stohastic_matrix);
}


bool bayes_loss_function(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob,
    u_int64_t ciphertext_index,   
    u_int64_t plaintext
)
{
    return bayes_function(table, prob, ciphertext_index) != plaintext;
}


bool bayes_loss_function(
    const std::vector<std::vector<double>>& cond_plt_cpht_dist,
    u_int64_t ciphertext_index, 
    u_int64_t plaintext
)
{
    return bayes_function(cond_plt_cpht_dist, ciphertext_index) != plaintext;
}


// double avg_bayes_loss_function(
//     const std::vector<std::vector<std::map<std::string, int>>>& table, 
//     const std::map<std::string, std::vector<double>>& prob
// )
// {
//     std::vector<std::vector<double>> plt_cpht_dist;
//     plaintext_ciphertext_probability_distribution(table, prob, plt_cpht_dist);

//     std::vector<std::vector<double>> cond_plt_cpht_dist;
//     probability_distribution_plaintext_under_condition_ciphertext(table, prob, cond_plt_cpht_dist);
//     return avg_bayes_loss_function(cond_plt_cpht_dist, plt_cpht_dist);
// }


// double avg_bayes_loss_function(
//     const std::vector<std::vector<double>>& plt_cpht_dist,
//     const std::vector<std::vector<double>>& cond_plt_cpht_dist
// )
// {
//     u_int64_t index_plt = -1;
//     u_int64_t index_cpht = -1;
//     return std::accumulate(ALL(plt_cpht_dist), .0, [&](auto a, auto b)
//     {
//         index_plt++;
//         index_cpht = -1;
//         return a + std::accumulate(ALL(b), .0, [&](auto a, auto b)
//         {
//             index_cpht++;
//             return a + (double)bayes_loss_function(cond_plt_cpht_dist, index_cpht, index_plt) * b;
//         });
//     });
// }

double avg_bayes_loss_function(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob
)
{
    std::vector<double> cpht_dist;
    ciphertext_probability_distribution(table, prob, cpht_dist);

    std::vector<std::vector<double>> cond_plt_cpht_dist;
    probability_distribution_plaintext_under_condition_ciphertext(table, prob, cond_plt_cpht_dist);

    return avg_bayes_loss_function(cpht_dist, cond_plt_cpht_dist);
}


double avg_bayes_loss_function(
    const std::vector<double>& cpht_dist,
    const std::vector<std::vector<double>>& cond_plt_cpht_dist
)
{
    u_int64_t cpht_index = -1;
    return std::accumulate(ALL(cpht_dist), .0, [&](auto a, auto b)
    {
        cpht_index++;
        return a + b * (1 - cond_plt_cpht_dist[bayes_function(cond_plt_cpht_dist, cpht_index)][cpht_index]);
    });
}


double avg_stohastic_loss_function(
    const std::vector<std::vector<std::map<std::string, int>>>& table, 
    const std::map<std::string, std::vector<double>>& prob
)
{
    std::vector<double> cpht_dist;
    ciphertext_probability_distribution(table, prob, cpht_dist);

    std::vector<std::vector<double>> cond_plt_cpht_dist;
    probability_distribution_plaintext_under_condition_ciphertext(table, prob, cond_plt_cpht_dist);
    
    return avg_stohastic_loss_function(cpht_dist, cond_plt_cpht_dist);
}

double avg_stohastic_loss_function(
    const std::vector<double>& cpht_dist,
    const std::vector<std::vector<double>>& cond_plt_cpht_dist
)
{
    
    std::vector<std::vector<double>> st_matrix;
    stohastic_matrix(cond_plt_cpht_dist, st_matrix);

    u_int64_t index_cpht = -1;
    u_int64_t index_plt = -1;
    return std::accumulate(ALL(cpht_dist), .0, [&](auto a, auto b)
    {
        index_cpht++;
        index_plt = -1;
        return a + b * (1 - std::accumulate(ALL(cond_plt_cpht_dist), .0, [&](auto a, auto b)
        {
            index_plt++;
            return a + b[index_cpht] * st_matrix[index_plt][index_cpht];
        }));
    });
}