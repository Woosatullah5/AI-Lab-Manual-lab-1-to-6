"""Lab 2 - Task 3: Stateful temperature/occupancy controller.

Assumptions:
- HEAT when occupied and temperature is below 18 C.
- COOL when occupied and temperature is above 26 C.
- OFF at both exact boundaries and between the thresholds.
- Occupancy has priority: an empty room always targets OFF.
- A command is sent only when the target differs from the previous mode.
- Change LOW_THRESHOLD/HIGH_THRESHOLD if your Lab 1 code used other values.
"""

LOW_THRESHOLD = 18.0
HIGH_THRESHOLD = 26.0


class StatefulController:
    def __init__(self, previous_mode="OFF"):
        valid_modes = {"HEAT", "COOL", "OFF"}
        if previous_mode not in valid_modes:
            raise ValueError(f"previous_mode must be one of {valid_modes}")
        self.previous_mode = previous_mode

    def choose_target(self, temperature, occupied):
        if not isinstance(temperature, (int, float)):
            raise TypeError("temperature must be a number")
        if isinstance(temperature, bool):
            raise TypeError("temperature must be a number, not bool")
        if not isinstance(occupied, bool):
            raise TypeError("occupied must be True or False")

        # Occupancy priority is checked first.
        if not occupied:
            return "OFF"
        if temperature < LOW_THRESHOLD:
            return "HEAT"
        if temperature > HIGH_THRESHOLD:
            return "COOL"
        return "OFF"

    def process(self, temperature, occupied):
        old_mode = self.previous_mode
        target_mode = self.choose_target(temperature, occupied)
        command_should_be_sent = target_mode != old_mode

        if command_should_be_sent:
            self.previous_mode = target_mode

        return {
            "temperature": temperature,
            "occupied": occupied,
            "previous_mode": old_mode,
            "target_mode": target_mode,
            "command_should_be_sent": command_should_be_sent,
            "command": target_mode if command_should_be_sent else "NO COMMAND",
            "mode_after_processing": self.previous_mode,
        }


if __name__ == "__main__":
    controller = StatefulController(previous_mode="OFF")
    sample_percepts = [
        (16, True),   # Transition OFF -> HEAT
        (16, True),   # Repeated percept: no repeated command
        (18, True),   # Exact lower boundary: target OFF
        (26, True),   # Exact upper boundary: remains OFF
        (29, True),   # Transition OFF -> COOL
        (29, True),   # Repeated percept: no repeated command
        (22, False),  # Empty room overrides temperature: COOL -> OFF
    ]

    print("STATEFUL CONTROLLER TRACE")
    print("=" * 88)
    for number, (temperature, occupied) in enumerate(sample_percepts, start=1):
        result = controller.process(temperature, occupied)
        print(
            f"Case {number}: previous={result['previous_mode']}, "
            f"temperature={result['temperature']} C, "
            f"occupied={result['occupied']}, "
            f"target={result['target_mode']}, "
            f"command={result['command']}, "
            f"send={result['command_should_be_sent']}, "
            f"mode_after={result['mode_after_processing']}"
        )
