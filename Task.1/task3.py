comparison = {
    "topic": "Conversational Test vs General Intelligence",
    "conversational_test_observes": (
        "Whether a machine can produce conversational responses "
        "that are difficult to distinguish from human responses."
    ),
    "what_it_does_not_prove": (
        "Passing a conversational test does not establish broad "
        "reasoning ability, genuine understanding, or reliable "
        "performance across different tasks."
    ),
    "fluent_but_incorrect_example": (
        "A chatbot may confidently explain a mathematical problem "
        "but provide an incorrect calculation."
    ),
    "additional_reliability_test": (
        "Evaluate the system on unseen problems with objectively "
        "verifiable answers, repeated trials, and an accuracy score."
    ),
    "historical_claims": [
        {
            "claim": "Alan Turing proposed the imitation game in 1950.",
            "source": "https://doi.org/10.1093/mind/LIX.236.433"
        },
        {
            "claim": (
                "John Searle introduced the Chinese Room argument "
                "in 1980 to challenge claims about understanding."
            ),
            "source": "https://doi.org/10.1017/S0140525X00005756"
        }
    ]
}

print("CONVERSATIONAL TEST AND GENERAL INTELLIGENCE")
print("=" * 60)

for key, value in comparison.items():
    print(f"\n{key.replace('_', ' ').title()}:")

    if isinstance(value, list):
        for item in value:
            for claim_key, claim_value in item.items():
                print(f"  {claim_key.title()}: {claim_value}")
            print()
    else:
        print(value)
