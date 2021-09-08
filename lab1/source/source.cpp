#include "../headers/source.hpp"

int parse_data(std::vector<std::vector<double>>& result, std::ifstream& file)
{
    // convert csv str to array double
    auto convert = [](std::string& line)
    {
        std::regex rgx{R"(\d+\.?\d*)"};
        const std::vector<std::smatch> rgx_res{
            std::sregex_iterator{line.begin(), line.end(), rgx},
            std::sregex_iterator{}
        };
        std::vector<double> res;
        for (auto i : rgx_res) {
            res.push_back(stod(i.str(0)));
        }
        return res;
    };

    std::string line;
    if (file.is_open()) {
        while ( getline(file ,line) ) {            
            result.push_back(convert(line));
        }
    }
    else {
        return -1;
    }
    return 0;
}