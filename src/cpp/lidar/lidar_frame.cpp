#include "lidar_frame.hpp"
#include <cmath>

LidarFrame::LidarFrame(TimePoint timestamp)
    : timestamp_(timestamp) {}

LidarFrame::TimePoint LidarFrame::timestamp() const {
    return timestamp_;
}

void LidarFrame::addPoint(float x, float y, float z) {
    points_.push_back({x, y, z});
}

const std::vector<Point3D>& LidarFrame::points() const {
    return points_;
}

std::vector<Point3D> LidarFrame::getCentroids() const {
    if (points_.empty()) return {};
    
    Point3D centroid{0, 0, 0};
    for (const auto& p : points_) {
        centroid.x += p.x;
        centroid.y += p.y;
        centroid.z += p.z;
    }
    float n = static_cast<float>(points_.size());
    centroid.x /= n;
    centroid.y /= n;
    centroid.z /= n;
    
    return {centroid};
}
