# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.18

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame/Release

# Include any dependencies generated for this target.
include CMakeFiles/hello_world.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/hello_world.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/hello_world.dir/flags.make

CMakeFiles/hello_world.dir/test/hello_world.cc.o: CMakeFiles/hello_world.dir/flags.make
CMakeFiles/hello_world.dir/test/hello_world.cc.o: ../test/hello_world.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame/Release/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/hello_world.dir/test/hello_world.cc.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/hello_world.dir/test/hello_world.cc.o -c /home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame/test/hello_world.cc

CMakeFiles/hello_world.dir/test/hello_world.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/hello_world.dir/test/hello_world.cc.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame/test/hello_world.cc > CMakeFiles/hello_world.dir/test/hello_world.cc.i

CMakeFiles/hello_world.dir/test/hello_world.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/hello_world.dir/test/hello_world.cc.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame/test/hello_world.cc -o CMakeFiles/hello_world.dir/test/hello_world.cc.s

# Object files for target hello_world
hello_world_OBJECTS = \
"CMakeFiles/hello_world.dir/test/hello_world.cc.o"

# External object files for target hello_world
hello_world_EXTERNAL_OBJECTS =

bin/hello_world: CMakeFiles/hello_world.dir/test/hello_world.cc.o
bin/hello_world: CMakeFiles/hello_world.dir/build.make
bin/hello_world: lib/libDataFrame.a
bin/hello_world: CMakeFiles/hello_world.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame/Release/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable bin/hello_world"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/hello_world.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/hello_world.dir/build: bin/hello_world

.PHONY : CMakeFiles/hello_world.dir/build

CMakeFiles/hello_world.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/hello_world.dir/cmake_clean.cmake
.PHONY : CMakeFiles/hello_world.dir/clean

CMakeFiles/hello_world.dir/depend:
	cd /home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame/Release && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame /home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame /home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame/Release /home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame/Release /home/nightfury/CLionProjects/SecuProject/Tests/C++/library/DataFrame/Release/CMakeFiles/hello_world.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/hello_world.dir/depend

