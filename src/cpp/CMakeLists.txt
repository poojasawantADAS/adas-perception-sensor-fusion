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


# Perception Core Library
add_library(perception_core
    perception/image_frame.cpp
    perception/perception_pipeline.cpp
)
target_include_directories(perception_core
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/perception
)
target_link_libraries(perception_core
    PUBLIC
        acc_decision
)


#Opencv + excecutable
find_package(OpenCV REQUIRED)

add_executable(adas_demo
    main.cpp
)

target_link_libraries(adas_demo
    PRIVATE
        perception_core
        acc_decision
        ${OpenCV_LIBS}
)

target_include_directories(adas_demo
    PRIVATE
        ${OpenCV_INCLUDE_DIRS}
)

