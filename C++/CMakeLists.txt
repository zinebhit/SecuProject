cmake_minimum_required(VERSION 3.20.2)
project(Security Project)

#set(CMAKE_Project_COMPILER "usr/bin/clang")
set(CMAKE_Project_COMPILER "usr/bin/gcc")
ADD_DEFINITIONS(-std=c++17)

add_executable(run_main main.cpp)

#set(THREADS_PREFER_PTHREAD_FLAG ON)
#find_package(Threads REQUIRED)
#target_link_libraries(generate_md_file PRIVATE Threads::Threads)

#target_link_libraries(run_main ../library/csv.hpp)