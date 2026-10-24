import re

samples = [
    "AI, search!",
    "I can't log in.",
    "help@example.com",
    "CS4944 version 2.1",
    "",
    "یہ ایک مثال ہے"
]

def main():
    for text in samples:
        whitespace = text.split()
        word_like = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
        print("Original:", repr(text))
        print("Whitespace:", whitespace, "count =", len(whitespace))
        print("Word-like:", word_like, "count =", len(word_like))
        print("-" * 60)
    assert re.findall(r"\b\w+\b", "", flags=re.UNICODE) == []
    print("Differences:")
    print("1. Whitespace splitting retains punctuation attached to tokens; the regex drops punctuation.")
    print("2. The regex splits the contraction can't into can and t, while whitespace keeps can't together.")
    print("Normalization risk: changing case or punctuation can damage identifiers and source wording.")
    print("The regex is a simple word-like tokenizer, not a complete multilingual tokenizer.")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2", device="cpu")
        print("Optional model subword tokens:")
        for text in samples[:2]:
            print(repr(text), model.tokenizer.tokenize(text))
    except ImportError:
        print("Optional model comparison skipped: install sentence-transformers.")
    except Exception as exc:
        print("Optional model comparison unavailable:", exc)

if __name__ == "__main__":
    main()
