#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <map>
#include <numeric>
#include "headers/lab1.hpp"
#include "headers/source.hpp"
#include "headers/defines.hpp"

using namespace std;

#define PATH_TO_SOURCE (string)"./vars/"
#define PATH_TO_RESULT (string)"./result/"

int main(int argc, char const *argv[])
{
    
    try {
        if (argc < 2) {
            throw -1;
        }
    }
    catch (int a) {
        cerr << "Not enough arguments\n";
        return a;
    }
    
    string var_num = argv[1];
    var_num = (var_num.length() > 1 ? "" : "0") + var_num;

    vector<vector<double>> prob;
    vector<vector<int>> table;
    try {
        read_from_file(PATH_TO_SOURCE + "prob_" + var_num + ".csv", prob);
        read_from_file(PATH_TO_SOURCE + "table_" + var_num + ".csv", table);
    }
    catch(int a) {
        cerr << "File reading error";
        return a;
    }

    // stores the plaintext and key indices for the ciphertext 
    vector<vector<map<string, int>>> ciphertext_indexes(C);
    for (u_int64_t k_indx = 0; k_indx < table.size(); k_indx++) {
        for (u_int64_t plt_indx = 0; plt_indx < table[k_indx].size(); plt_indx++) {
            ciphertext_indexes[ table[k_indx][plt_indx] ].push_back({
                {"key", k_indx}, 
                {"plaintext", plt_indx}
            }); 
        }
    }

    // stores the probabilities of the plaintexts and keys
    map<string, vector<double>> probabilities{{"plaintext", prob[0]}, {"key", prob[1]}};


    vector<double> cpht_dist;
    ciphertext_probability_distribution(ciphertext_indexes, probabilities, cpht_dist);
    write_to_file(PATH_TO_RESULT + "cpht_dist_" + var_num + ".csv", cpht_dist);

    vector<vector<double>> plt_cpht_dist;
    plaintext_ciphertext_probability_distribution(ciphertext_indexes, probabilities, plt_cpht_dist);
    write_to_file(PATH_TO_RESULT + "plt_cpht_dist_" + var_num + ".csv", plt_cpht_dist);


    vector<vector<double>> cond_plt_cpht_dist;
    probability_distribution_plaintext_under_condition_ciphertext(ciphertext_indexes, probabilities, cond_plt_cpht_dist);
    write_to_file(PATH_TO_RESULT + "cond_plt_cpht_dist_" + var_num + ".csv", cond_plt_cpht_dist);

    // for (auto i = 0; i < 20; i++)
    // {
    //     cout << bayes_loss_function(cond_plt_cpht_dist,0, i) << endl;
    // }

    cout << avg_bayes_loss_function(plt_cpht_dist, cond_plt_cpht_dist) << endl;
    
    //cout << stohastic_function(ciphertext_indexes, probabilities, 5) << endl;
    // vector<vector<double>> m;
    // stohastic_matrix(cond_plt_cpht_dist, m);
    return 0;
}
