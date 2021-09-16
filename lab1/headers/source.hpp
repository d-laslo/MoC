#pragma once
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <regex>
#include "defines.hpp"

int parse_data(std::vector<std::vector<double>>&, std::ifstream&);
int parse_data(std::vector<std::vector<int>>&, std::ifstream&);
void read_from_file(std::string&& file_name, std::vector<std::vector<int>>& container);
void read_from_file(std::string&& file_name, std::vector<std::vector<double>>&  container);

int write_data(const std::vector<double>& data, std::ofstream& file);
int write_data(const std::vector<std::vector<double>>& data, std::ofstream& file);
void write_to_file(const std::string&& file_name, const std::vector<double>& data);
void write_to_file(const std::string&& file_name, const std::vector<std::vector<double>>& data);

void transpose(std::vector<std::vector<double>>& matrix);