# specify version of Cmake
cmake_minimum_required(VERSION 3.20)

# set name for project
project(Security_Project)

# use C++ version 2017
set(CMAKE_CXX_STANDARD 17)

# Add all header-file (library) recursively to project

#file(GLOB_RECURSE HEADERS "DataFrame/*.hpp" "DataFrame/*.tcc")
add_subdirectory(library/DataFrame)
add_subdirectory(library/csv-parser)
#add_subdirectory(csv-parser)

# Add flags to optimize time execution
#https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html#
#set(CMAKE_CXX_FLAGS_RELEASE -O3 -lpthread )
set(CMAKE_CXX_FLAGS  "-pthread -Ofast")
#
#add_library(DataFrame INTERFACE)
#target_include_directories(DataFrame INTERFACE .)
#target_sources(DataFrame INTERFACE ${HEADERS})
#INCLUDE_DIRECTORIES(DataFrame)
#LINK_DIRECTORIES(DataFrame)

#target_link_libraries(run_main library)

# add main.cpp to project
# now we can run by click run_main in the toolbar
add_executable(run_main main.cpp)
add_executable(fix_dataset fix_dataset.cpp)
add_executable(csv17 csv17.cpp)

target_link_libraries(run_main library/DataFrame)
#target_link_libraries(fix_dataset csv)
