#include "ImageFrame.h"
#include <sstream>

ImageFrame::ImageFrame(int width, int height, double timestamp)
    : width_(width), height_(height), timestamp_(timestamp),
      pixels_(width * height, 0) {}

int ImageFrame::getWidth() const { return width_; }
int ImageFrame::getHeight() const { return height_; }
double ImageFrame::getTimestamp() const { return timestamp_; }

std::string ImageFrame::getInfo() const {
    std::ostringstream oss;
    oss << "ImageFrame: " << width_ << "x" << height_
        << ", timestamp=" << timestamp_;
    return oss.str();
}
