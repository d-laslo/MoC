#include "../headers/source.hpp"

int parse_data(std::vector<std::vector<double>>& result, std::ifstream& file)
{
    // convert csv str to array double
    auto convert = [](std::string& line)
    {
        std::regex rgx{R"(\d+\.?\d*)"};
        const std::vector<std::smatch> rgx_res{
            std::sregex_iterator{ALL(line), rgx},
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
        return 0;
    }
    return 1;
}

int parse_data(std::vector<std::vector<int>>& result, std::ifstream& file)
{
    // convert csv str to array double
    auto convert = [](std::string& line)
    {
        std::regex rgx{R"(\d+\.?\d*)"};
        const std::vector<std::smatch> rgx_res{
            std::sregex_iterator{ALL(line), rgx},
            std::sregex_iterator{}
        };
        std::vector<int> res;
        for (auto i : rgx_res) {
            res.push_back(stoi(i.str(0)));
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
        return 0;
    }
    return 1;
}


void read_from_file(std::string&& file_name, std::vector<std::vector<int>>& container)
{
    std::ifstream file(file_name);
    if (!parse_data(container, file)) throw -2;
    file.close();
}

void read_from_file(std::string&& file_name, std::vector<std::vector<double>>& container)
{
    std::ifstream file(file_name);
    if (!parse_data(container, file)) throw -2;
    file.close();
}

int write_data(const std::vector<double>& data, std::ofstream& file)
{
    if (file.is_open()) {
        for (auto col_data : data) {
            file <<  col_data << ",";
        }
    }
    else {
        return 0;
    }
    return 1;
}

int write_data(const std::vector<std::vector<double>>& data, std::ofstream& file)
{
    if (file.is_open()) {
        for (const auto& row : data) {
            for (auto col_data : row) {
                file <<  col_data << ",";
            }
            file << std::endl;
        }
    }
    else {
        return 0;
    }
    return 1;
}

void write_to_file(const std::string&& file_name, const std::vector<double>& data)
{
    std::ofstream file(file_name);
    if (!write_data(data, file)) throw -2;
    file.close();
}

void write_to_file(const std::string&& file_name, const std::vector<std::vector<double>>& data)
{
    std::ofstream file(file_name);
    if (!write_data(data, file)) throw -2;
    file.close();
}

void transpose(std::vector<std::vector<double>>& matrix)
{
    // std::vector<std::vector<double>> transponded_matrix(matrix.size(), std::vector<double>(matrix[0].size()));
    auto row_num = matrix.size();
    auto column_num = matrix[0].size();
    std::vector<std::vector<double>> transponded_matrix(column_num, std::vector<double>(row_num));
     
    for (u_int64_t i = 0; i < row_num; i++) {
        for (u_int64_t j = 0; j < column_num; j++) {
            transponded_matrix[j][i] = matrix[i][j];
        }
    }

    matrix = std::move(transponded_matrix);
}