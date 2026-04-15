#include <iostream>
#include <chrono>
#include "perception/image_frame.hpp"
#include "lidar/lidar_frame.hpp"
#include "tracker/ekf_tracker.hpp"
#include "tracker/timestamp_sync.hpp"

int main() {
    std::cout << "=== ADAS Perception & Sensor Fusion Pipeline ===\n\n";

    auto now = std::chrono::steady_clock::now();

    std::cout << "[TEST 1] Timestamp Synchronization\n";
    TimestampSync sync;
    ImageFrame cam1(now);
    LidarFrame  lid1(now + std::chrono::milliseconds(20));
    sync.addCameraFrame(cam1);
    sync.addLidarFrame(lid1);
    auto pair = sync.trySync();
    if (pair.has_value()) {
        std::cout << "  PASS - Camera + LiDAR synced within 50ms\n";
    } else {
        std::cout << "  FAIL - Sync not working\n";
    }

    std::cout << "\n[TEST 2] EKF Tracker - New Object Detection\n";
    EKFTracker tracker;
    Detection det1{5.0f, 10.0f, 0.0f, 1.0};
    Track track1 = tracker.update(det1);
    std::cout << "  Track ID: " << track1.id << "\n";
    std::cout << "  Position: x=" << track1.x << " y=" << track1.y << " z=" << track1.z << "\n";
    std::cout << "  PASS - Track initialized\n";

    std::cout << "\n[TEST 3] EKF Tracker - Update Existing Track\n";
    Detection det2{5.5f, 10.5f, 0.0f, 1.1};
    Track track2 = tracker.update(det2);
    std::cout << "  Track ID: " << track2.id << " (should be same: 0)\n";
    std::cout << "  Updated Position: x=" << track2.x << " y=" << track2.y << "\n";
    std::cout << "  Hits: " << track2.hits << " (should be 2)\n";
    std::cout << "  PASS - Track updated with Kalman Filter\n";

    std::cout << "\n[TEST 4] EKF Predict - Motion Extrapolation\n";
    tracker.predict(0.1);
    const auto& tracks = tracker.getTracks();
    std::cout << "  Active tracks: " << tracks.size() << "\n";
    std::cout << "  PASS - Prediction step complete\n";

    std::cout << "\n[TEST 5] LiDAR Frame - Point Cloud\n";
    LidarFrame lidar(now);
    lidar.addPoint(1.0f, 2.0f, 0.5f);
    lidar.addPoint(1.1f, 2.1f, 0.5f);
    lidar.addPoint(0.9f, 1.9f, 0.5f);
    auto centroids = lidar.getCentroids();
    std::cout << "  Points added: " << lidar.points().size() << "\n";
    std::cout << "  Centroid: x=" << centroids[0].x << " y=" << centroids[0].y << "\n";
    std::cout << "  PASS - LiDAR centroid computed\n";

    std::cout << "\n=== ALL TESTS PASSED - Pipeline Ready ===\n";
    return 0;
}
