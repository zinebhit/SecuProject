#pragma once
#include "library/csv.hpp"
#include <DataFrame/DataFrame.h>

//using namespace std;
using ULDataFrame = hmdf::StdDataFrame<unsigned long>;

namespace dazc{
    // use wc -l to know number of lines of the data set
    ULDataFrame read(const std::string& filename, const unsigned int number_of_lines) {
        csv::CSVReader reader(filename);
        std::vector<int> id(number_of_lines);
        std::vector<std::string> date(number_of_lines);
        std::vector<double> x(number_of_lines);
        std::vector<double> y(number_of_lines);

        // data colums : int ; string ; double ; double;
        // use library csv to read data and store it to vectors
        int count = 0;
        for (csv::CSVRow& row: reader) { // Input iterator
            for (int i=0; i<row.size(); i++) {
                if (i == 0) id[count] = row[i].get<int>();
                else if (i==1) date[count] = row[i].get<std::string_view >();
                else if (i==2) x[count] = row[i].get<double>();
                else if (i==3) y[count] = row[i].get<double>();
            }
            count++;
        }

        // load data to data frame
        ULDataFrame df;
        // Start value is included. End value is excluded.
        // Index will be from 1 to N. (N is number_of_lines)
        df.load_data(
                ULDataFrame::gen_sequence_index(1, number_of_lines+1, 1 ), // INDEX
                std::make_pair("ID", id),
                std::make_pair("DateTime", date),
                std::make_pair("X", x),
                std::make_pair("Y", y)
        );
        return df;
   }
};