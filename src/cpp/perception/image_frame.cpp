#include "image_frame.hpp"

ImageFrame::ImageFrame(const cv::Mat& img, TimePoint ts)
    : image_(img.clone()), timestamp_(ts) {}

const cv::Mat& ImageFrame::image() const {
    return image_;
}

ImageFrame::TimePoint ImageFrame::timestamp() const {
    return timestamp_;
}
