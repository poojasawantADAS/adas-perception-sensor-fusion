add_executable(adas_perception_app
    cpp/main.cpp
    cpp/perception/image_frame.cpp
    cpp/perception/perception_pipeline.cpp
)

target_include_directories(adas_perception_app
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/cpp/perception
)
