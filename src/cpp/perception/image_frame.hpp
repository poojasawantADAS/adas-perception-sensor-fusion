#pragma once
#include <chrono>

class ImageFrame {
public:
    using TimePoint = std::chrono::steady_clock::time_point;

    explicit ImageFrame(TimePoint timestamp);

    TimePoint timestamp() const;

private:
    TimePoint timestamp_;
};
