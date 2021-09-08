#include <iostream>
#include <string>
#include "headers/lab1.hpp"
#include "headers/source.hpp"

int main(int argc, char const *argv[])
{
    try {
        if (argc < 2) {
            throw -1;//"Not enough arguments";
        }
    }
    catch (int a) {
        std::cerr << "Not enough arguments\n";
    }
    
    
    return 0;
}
