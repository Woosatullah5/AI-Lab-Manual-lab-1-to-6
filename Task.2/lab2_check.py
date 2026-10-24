"""Lab 2 - Task 3: Reproducible checks for the stateful controller."""

from lab2_model import StatefulController


def run_case(name, controller, temperature, occupied, expected_target, expected_send):
    result = controller.process(temperature, occupied)
    passed = (
        result["target_mode"] == expected_target
        and result["command_should_be_sent"] == expected_send
    )
    print(f"{name}")
    print(
        f"  input=(temperature={temperature}, occupied={occupied}), "
        f"previous={result['previous_mode']}"
    )
    print(
        f"  expected=(target={expected_target}, send={expected_send})"
    )
    print(
        f"  actual=(target={result['target_mode']}, "
        f"send={result['command_should_be_sent']}, "
        f"command={result['command']})"
    )
    print(f"  result={'PASS' if passed else 'FAIL'}\n")
    return passed


def main():
    controller = StatefulController(previous_mode="OFF")
    results = []

    # Mode transition: OFF -> HEAT.
    results.append(run_case(
        "1. Cold occupied room", controller, 16, True, "HEAT", True
    ))

    # Same target and same mode: suppress duplicate command.
    results.append(run_case(
        "2. Repeated percept", controller, 16, True, "HEAT", False
    ))

    # Exact lower boundary.
    results.append(run_case(
        "3. Exact lower threshold", controller, 18, True, "OFF", True
    ))

    # Exact upper boundary; mode is already OFF, so no command.
    results.append(run_case(
        "4. Exact upper threshold", controller, 26, True, "OFF", False
    ))

    # Mode transition: OFF -> COOL.
    results.append(run_case(
        "5. Warm occupied room", controller, 29, True, "COOL", True
    ))

    # Empty-room priority: COOL -> OFF even though temperature is warm.
    results.append(run_case(
        "6. Empty room", controller, 29, False, "OFF", True
    ))

    # Empty room is already OFF: no command.
    results.append(run_case(
        "7. Empty room remains OFF", controller, 22, False, "OFF", False
    ))

    print(f"Summary: {sum(results)}/{len(results)} tests passed.")
    if not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
