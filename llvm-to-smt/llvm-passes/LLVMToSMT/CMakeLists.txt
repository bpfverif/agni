cmake_minimum_required(VERSION 3.13.4)
project(llvm-to-smt)

#===============================================================================
# 1. LOAD LLVM CONFIGURATION
#===============================================================================
# Set this to a valid LLVM installation dir
set(LT_LLVM_INSTALL_DIR "" CACHE PATH "LLVM installation directory")

# Add the location of LLVMConfig.cmake to CMake search paths (so that
# find_package can locate it)
list(APPEND CMAKE_PREFIX_PATH "${LT_LLVM_INSTALL_DIR}/lib/cmake/llvm/")

find_package(LLVM 12.0.0 REQUIRED CONFIG)

# LLVMToSMT includes headers from LLVM - update the include paths accordingly
include_directories(SYSTEM ${LLVM_INCLUDE_DIRS})

#===============================================================================
# 2. LLVM-TUTOR BUILD CONFIGURATION
#===============================================================================
# Use the same C++ standard as LLVM does
set(CMAKE_CXX_STANDARD 14 CACHE STRING "")

# Build type
if (NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug CACHE
      STRING "Build type (default Debug):" FORCE)
endif()

# Compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall\
    -fdiagnostics-color=always")

# LLVM is normally built without RTTI. Be consistent with that.
if(NOT LLVM_ENABLE_RTTI)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-rtti")
endif()

set(CMAKE_BUILD_TYPE Debug)

#===============================================================================
# 3. ADD THE TARGET
#===============================================================================
add_library(LLVMToSMT SHARED BitvecHelper.cpp BVTree.cpp FunctionEncoder.cpp ModuleEncoder.cpp LLVMToSMT.cpp)

## CMakeGraphVizOptions.cmake
# add_custom_target(graphviz ALL
#     COMMAND ${CMAKE_COMMAND} "--graphviz=foo.dot" .
#     COMMAND dot -Tpng foo.dot -o foo.png
#     WORKING_DIRECTORY "${CMAKE_BINARY_DIR}"
# )

target_link_libraries(LLVMToSMT -lz3 -ljsoncpp)

# Allow undefined symbols in shared objects on Darwin (this is the default
# behaviour on Linux)
target_link_libraries(LLVMToSMT
  "$<$<PLATFORM_ID:Darwin>:-undefined dynamic_lookup>")
