import csv
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from task2_chunks import make_chunks


def evaluate(scores, chunks, items):
    hits, reciprocal = [], []
    for row, query in zip(scores, items):
        if query["doc"] is None:
            continue
        top = np.argsort(-row, kind="stable")[:3]
        good = [rank for rank, i in enumerate(top, 1)
                if chunks[i]["doc"] == query["doc"]
                and query["evidence"] in chunks[i]["text"]]
        hits.append(bool(good))
        reciprocal.append(1 / good[0] if good else 0)
    if not hits:
        return None, None
    return float(np.mean(hits)), float(np.mean(reciprocal))


DOCS = {'late': 'Late submission is normally penalized under the assessment procedure. Students should submit work through the learning portal before the stated deadline. A student who experiences illness may request an extension, but medical evidence must be provided before the deadline. The exception does not automatically approve an extension; the course coordinator reviews the request and confirms the revised date in writing. Students should retain the confirmation message with their course records. If the portal is unavailable, take a screenshot of the error and contact the help desk before the deadline. Do not assume that an email attachment counts as a formal submission unless the coordinator confirms it. Late work without an approved extension may receive the standard penalty. Students should check the current assessment brief for the applicable submission format and time zone. Students should read announcements because deadlines can change only through an authorized course notice. Keep a copy of the submitted file and verify that it opens correctly. If the evidence arrives after the deadline, explain the timing honestly and ask the coordinator how the request will be handled. This teaching example is not an actual university rule.', 'password': "A forgotten account password can be reset using the recovery link on the login page. Enter the email address associated with the account and follow the instructions sent to that address. Never share a password or recovery code with another person, including someone claiming to be support staff. If the recovery email does not arrive, check the junk folder and confirm that the account email was entered correctly. After several unsuccessful attempts, contact the IT help desk and include the time of the attempt, but never send a password. Multi-factor authentication may require a second verification step. A password reset does not change access permissions or restore deleted files. Use a unique password and store it in an approved password manager. Support staff will not ask you to disclose the old password. When using a shared computer, sign out after completing the reset and avoid saving credentials in the browser. If you suspect an account is compromised, tell the help desk and follow the official account-security process. This teaching example is synthetic and should not replace an organization's real security instructions.", 'assignment': 'Assignments are uploaded through the learning portal using the assignment page for the relevant course. Check the course name and assignment title before selecting a file. The final submission should be a PDF unless the assessment brief specifies another format. After uploading, wait for the confirmation screen and save the receipt if one is provided. A draft saved on a local computer is not a submitted assignment. If the upload fails, retry while time remains and contact the help desk with the course, assignment title and a screenshot of the error. Do not include passwords or private credentials in support requests. File size limits and accepted formats can vary by course, so consult the current assessment brief. A submission is complete only when the portal displays a successful confirmation. If more than one file is required, check the instructions before submitting and make sure each required item is included. Use a clear filename that identifies the assignment without exposing sensitive personal information. This teaching example is synthetic and does not replace the current course instructions.', 'contractor': "Contractors may work remotely only when the signed contract explicitly permits remote work. General employee remote-work guidance does not automatically apply to contractors. A project manager may explain the procedure, but cannot override the signed contract without an approved written amendment. Contractors should confirm permitted locations, working hours and data-handling requirements before accessing company systems remotely. Sensitive files must be handled according to the relevant agreement and access rules. If the contract is unclear, ask the contract owner for written clarification rather than relying on a general staff page. Employees may request remote work with manager approval, but that separate rule is not evidence of contractor eligibility. The examples in this training document are synthetic and do not represent an actual organization's policy. Access should be limited to systems needed for the assigned work. A temporary exception should have a clear approver and end date. If the work location changes, confirm that the agreement still permits access from that location. This training example is synthetic, not legal advice or a real contract.", 'printer': "For blank printer pages, first check the ink or toner level and confirm that the correct printer is selected. If the device manual permits it, run the printer cleaning utility and then print a test page. Keep the steps in order so that the result of each check can be observed. If the test page remains blank, check whether protective tape was removed from a new cartridge and confirm that the cartridge is seated correctly. Do not disassemble the printer while it is powered on. A scanner producing a blank image has a different procedure: check document placement and choose the correct scanning source. Record the printer model and any error message before contacting technical support. Follow the device manual for model-specific instructions and do not assume that a scanner fix applies to a printer. Use paper recommended for the device and check for a paper-feed warning if the printer reports one. After troubleshooting, note which action changed the result so that support staff can avoid repeating checks. This training example is synthetic and does not replace the manufacturer's manual."}

QUERIES = [{'query': 'What is required for illness extensions?', 'doc': 'late', 'evidence': 'The exception does not automatically approve an extension; the course coordinator reviews the request and confirms the revised date in writing.', 'split': 'dev'}, {'query': 'How do I reset a forgotten password?', 'doc': 'password', 'evidence': 'A forgotten account password can be reset using the recovery link on the login page.', 'split': 'dev'}, {'query': 'Where do I upload assignments?', 'doc': 'assignment', 'evidence': 'Assignments are uploaded through the learning portal using the assignment page for the relevant course.', 'split': 'dev'}, {'query': 'Can contractors work remotely?', 'doc': 'contractor', 'evidence': 'Contractors may work remotely only when the signed contract explicitly permits remote work.', 'split': 'dev'}, {'query': 'What do I do for blank printer pages?', 'doc': 'printer', 'evidence': 'For blank printer pages, first check the ink or toner level and confirm that the correct printer is selected.', 'split': 'test'}, {'query': 'How can I recover my login access?', 'doc': 'password', 'evidence': 'A forgotten account password can be reset using the recovery link on the login page.', 'split': 'test'}, {'query': 'How should I hand in my coursework?', 'doc': 'assignment', 'evidence': 'Assignments are uploaded through the learning portal using the assignment page for the relevant course.', 'split': 'test'}, {'query': 'What proof is needed when I was ill?', 'doc': 'late', 'evidence': 'The exception does not automatically approve an extension; the course coordinator reviews the request and confirms the revised date in writing.', 'split': 'test'}, {'query': "What are tomorrow's flight prices?", 'doc': None, 'evidence': None, 'split': 'test'}, {'query': 'Who won the football match?', 'doc': None, 'evidence': None, 'split': 'test'}]

def main():
    docs = DOCS
    items = QUERIES
    assert len(docs) >= 5
    assert sum(q["doc"] is not None and q["split"] == "dev" for q in items) >= 4
    assert sum(q["doc"] is not None and q["split"] == "test" for q in items) >= 4
    assert sum(q["doc"] is None for q in items) >= 2
    for q in items:
        assert q["split"] in {"dev", "test"}
        if q["doc"] is not None:
            assert q["evidence"] and q["evidence"] in docs[q["doc"]]

    model = None
    try:
        from sentence_transformers import SentenceTransformer
        print("Loading sentence encoder (first run may download the model)...")
        t = time.perf_counter()
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
        print("Model load seconds:", round(time.perf_counter() - t, 4))
    except ImportError:
        print("sentence-transformers is not installed; running TF-IDF only.")
        print("For real embeddings, run: pip install -r requirements.txt")
    except Exception as exc:
        print("Sentence encoder unavailable; running TF-IDF only:", exc)
    query_texts = [q["query"] for q in items]
    logs = []
    for strategy in ["0", "10", "sentence"]:
        chunks = make_chunks(docs, strategy)
        texts = [c["text"] for c in chunks]
        if model is not None:
            lengths = [len(model.tokenizer(t, truncation=False)["input_ids"])
                       for t in texts + query_texts]
            print("Strategy", strategy, "chunks", len(chunks),
                  "max model token length", max(lengths), "limit", model.max_seq_length)
            if max(lengths) > model.max_seq_length:
                raise ValueError("Model limit exceeded; rechunk or shorten query")
        else:
            print("Strategy", strategy, "chunks", len(chunks), "(model token audit skipped without encoder)")
        methods = ["tfidf", "embedding"] if model is not None else ["tfidf"]
        for method in methods:
            t = time.perf_counter()
            if method == "tfidf":
                vectorizer = TfidfVectorizer()
                C = vectorizer.fit_transform(texts)
                Q = vectorizer.transform(query_texts)
            else:
                C = model.encode(texts, normalize_embeddings=True)
                Q = model.encode(query_texts, normalize_embeddings=True)
            encode_seconds = time.perf_counter() - t
            t = time.perf_counter()
            scores = (Q @ C.T).toarray() if method == "tfidf" else Q @ C.T
            search_seconds = time.perf_counter() - t
            for split in ["dev", "test"]:
                indices = [i for i, q in enumerate(items) if q["split"] == split]
                result = evaluate(scores[indices], chunks, [items[i] for i in indices])
                print(strategy, method, split, "Hit@3/MRR@3", result,
                      "chunks", len(chunks), "encode/index seconds",
                      round(encode_seconds, 4), "search seconds", round(search_seconds, 4))
            for row, query in zip(scores, items):
                for rank, i in enumerate(np.argsort(-row, kind="stable")[:3], 1):
                    chunk = chunks[i]
                    record = dict(strategy=strategy, method=method,
                        query=query["query"], split=query["split"], rank=rank,
                        score=float(row[i]), chunk_id=chunk["id"], doc=chunk["doc"],
                        start=chunk["start"], end=chunk["end"], text=chunk["text"],
                        answerable=query["doc"] is not None)
                    logs.append(record)
                    print(record)
    if logs:
        with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(logs[0]))
            writer.writeheader()
            writer.writerows(logs)
        print("Wrote retrieval_log.csv")
    print("Unanswerable-query top results are candidates only; no evidence is labelled relevant.")


if __name__ == "__main__":
    main()
