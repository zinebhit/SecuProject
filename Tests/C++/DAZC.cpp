#pragma once

#include "library/csv.hpp"
#include <DataFrame/DataFrame.h>
#include <filesystem>

//using namespace std;
using ULDataFrame = hmdf::StdDataFrame<unsigned long>;
using namespace hmdf;

unsigned int NUMBER_OF_LINE;

// get data
namespace dazc {
    struct point {
        int id{};
        std::string datetime;
        double x{};
        double y{};
    };

    point get_data_row(const ULDataFrame& df, unsigned int index) {
        assert(index >= 0);
        HeteroVector row = df.get_row<int, std::string, double>(index);
        point data_point = {
                row.at<int>(0),
                row.at<std::string>(0),
                row.at<double>(0),
                row.at<double>(1)
        };
        return data_point;
    }
}

// some useful functions
namespace dazc {
    // use wc -l to know number of lines of the data set
    ULDataFrame read(const std::string &file_name, const unsigned int number_of_lines) {
        // set global variable
        NUMBER_OF_LINE = number_of_lines;
        csv::CSVFormat format; format.delimiter('\t').no_header();
        csv::CSVReader reader(file_name, format);
        std::vector<int> id(number_of_lines);
        std::vector<std::string> date(number_of_lines);
        std::vector<double> x(number_of_lines);
        std::vector<double> y(number_of_lines);

        // data colums : int ; string ; double ; double;
        // use library csv to read data and store it to vectors
        int count = 0;
        for (csv::CSVRow &row: reader) { // Input iterator
            // check if variale number_of_lines smaller than the real number of lines
            assert (count < number_of_lines && "Error: Wrong number of lines!");
            for (int i = 0; i < row.size(); i++) {
                if (i == 0) id[count] = row[i].get<int>();
                else if (i == 1) date[count] = row[i].get<std::string_view>();
                else if (i == 2) x[count] = row[i].get<double>();
                else if (i == 3) y[count] = row[i].get<double>();
            }
            count++;
        }

        // load data to data frame
        ULDataFrame df;
        // Start value is included. End value is excluded.
        // Index will be from 1 to N. (N is number_of_lines)
        df.load_data(
                ULDataFrame::gen_sequence_index(0, number_of_lines , 1), // INDEX
                std::make_pair("ID", id),
                std::make_pair("DateTime", date),
                std::make_pair("X", x),
                std::make_pair("Y", y)
        );
        return df;
    }

    void write(const ULDataFrame& df, const std::string &file_name) {
        std::ofstream output_file(file_name);
        point data_point;
        for (int i=0; i < NUMBER_OF_LINE; i++ ) {
            data_point = get_data_row(df, i);
            output_file << data_point.id << '\t' << data_point.datetime << '\t' << data_point.x << '\t' << data_point.y << '\n';
        }
    }

    void generate_small_data_set(const std::string &input_file_name,
                                 const std::string &output_file_name, const unsigned int number_of_lines_of_output) {
        // check if the file already exists, then anounce
        if (std::filesystem::exists(output_file_name)) {
            std::cout << "File exists!!! Do you want to replace? (y/n) : ";
            std::string s; std::cin >> s;
            if (s == "n") return;
        }

        std::ifstream input_file(input_file_name);
        std::ofstream output_file(output_file_name, std::fstream::trunc);
        std::string s;
        int i = 0;
        while (getline(input_file, s) && i++ < number_of_lines_of_output) {
            output_file << s << '\n';
        }
        assert(i != number_of_lines_of_output && "Error: file input's lines < number of lines expected!");
        input_file.close();
        output_file.close();
    }
};
