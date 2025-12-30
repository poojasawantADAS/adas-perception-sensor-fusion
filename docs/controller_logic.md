# Controller Algorithms in ADAS

## Adaptive Cruise Control (ACC)

Adaptive Cruise Control is a longitudinal control function that maintains a safe
distance from a lead vehicle while attempting to keep a driver-set target speed.

### Inputs
- Ego vehicle speed
- Relative distance to lead vehicle
- Relative velocity

### Decision Logic
If no lead vehicle is detected, the system maintains the set speed. If a lead
vehicle is detected and the distance reduces below a safe threshold, the system
reduces speed or applies braking to maintain safety.

### Outputs
- Throttle command
- Brake command



## Safety and Standards Considerations

Adaptive Cruise Control (ACC) is a safety-related driver assistance function.
System-level safety requirements for ACC are typically derived in accordance
with ISO 26262 to ensure that the system behaves safely in the presence of
sensor faults, incorrect detections, or unexpected operating conditions.

Potential hazards such as unintended acceleration, delayed braking, or
incorrect lead vehicle detection are analyzed at the system level, and
appropriate safety mechanisms (e.g., fallback strategies, driver warnings,
or controlled deactivation) are defined.

In addition to functional safety, ACC performance limitations related to
sensor perception and environmental conditions are considered under
ISO 21448 (Safety of the Intended Functionality, SOTIF). This includes
scenarios where sensors provide valid data but the perception output may
still be insufficient or uncertain.

The controller logic described in this project represents a simplified
functional view and does not replace production-level safety validation
or certification processes.


## Planning to Control Flow for our project

The planning module determines the desired vehicle behavior based on perceived
environment and driving goals. The controller converts planning decisions into
low-level actuation commands while ensuring smoothness and passenger comfort.

**Note**  : The ACC decision logic is implemented in both Python 3.10.x and C++20 to reflect typical ADAS development workflows
