#include "ekf_tracker.hpp"
#include <cmath>
#include <iostream>

EKFTracker::EKFTracker()
    : next_id_(0)
    , process_noise_(0.1f)
    , measurement_noise_(0.5f)
{
    state_ = {0, 0, 0, 0, 0};
}

bool EKFTracker::isNewTrack(const Detection& det) const {
    if (tracks_.empty()) return true;

    // If detection is far from all existing tracks — it's a new object
    for (const auto& track : tracks_) {
        float dx = track.x - det.x;
        float dy = track.y - det.y;
        float dz = track.z - det.z;
        float dist = std::sqrt(dx*dx + dy*dy + dz*dz);
        if (dist < 2.0f) return false; // within 2 meters = same object
    }
    return true;
}

Track EKFTracker::initTrack(const Detection& det) {
    Track t;
    t.id        = next_id_++;
    t.x         = det.x;
    t.y         = det.y;
    t.z         = det.z;
    t.vx        = 0.0f;
    t.vy        = 0.0f;
    t.timestamp = det.timestamp;
    t.hits      = 1;
    return t;
}

void EKFTracker::updateTrack(Track& track, const Detection& det) {
    // Kalman Gain — blend between prediction and measurement
    float K = process_noise_ / (process_noise_ + measurement_noise_);

    // Update position using Kalman gain
    float prev_x = track.x;
    float prev_y = track.y;

    track.x = track.x + K * (det.x - track.x);
    track.y = track.y + K * (det.y - track.y);
    track.z = track.z + K * (det.z - track.z);

    // Estimate velocity
    double dt = det.timestamp - track.timestamp;
    if (dt > 0.0) {
        track.vx = (track.x - prev_x) / static_cast<float>(dt);
        track.vy = (track.y - prev_y) / static_cast<float>(dt);
    }

    track.timestamp = det.timestamp;
    track.hits++;
}

Track EKFTracker::update(const Detection& det) {
    if (isNewTrack(det)) {
        Track t = initTrack(det);
        tracks_.push_back(t);
        return t;
    }

    // Find closest track and update it
    float min_dist = 1e9f;
    Track* closest = nullptr;

    for (auto& track : tracks_) {
        float dx = track.x - det.x;
        float dy = track.y - det.y;
        float dz = track.z - det.z;
        float dist = std::sqrt(dx*dx + dy*dy + dz*dz);
        if (dist < min_dist) {
            min_dist = dist;
            closest = &track;
        }
    }

    updateTrack(*closest, det);
    return *closest;
}

void EKFTracker::predict(double dt) {
    // Move each track forward using velocity
    for (auto& track : tracks_) {
        track.x += track.vx * static_cast<float>(dt);
        track.y += track.vy * static_cast<float>(dt);
    }
}

const std::vector<Track>& EKFTracker::getTracks() const {
    return tracks_;
}

void EKFTracker::reset() {
    tracks_.clear();
    next_id_ = 0;
}
