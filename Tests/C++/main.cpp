// IO library  (input - output)
#include <iostream>

// Add library DataFrame
#include "DataFrame/DataFrame.h"
#include <DataFrame/DataFrameFinancialVisitors.h>  // Financial algorithms
#include <DataFrame/DataFrameMLVisitors.h>  // Machine-learning algorithms
#include <DataFrame/DataFrameStatsVisitors.h>  // Statistical algorithms

// more info: https://www.geeksforgeeks.org/namespace-in-c/
using namespace hmdf;
using namespace std;

// define the type of index of the table : unsigned long ( 1 2 3 ...)
// more info about "using" : https://www.educative.io/edpresso/what-is-the-using-keyword-in-cpp
using ULDataFrame = StdDataFrame<unsigned long>;
//using StrDataFrame = StdDataFrame<std::string>;

int main() {
    ULDataFrame ul_df1;
    ul_df1.read("../../../bdd.csv", io_format::csv2);
    // print to stdout
    ul_df1.write<std::ostream, int, string, string, string>(cout, io_format::csv2);
    return 0;
}
