cmake_minimum_required(VERSION 3.16)

project(ADAS_Perception_Sensor_Fusion
    VERSION 1.0
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

#set(OpenCV_DIR "C:/opencv/build/x64/vc16")
#set(OpenCV_DIR "C:/opencv/build")
#set(OpenCV_RUNTIME "vc16/x64")
find_package(OpenCV REQUIRED)


# Enable good compile warnings (optional but recommended)
if (MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Add subdirectories
add_subdirectory(src)
