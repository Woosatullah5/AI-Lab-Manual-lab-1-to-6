"""Lab 2 - Task 1: PEAS specifications for two intelligent agents."""

def print_peas(title, peas):
    print(f"\n{title}")
    print("-" * len(title))
    for component, entries in peas.items():
        print(f"{component}:")
        for entry in entries:
            print(f"  - {entry}")

delivery_robot = {
    "Performance measure": [
        "Deliver the correct parcel to the correct destination",
        "Avoid collisions and protect people",
        "Deliver on time while minimizing energy use",
    ],
    "Environment": [
        "Homes, offices, corridors, lifts, pavements and delivery locations",
        "People, pets, doors, obstacles, weather and other robots",
    ],
    "Actuators": [
        "Drive motors and steering",
        "Brakes, robotic arm or parcel compartment lock",
        "Speaker, display and status lights",
    ],
    "Sensors": [
        "Cameras and depth/proximity sensors",
        "Wheel encoders, GPS where available, IMU",
        "Parcel ID scanner and battery/door sensors",
    ],
}

student_support_agent = {
    "Performance measure": [
        "Give accurate, relevant and understandable study guidance",
        "Protect student privacy and avoid unsupported claims",
        "Escalate sensitive, ambiguous or high-stakes issues to staff",
    ],
    "Environment": [
        "Student questions, course materials and approved learning platform",
        "Instructor policies, deadlines and available support resources",
    ],
    "Actuators": [
        "Text responses and links to approved resources",
        "Ask clarifying questions",
        "Create a support ticket or refer to staff when authorized",
    ],
    "Sensors": [
        "Student's current message and conversation context",
        "Approved course documents and knowledge base",
        "Tool results from explicitly authorized systems",
    ],
}

if __name__ == "__main__":
    print_peas("PEAS 1: DELIVERY ROBOT", delivery_robot)
    print_peas("PEAS 2: LLM-BASED STUDENT-SUPPORT AGENT", student_support_agent)
    print("\nOperational assumptions:")
    print("- The delivery robot can use navigation and obstacle-detection sensors.")
    print("- The student-support agent can read approved course materials only.")
    print("- It cannot access grades, private records, email, or submit changes unless")
    print("  an explicitly authorized tool grants that access.")
    print("\nTrade-off:")
    print("- More sensing and repeated checks can improve safety, but may increase")
    print("  latency, energy use, and operating cost.")
