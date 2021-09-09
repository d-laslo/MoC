#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <map>
#include <numeric>
#include "headers/lab1.hpp"
#include "headers/source.hpp"



int main(int argc, char const *argv[])
{
    
    try {
        if (argc < 2) {
            throw -1;
        }
    }
    catch (int a) {
        std::cerr << "Not enough arguments\n";
        return a;
    }
    
    std::ifstream fprob, ftable;
    std::string var_num = argv[1];
    var_num = (var_num.length() > 1 ? "" : "0") + var_num;

    std::vector<std::vector<double>> prob;
    std::vector<std::vector<int>> table;
    try {
        fprob.open("vars/prob_" + var_num + ".csv");
        if (parse_data(prob, fprob)) throw -2;
        fprob.close();

        ftable.open("vars/table_" + var_num + ".csv");
        if (parse_data(table, ftable)) throw -2;
        ftable.close();
    }
    catch(int a) {
        std::cerr << "Parsing error";
        return a;
    }

    // stores the plaintext and key indices for the ciphertext 
    std::vector<std::vector<std::map<std::string, int>>> ciphertext_indexes(C);
    for (u_int64_t k_indx = 0; k_indx < table.size(); k_indx++) {
        for (u_int64_t plt_indx = 0; plt_indx < table[k_indx].size(); plt_indx++) {
            ciphertext_indexes[ table[k_indx][plt_indx] ].push_back({
                {"key", k_indx}, 
                {"plaintext", plt_indx}
            }); 
        }
    }

    // stores the probabilities of the plaintexts and keys
    std::map<std::string, std::vector<double>> probabilities {{"plaintext", prob[0]}, {"key", prob[1]}};


    std::vector<double> ciphertext_dist;
    ciphertext_probability_distribution(ciphertext_indexes, probabilities, ciphertext_dist);
    
        
    return 0;
}
