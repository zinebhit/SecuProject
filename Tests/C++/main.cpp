//
// Created by nightfury on 10/8/21.
//
#include "DAZC.cpp"
using namespace std;

int main() {
    // To count number of lines of data set, use : wc -l name_data_set.csv
    ULDataFrame df = dazc::read("/home/nightfury/CLionProjects/bdd.csv", 34551849);
    return 0;
}

