//
// Created by nightfury on 10/8/21.
//
#include "DAZC.cpp"
using namespace std;

int main() {
    ULDataFrame df = dazc::read("/home/nightfury/CLionProjects/test_bdd.csv", 50);
    // test : print date-time's column
    vector<string> date_time = df.get_column<string>("DateTime");
    for (auto d : date_time) cout << d << " | \n";
    return 0;
}

