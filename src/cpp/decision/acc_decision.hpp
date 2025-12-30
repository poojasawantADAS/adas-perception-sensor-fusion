#pragma once

enum class AccAction {
    MaintainSpeed,
    SlowDown,
    Brake
};

class AccDecision {
public:
    AccDecision(double safeDist = 30.0,
                double criticalDist = 15.0);

    AccAction decide(double egoSpeed,
                     double leadDistance,
                     double relativeVelocity) const;

private:
    double safeDistance;
    double criticalDistance;
};
