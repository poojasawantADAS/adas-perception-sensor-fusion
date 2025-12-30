cmake_minimum_required(VERSION 3.16)

project(adas_cpp_modules LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Library for ACC decision logic
add_library(acc_decision
    decision/acc_decision.cpp
)

target_include_directories(acc_decision
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/decision
)
