# specify version of Cmake
cmake_minimum_required(VERSION 3.20)

# set name for project
project(Security_Project)

# use C++ version 2017
set(CMAKE_CXX_STANDARD 17)

# Add all header-file (library) recursively to project
add_subdirectory(library/DataFrame)

#set(HEADERS library/DAZC.hpp library/csv.hpp)
#add_library(dazc STATIC ${HEADERS})


# Add flags to optimize time execution
#https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html#
#set(CMAKE_CXX_FLAGS_RELEASE -O3 -lpthread )
set(CMAKE_CXX_FLAGS  "-pthread -Ofast")

# add main.cpp to project
# now we can run by click run_main in the toolbar
#add_executable(run_main main.cpp)
#add_executable(fix_dataset fix_dataset.cpp)
#add_executable(csv17 csv17.cpp)

add_executable(run_save_main save_main.cpp)
add_executable(run_main main.cpp)
add_executable(fix_dataset fix_dataset.cpp)
add_executable(csv17  csv17.cpp)
add_executable(dazc DAZC.cpp)

target_link_libraries(run_save_main DataFrame)
target_link_libraries(run_main DataFrame)
target_link_libraries(csv17 DataFrame)
target_link_libraries(fix_dataset DataFrame)
target_link_libraries(dazc DataFrame)


#target_link_libraries(run_main dazc)

