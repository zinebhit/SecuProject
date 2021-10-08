//
// Created by nightfury on 10/8/21.
//

#include <fstream>
#include "library/csv.hpp"

using namespace csv;
using namespace std;

//const unsigned int NUMBER_OF_LINES = 50;
const unsigned int NUMBER_OF_LINES = 34551849;

struct node{
   unsigned int id;
   string date;
   double x;
   double y;
};

int main() {
//    std::ofstream fixed_dataset("/Users/nightfury/CLionProjects/fixed_bdd.csv", std::ofstream::trunc);
//    std::string s;

    CSVReader reader("/home/nightfury/CLionProjects/bdd.csv");
//    CSVReader reader("/home/nightfury/CLionProjects/test_bdd.csv");
    vector<int> id(NUMBER_OF_LINES);
    vector<string> date(NUMBER_OF_LINES);
    vector<double> x(NUMBER_OF_LINES);
    vector<double> y(NUMBER_OF_LINES);

    // create a data base : int ; string ; double ; double;
    int count = 0;
    for (CSVRow& row: reader) { // Input iterator
        for (int i=0; i<row.size(); i++) {
//        for (CSVField& field: row) {
            // By default, get<>() produces a std::string.
            // A more efficient get<string_view>() is also available, where the resulting
            // string_view is valid as long as the parent CSVRow is alive
            if (i == 0) id[count] = row[i].get<int>();
            else if (i==1) date[count] = row[i].get<string_view >();
            else if (i==2) x[count] = row[i].get<double>();
            else if (i==3) y[count] = row[i].get<double>();
        }
        count++;
    }
    return 0;
}
