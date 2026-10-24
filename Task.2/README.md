# Lab 2 - Python Files

## Files
- `lab2_peas.py`: PEAS specifications for a delivery robot and an LLM-based student-support agent.
- `lab2_model.py`: Stateful temperature/occupancy controller that remembers the previous mode and avoids duplicate commands.
- `lab2_check.py`: Reproducible test cases for repeated percepts, exact boundaries, mode transitions, and an empty-room case.

## Requirements
Python 3. No third-party packages are required.

## Run
```bash
python lab2_peas.py
python lab2_model.py
python lab2_check.py
```

## Assumptions to verify
The controller uses 18 C and 26 C thresholds, and an empty room takes priority over temperature. If your earlier Lab 1 code uses different thresholds or a different occupancy rule, update the constants/rule in `lab2_model.py` and adjust expected values in `lab2_check.py`.
