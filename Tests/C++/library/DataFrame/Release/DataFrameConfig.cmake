set (DataFrame_VERSION 1.0.0)


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was DataFrameConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

####################################################################################



if (NOT TARGET DataFrame::DataFrame)
  include("${CMAKE_CURRENT_LIST_DIR}/DataFrameTargets.cmake")
endif()

# Compatibility
get_property(DataFrame_DataFrame_INCLUDE_DIR TARGET DataFrame::DataFrame PROPERTY INTERFACE_INCLUDE_DIRECTORIES)

set(DataFrame_LIBRARIES DataFrame::DataFrame)
set(DataFrame_INCLUDE_DIRS "${DataFrame_DataFrame_INCLUDE_DIR}")
list(REMOVE_DUPLICATES DataFrame_INCLUDE_DIRS)


