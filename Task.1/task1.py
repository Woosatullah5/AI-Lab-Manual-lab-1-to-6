
timeline = [
    {
        "year": "1950",
        "event": "Turing Test",
        "significance": "Alan Turing proposed a test for evaluating machine intelligence through conversation.",
        "source": "https://doi.org/10.1093/mind/LIX.236.433"
    },
    {
        "year": "1956",
        "event": "Dartmouth AI Workshop",
        "significance": "The Dartmouth workshop helped establish artificial intelligence as a research field.",
        "source": "https://home.dartmouth.edu/about/artificial-intelligence-ai-coined-dartmouth"
    },
    {
        "year": "1974-1980",
        "event": "First AI Winter",
        "significance": "Reduced funding and unmet expectations slowed progress in several AI research areas.",
        "source": "https://www.britannica.com/technology/artificial-intelligence"
    },
    {
        "year": "1997",
        "event": "Deep Blue",
        "significance": "IBM's Deep Blue defeated world chess champion Garry Kasparov in a match.",
        "source": "https://www.ibm.com/history/deep-blue"
    },
    {
        "year": "2012",
        "event": "AlexNet",
        "significance": "A deep neural network achieved a major breakthrough in the ImageNet image-recognition competition.",
        "source": "https://doi.org/10.1145/3065386"
    },
    {
        "year": "2017",
        "event": "Transformer Architecture",
        "significance": "The Transformer introduced an attention-based architecture that became influential in modern language models.",
        "source": "https://doi.org/10.48550/arXiv.1706.03762"
    },
    {
        "year": "2020",
        "event": "Large-Scale Language Models",
        "significance": "GPT-3 demonstrated the capabilities of language models trained at large scale.",
        "source": "https://doi.org/10.48550/arXiv.2005.14165"
    }
]

print("AI MILESTONES TIMELINE")
print("=" * 70)

for milestone in timeline:
    print(f"\nYear/Period: {milestone['year']}")
    print(f"Event: {milestone['event']}")
    print(f"Significance: {milestone['significance']}")
    print(f"Source: {milestone['source']}")
