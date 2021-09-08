#include <iostream>
#include <string>
#include <fstream>
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

    try {
        fprob.open("vars/prob_" + var_num + ".csv");
        std::vector<std::vector<double>> prob;
        if (!parse_data(prob, fprob)) throw -2;
        fprob.close();

        ftable.open("vars/table_" + var_num + ".csv");
        std::vector<std::vector<double>> table;
        if (!parse_data(table, ftable)) throw -2;
        ftable.close();
    }
    catch(int a) {
        std::cerr << "Parsing error";
        return a;
    }
    
    return 0;
}
