
def evaluate_candidate(score, completeness, attendance, assignment_submitted):
    # Original conditions
    if score < 70:
        return "FAIL", "Score is below 70."

    if not completeness:
        return "FAIL", "Required documentation is incomplete."

    # Two additional transparent conditions
    if attendance < 75:
        return "FAIL", "Attendance is below 75%."

    if not assignment_submitted:
        return "FAIL", "Required assignment was not submitted."

    return "PASS", "All requirements are satisfied."


test_cases = [
    {
        "name": "Test 1 - Pass at score boundary",
        "score": 70,
        "completeness": True,
        "attendance": 75,
        "assignment_submitted": True,
        "expected": "PASS"
    },
    {
        "name": "Test 2 - Attendance failure",
        "score": 85,
        "completeness": True,
        "attendance": 74,
        "assignment_submitted": True,
        "expected": "FAIL"
    },
    {
        "name": "Test 3 - Assignment failure",
        "score": 90,
        "completeness": True,
        "attendance": 90,
        "assignment_submitted": False,
        "expected": "FAIL"
    },
    {
        "name": "Test 4 - Score below boundary",
        "score": 69,
        "completeness": True,
        "attendance": 90,
        "assignment_submitted": True,
        "expected": "FAIL"
    }
]

print("RULE-BASED SYSTEM TEST RESULTS")
print("=" * 60)

for test in test_cases:
    actual, reason = evaluate_candidate(
        score=test["score"],
        completeness=test["completeness"],
        attendance=test["attendance"],
        assignment_submitted=test["assignment_submitted"]
    )

    print(f"\n{test['name']}")
    print(f"Input: {test}")
    print(f"Expected result: {test['expected']}")
    print(f"Actual result: {actual}")
    print(f"Reason: {reason}")
    print(f"Test passed: {actual == test['expected']}")
