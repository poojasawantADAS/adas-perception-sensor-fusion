#pragma once

#include <opencv2/opencv.hpp>
#include <chrono>

class ImageFrame {
public:
    using TimePoint = std::chrono::steady_clock::time_point;

    ImageFrame(const cv::Mat& img, TimePoint ts);

    const cv::Mat& image() const;
    TimePoint timestamp() const;

private:
    cv::Mat image_;
    TimePoint timestamp_;
};
