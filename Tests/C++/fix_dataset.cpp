//
// Created by nightfury on 10/7/21.
//
#include <fstream>
//#include

using namespace csv;
// This file will add a header (a line) to the data set.
// This line will specify the type of each column, to be recognized by Data Frame

// Use this command to count how many lines are there in the data set :
//  wc -l bdd.csv
//     -> result : 34551849 bdd.csv

const std::string NUMBER_OF_LINES = "34551849";
const std::string NUMBER_OF_LINES_FOR_TEST = "200";

// argument column type must be in the "<here>" ;
// example : bool ->> "bool"
std::string add_type_of_column(std::string column_name,  std::string column_type, bool for_test = false) {
    if (for_test)
        return column_name + ":" + NUMBER_OF_LINES_FOR_TEST + ":<" + column_type + '>';
    else
        return column_name + ":" + NUMBER_OF_LINES + ":<" + column_type + '>';
}

int main() {
    // create fixed_bdd.csv
//    std::ofstream fixed_dataset("/Users/nightfury/CLionProjects/fixed_bdd.csv", std::ofstream::trunc);
    // create test_bdd.csv : a small data set
    std::ofstream fixed_dataset("/Users/nightfury/CLionProjects/test_bdd.csv", std::ofstream::trunc);
    std::string s;
    // Add name , type here   ; the last line hasn't le comma ','
    // Should avoid "int" ; use "ul" instead
    bool for_test = true;
    if (for_test) {
        s += add_type_of_column("ID", "int", true) + ',';
        s += add_type_of_column("datetime", "string", true) + ',';
        s += add_type_of_column("X", "double", true) + ',';
        s += add_type_of_column("Y", "double", true);
    } else {
        s += add_type_of_column("ID", "int") + ',';
        s += add_type_of_column("datetime", "string") + ',';
        s += add_type_of_column("X", "double") + ',';
        s += add_type_of_column("Y", "double");
    }
    fixed_dataset << s << '\n';
//    std::ifstream dataset("/home/nightfury/CLionProjects/bdd.csv");
    CSVReader reader("/Users/nightfury/CLionProjects/bdd.csv");
    int count = 0;
    for (CSVRow& row: reader) { // Input iterator
        if (count++ >= stoi(NUMBER_OF_LINES_FOR_TEST)) {break;}
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