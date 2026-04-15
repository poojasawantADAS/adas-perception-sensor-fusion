#pragma once
#include <array>
#include <chrono>
#include <vector>

// 5-state vector: [x, y, z, vx, vy]
// x, y, z = 3D position
// vx, vy  = velocity

struct Detection {
    float x, y, z;       // position from camera or lidar
    double timestamp;     // when was this detected
};

struct Track {
    int id;
    float x, y, z;       // fused position
    float vx, vy;        // estimated velocity
    double timestamp;
    int hits;            // how many times updated
};

class EKFTracker {
public:
    EKFTracker();

    // Feed a new detection — returns updated track
    Track update(const Detection& det);

    // Predict track forward in time
    void predict(double dt);

    // Get all active tracks
    const std::vector<Track>& getTracks() const;

    // Reset tracker
    void reset();

private:
    std::vector<Track> tracks_;
    int next_id_;

    // State: [x, y, z, vx, vy]
    std::array<float, 5> state_;

    // Process noise (how much we trust motion model)
    float process_noise_;

    // Measurement noise (how much we trust sensor)
    float measurement_noise_;

    bool isNewTrack(const Detection& det) const;
    Track initTrack(const Detection& det);
    void updateTrack(Track& track, const Detection& det);
};
