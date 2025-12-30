#include "acc_decision.hpp"

AccDecision::AccDecision(double safeDist, double criticalDist)
    : safeDistance(safeDist),
      criticalDistance(criticalDist) {}

AccAction AccDecision::decide(double,
                              double leadDistance,
                              double relativeVelocity) const {
    if (leadDistance < 0) {
        return AccAction::MaintainSpeed;
    }

    if (leadDistance > safeDistance) {
        return AccAction::MaintainSpeed;
    }

    if (leadDistance > criticalDistance && relativeVelocity < 0) {
        return AccAction::SlowDown;
    }

    return AccAction::Brake;
}
