import os
from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)


nlp = None


def get_nlp():
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")
    return nlp


@app.route('/entities', methods=['POST'])
def entities():
    if not request.is_json:
        return jsonify({"error": "Expected application/json body"}), 400
    data = request.get_json(silent=True) or {}
    text = data.get('text')
    if not text or not isinstance(text, str):
        return jsonify({"error": "Field 'text' is required and must be a string"}), 400

    doc = get_nlp()(text)
    entities = sorted({ent.text.lower() for ent in doc.ents})
    return jsonify({"entities": entities})

if __name__ == "__main__":
    app.run(host="0.0.0.0",  debug=True)