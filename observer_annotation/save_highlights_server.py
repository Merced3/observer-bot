# observer_annotation/save_highlights_server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import spacy
from spacy.language import Language

app = Flask(__name__)
CORS(app)
TRAIN_DATA_FILE = "observer_annotation/training_data.json"

# Ensure training file exists
if not os.path.exists(TRAIN_DATA_FILE) or os.stat(TRAIN_DATA_FILE).st_size == 0:
    with open(TRAIN_DATA_FILE, "w") as f:
        json.dump([], f)

nlp = spacy.load("en_core_web_sm")

# Register custom component
@Language.component("newline_sentencizer")
def newline_sentencizer(doc):
    for i, token in enumerate(doc[:-1]):
        if token.text == "\n":
            doc[i + 1].is_sent_start = True
    return doc

# Add it to the pipeline *before* the parser
if "parser" in nlp.pipe_names:
    nlp.remove_pipe("parser")

nlp.add_pipe("newline_sentencizer", before="ner")

def get_sentences(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

@app.route("/save", methods=["POST"])
def save_highlighted():
    try:
        print("\n[5000] 🔹 Saving new annotation...")

        #print("[DEBUG] Request content-type:", request.content_type)
        #print("[DEBUG] Request data:", request.data.decode('utf-8'))

        data = request.get_json(force=True)
        if not data:
            return jsonify({"status": "error", "message": "No JSON data received"}), 400
        
        raw_post = data.get("raw_post", {})
        highlights = data.get("highlights", {})

        #print("[DEBUG] Raw post keys:", raw_post.keys())
        #print("[DEBUG] Highlights:", highlights)

        # Collect all highlights (flattened to a set)
        all_highlighted = set(highlights.get("title", []) + highlights.get("body", []) + highlights.get("comments", []))

        # Combine all text fields into one string block
        combined = []
        if raw_post.get("title"): combined.append(raw_post["title"])
        if raw_post.get("body"): combined.append(raw_post["body"])
        if raw_post.get("comments"): combined.extend(raw_post["comments"])

        full_text = "\n".join(combined)

        # Split into sentences and match highlights
        sentences = get_sentences(full_text)
        entries = []
        for sentence in sentences:
            found = [word for word in all_highlighted if word in sentence]
            entries.append({
                "context": sentence,
                "keywords": found
            })

        # Save to file
        try:
            with open(TRAIN_DATA_FILE, "r") as f:
                existing_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_data = []

        existing_data.extend(entries)

        with open(TRAIN_DATA_FILE, "w") as f:
            json.dump(existing_data, f, indent=2)

        print(f"[5000] 🔹 Saved {len(entries)} new entries")
        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)