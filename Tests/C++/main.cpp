//
// Created by nightfury on 10/8/21.
//
#include "DAZC.cpp"

using namespace std;

int main() {
    // To count number of lines of data set, use : wc -l name_data_set.csv
//    ULDataFrame df = dazc::read("/home/nightfury/CLionProjects/bdd.csv", 34551849);

    // Generate test file :
    dazc::generate_small_data_set("/home/nightfury/CLionProjects/bdd.csv",
                                  "/home/nightfury/CLionProjects/small_data_set.csv", 200);
    // For test's purpose
//    ULDataFrame df = dazc::read("/home/nightfury/CLionProjects/bdd.csv", 34551849);
//    dazc::write(df, "/home/nightfury/CLionProjects/output.csv");
    return 0;
}

