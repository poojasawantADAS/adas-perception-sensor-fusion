class ACCDecision:
    def __init__(self,
                 safe_distance=30.0,
                 critical_distance=15.0):
        self.safe_distance = safe_distance
        self.critical_distance = critical_distance

    def decide(self,
               ego_speed,
               lead_distance,
               relative_velocity):
        """
        Decide ACC action based on distance and relative speed.

        Inputs:
        - ego_speed: current vehicle speed (m/s)
        - lead_distance: distance to lead vehicle (m)
        - relative_velocity: relative speed to lead vehicle (m/s)

        Output:
        - action: Maintain Speed / Slow Down / Brake
        """

        if lead_distance is None:
            return "Maintain Speed"

        if lead_distance > self.safe_distance:
            return "Maintain Speed"

        elif self.critical_distance < lead_distance <= self.safe_distance:
            if relative_velocity < 0:
                return "Slow Down"
            else:
                return "Maintain Speed"

        else:
            return "Brake"

if __name__ == "__main__":
    acc = ACCDecision()

    scenarios = [
        {"dist": 50, "rel_vel": -2},
        {"dist": 25, "rel_vel": -3},
        {"dist": 10, "rel_vel": -5},
        {"dist": None, "rel_vel": 0}
    ]

    for s in scenarios:
        action = acc.decide(
            ego_speed=20,
            lead_distance=s["dist"],
            relative_velocity=s["rel_vel"]
        )
        print(f"Distance: {s['dist']}, Action: {action}")
