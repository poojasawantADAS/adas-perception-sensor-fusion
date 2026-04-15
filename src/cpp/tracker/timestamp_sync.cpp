#include "timestamp_sync.hpp"
#include <cmath>

void TimestampSync::addCameraFrame(const ImageFrame& frame) {
    camera_queue_.push_back(frame);
}

void TimestampSync::addLidarFrame(const LidarFrame& frame) {
    lidar_queue_.push_back(frame);
}

double TimestampSync::toMilliseconds(
    const ImageFrame::TimePoint& a,
    const LidarFrame::TimePoint& b) const {

    auto diff = std::chrono::duration_cast<std::chrono::microseconds>(a - b);
    return std::abs(diff.count() / 1000.0);
}

std::optional<SyncedPair> TimestampSync::trySync() {
    if (camera_queue_.empty() || lidar_queue_.empty()) {
        return std::nullopt;
    }

    const auto& cam   = camera_queue_.front();
    const auto& lidar = lidar_queue_.front();

    double gap_ms = toMilliseconds(cam.timestamp(), lidar.timestamp());

    if (gap_ms <= MAX_SYNC_GAP_MS) {
        // Good match — return the pair and remove from queues
        SyncedPair pair{cam, lidar};
        camera_queue_.pop_front();
        lidar_queue_.pop_front();
        return pair;
    }

    // Drop the older frame and wait for better match
    if (cam.timestamp() < lidar.timestamp()) {
        camera_queue_.pop_front();
    } else {
        lidar_queue_.pop_front();
    }

    return std::nullopt;
}

int TimestampSync::queueSize() const {
    return static_cast<int>(
        camera_queue_.size() + lidar_queue_.size());
}
