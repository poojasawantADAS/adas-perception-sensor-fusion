#pragma once
#include <chrono>
#include <deque>
#include <optional>
#include "../perception/image_frame.hpp"
#include "../lidar/lidar_frame.hpp"

struct SyncedPair {
    ImageFrame  camera;
    LidarFrame  lidar;
};

class TimestampSync {
public:
    // 50ms max allowed difference between camera and lidar
    static constexpr double MAX_SYNC_GAP_MS = 50.0;

    void addCameraFrame(const ImageFrame& frame);
    void addLidarFrame(const LidarFrame& frame);

    // Returns a matched pair if one exists within 50ms
    std::optional<SyncedPair> trySync();

    int queueSize() const;

private:
    std::deque<ImageFrame> camera_queue_;
    std::deque<LidarFrame> lidar_queue_;

    double toMilliseconds(
        const ImageFrame::TimePoint& a,
        const LidarFrame::TimePoint& b) const;
};
