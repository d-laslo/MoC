#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <map>
#include <numeric>
#include "headers/lab1.hpp"
#include "headers/source.hpp"

using namespace std;

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
    
    ifstream fprob, ftable;
    string var_num = argv[1];
    var_num = (var_num.length() > 1 ? "" : "0") + var_num;

    vector<vector<double>> prob;
    vector<vector<int>> table;
    try {
        fprob.open("vars/prob_" + var_num + ".csv");
        if (parse_data(prob, fprob)) throw -2;
        fprob.close();

        ftable.open("vars/table_" + var_num + ".csv");
        if (parse_data(table, ftable)) throw -2;
        ftable.close();
    }
    catch(int a) {
        cerr << "Parsing error";
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
    map<string, vector<double>> probabilities {{"plaintext", prob[0]}, {"key", prob[1]}};


    vector<double> cpht_dist;
    ciphertext_probability_distribution(ciphertext_indexes, probabilities, cpht_dist);

    vector<vector<double>> plt_cpht_dist;
    plaintext_ciphertext_probability_distribution(ciphertext_indexes, probabilities, plt_cpht_dist);

    vector<vector<double>> cond_plt_cpht_dist;
    probability_distribution_plaintext_under_condition_ciphertext(ciphertext_indexes, probabilities, cond_plt_cpht_dist);

    cout << bayes_function(ciphertext_indexes, probabilities, 0) << endl;
    return 0;
}
