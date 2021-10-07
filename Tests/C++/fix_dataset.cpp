//
// Created by nightfury on 10/7/21.
//
#include <fstream>
#include "csv.hpp"

using namespace csv;
// This file will add a header (a line) to the data set.
// This line will specify the type of each column, to be recognized by Data Frame

// Use this command to count how many lines are there in the data set :
//  wc -l bdd.csv
//     -> result : 34551849 bdd.csv

const std::string number_of_lines = "34551849";

// argument column type must be in the "<here>" ;
// example : bool ->> "bool"
std::string add_type_of_column(std::string column_name, std::string column_type) {
    return column_name + ":" + number_of_lines + ":<" + column_type + '>';
}
int main() {
    std::ofstream fixed_dataset("/home/nightfury/CLionProjects/fixed_bdd.csv", std::ofstream::trunc);
    std::string s;
    // Add name , type here   ; the last line hasn't le comma ','
    // Should avoid "int" ; use "ul" instead
    s += add_type_of_column("ID", "int") + ',';
    s += add_type_of_column("datetime", "string") + ',';
    s += add_type_of_column("X", "double") + ',';
    s += add_type_of_column("Y", "double") ;
    fixed_dataset << s << '\n';
//    std::ifstream dataset("/home/nightfury/CLionProjects/bdd.csv");
    CSVReader reader("/home/nightfury/CLionProjects/bdd.csv");

    for (CSVRow& row: reader) { // Input iterator
        int i=0;
        for (CSVField& field: row) {
            // By default, get<>() produces a std::string.
            // A more efficient get<string_view>() is also available, where the resulting
            // string_view is valid as long as the parent CSVRow is alive
            fixed_dataset << field.get<std::string_view>();
            if (i != 3) fixed_dataset << ',';
            ++i;
        }
        fixed_dataset << '\n';
    }
    // append the dataset
//    while (getline(dataset, s)) {
//        fixed_dataset << s << '\n';
//    }
//    dataset.close();
    fixed_dataset.close();
    return 0;
}