// IO library  (input - output)
#include <iostream>

// Add library DataFrame
#include <DataFrame/DataFrame.h>
//#include <DataFrame/DataFrameFinancialVisitors.h>  // Financial algorithms
//#include <DataFrame/DataFrameMLVisitors.h>  // Machine-learning algorithms
#include <DataFrame/DataFrameStatsVisitors.h>  // Statistical algorithms

// more info: https://www.geeksforgeeks.org/namespace-in-c/
using namespace hmdf;
using namespace std;

// define the type of index of the table : unsigned long ( 1 2 3 ...)
// more info about "using" : https://www.educative.io/edpresso/what-is-the-using-keyword-in-cpp
// !!! ATTENTION : the data always have an INDEX column, if the data set doesn't have it,
// use gen_sequence_index
using ULDataFrame = StdDataFrame<unsigned long>;
//using StrDataFrame = StdDataFrame<std::string>;

unsigned long const number_of_lines = 34551849;
unsigned long const number_of_lines_for_test = 200;

int main() {
    ULDataFrame ul_df1;
    // create column index : from 0 -> N-1
//    ul_df1.load_data(ULDataFrame::gen_sequence_index(0, number_of_lines, 1 ));
    ul_df1.load_data(ULDataFrame::gen_sequence_index(0, number_of_lines_for_test, 1 ));

    // test dataset
    ul_df1.read("/home/nightfury/CLionProjects/test_bdd.csv", io_format::csv2, true);

    // real dataset
//    ul_df1.read("/Users/nightfury/CLionProjects/fixed_bdd.csv", io_format::csv2, true);

    ul_df1.remove_column("INDEX");
    // print to stdout
    ul_df1.write<std::ostream, int, string, double, double>(cout, io_format::csv2);
    return 0;
}
