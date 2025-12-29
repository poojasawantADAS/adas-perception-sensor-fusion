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



## Planning to Control Flow

The planning module determines the desired vehicle behavior based on perceived
environment and driving goals. The controller converts planning decisions into
low-level actuation commands while ensuring smoothness and passenger comfort.
