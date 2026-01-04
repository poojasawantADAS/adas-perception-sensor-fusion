//#include <opencv2/opencv.hpp>

#include <iostream>
#include <chrono>
#include "perception/image_frame.hpp"
#include "perception/perception_pipeline.hpp"


int main()
{
    std::cout << "ADAS Perception App started\n";

    // Temporary stub image/frame (no OpenCV yet)
    auto now = std::chrono::steady_clock::now();

    ImageFrame frame(now);   // constructor WITHOUT cv::Mat
    PerceptionPipeline pipeline;
    pipeline.process(frame);

    std::cout << "ADAS Perception App finished\n";
    return 0;
}
