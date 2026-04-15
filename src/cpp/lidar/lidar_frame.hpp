#pragma once
#include <chrono>
#include <vector>

struct Point3D {
    float x, y, z;
};

class LidarFrame {
public:
    using TimePoint = std::chrono::steady_clock::time_point;

    explicit LidarFrame(TimePoint timestamp);

    TimePoint timestamp() const;
    void addPoint(float x, float y, float z);
    const std::vector<Point3D>& points() const;
    std::vector<Point3D> getCentroids() const;

private:
    TimePoint timestamp_;
    std::vector<Point3D> points_;
};
