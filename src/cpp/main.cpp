#include <opencv2/opencv.hpp>
#include <chrono>
#include "perception/image_frame.hpp"
#include "perception/perception_pipeline.hpp"

int main() {
    cv::Mat img = cv::imread("test.jpg");
    if (img.empty()) {
        return -1;
    }

    auto now = std::chrono::steady_clock::now();
    ImageFrame frame(img, now);

    PerceptionPipeline pipeline;
    pipeline.process(frame);

    return 0;
}
