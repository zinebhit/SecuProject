#include "library/csv.hpp"

using namespace csv;
using namespace std;

int main() {
    CSVReader reader("../../run_results.csv");
    vector <ofstream> list_file;
    ofstream new_file("../../new_results.csv", ofstream::trunc);

    for (CSVRow& row: reader) { // Input iterator
        for (CSVField& field: row) {
            // By default, get<>() produces a std::string.
            // A more efficient get<string_view>() is also available, where the resulting
            // string_view is valid as long as the parent CSVRow is alive
            new_file << field.get<string_view>() << " " ;
        }
        new_file << '\n';
    }
    new_file.close();

    return 0;
}