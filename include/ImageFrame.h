#pragma once
#include <vector>
#include <cstdint>
#include <string>

class ImageFrame {
public:
    ImageFrame(int width, int height, double timestamp);

    int getWidth() const;
    int getHeight() const;
    double getTimestamp() const;
    std::string getInfo() const;

private:
    int width_;
    int height_;
    double timestamp_;
    std::vector<uint8_t> pixels_;
};

