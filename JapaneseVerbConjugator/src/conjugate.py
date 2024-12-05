import sqlite3
import random
from flask import Flask, g, render_template, request, jsonify
from japverbconj.constants.enumerated_types import VerbClass, BaseForm, Tense, Polarity
from japverbconj.verb_form_gen import generate_japanese_verb_by_str

app = Flask(__name__)

DATABASE = 'src/verbs.db'  # Adjust for your file structure

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_random_verb():
    """Fetches a random verb from the database."""
    db = get_db()
    cursor = db.execute("SELECT dictionary_form, verb_class, translation FROM verbs ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    if result:
        return {"dictionary_form": result[0], "verb_class": result[1], "translation": result[2]}
    return None

@app.route('/')
def index():
    """Loads a random verb and conjugation details upon loading the page."""
    # Get a random verb, tense, formality, and polarity
    verb_data = get_random_verb()
    if not verb_data:
        return "Error: No verbs found in the database."

    dictionary_form = verb_data["dictionary_form"]
    translation = verb_data["translation"]
    verb_class = VerbClass[verb_data["verb_class"]]  # Expecting "GODAN" or "ICHIDAN or IRREGULAR"

    # Randomly select tense, base form, and polarity
    tense = random.choice(["nonpast", "past"])
    base_form = random.choice(["pla", "pol", "te", "ta", "tari", "cond", "vol", "pot", "imp", "prov", "caus", "pass"])
    polarity = random.choice(["pos", "neg"])

    # Generate the correct conjugation
    conjugated_verb = generate_japanese_verb_by_str(
        dictionary_form, verb_class, base_form, tense, polarity,
    )

    # Convert code values to readable format for display
    tense_display = "Present tense" if tense == "nonpast" else "Past tense"
    if base_form == "pla":
        form_display = "Plain Form"
    elif base_form == "pol":
        form_display = "Polite Form"
    elif base_form == "te":
        form_display = "Te Form"
    elif base_form == "ta":
        form_display = "Ta Form"
    elif base_form == "tari":
        form_display = "Tari Form"
    elif base_form == "cond":
        form_display = "Conditional Form"
    elif base_form == "vol":
        form_display = "Volitional Form"
    elif base_form == "pot":
        form_display = "Potential Form"
    elif base_form == "imp":
        form_display = "Imperative Form"
    elif base_form == "prov":
        form_display = "Provisional Form"
    elif base_form == "caus":
        form_display = "Causative Form"
    else:
        form_display = "Passive Form"
    polarity_display = "Positive" if polarity == "pos" else "Negative"

    return render_template(
        'testconjugate.html',
        dictionary_form=dictionary_form,
        conjugated_verb=conjugated_verb,
        translation = translation,
        base_form=form_display,
        tense=tense_display,
        polarity=polarity_display
    )

@app.route('/random_verb', methods=['GET'])
def random_verb():
    """Fetches and returns a random verb and conjugation details as JSON."""
    verb_data = get_random_verb()
    if not verb_data:
        return jsonify({"error": "No verbs found in the database"}), 404

    dictionary_form = verb_data["dictionary_form"]
    translation = verb_data["translation"]
    verb_class = VerbClass[verb_data["verb_class"]]

    tense = random.choice(["nonpast", "past"])
    base_form = random.choice(["pla", "pol", "te", "ta", "tari", "cond", "vol", "pot", "imp", "prov", "caus", "pass"])
    polarity = random.choice(["pos", "neg"])

    conjugated_verb = generate_japanese_verb_by_str(
        dictionary_form, verb_class, base_form, tense, polarity
    )

    tense_display = "Present tense" if tense == "nonpast" else "Past tense"
    if base_form == "pla":
        form_display = "Plain Form"
    elif base_form == "pol":
        form_display = "Polite Form"
    elif base_form == "te":
        form_display = "Te Form"
    elif base_form == "ta":
        form_display = "Ta Form"
    elif base_form == "tari":
        form_display = "Tari Form"
    elif base_form == "cond":
        form_display = "Conditional Form"
    elif base_form == "vol":
        form_display = "Volitional Form"
    elif base_form == "pot":
        form_display = "Potential Form"
    elif base_form == "imp":
        form_display = "Imperative Form"
    elif base_form == "prov":
        form_display = "Provisional Form"
    elif base_form == "caus":
        form_display = "Causative Form"
    else:
        form_display = "Passive Form"
    polarity_display = "Positive" if polarity == "pos" else "Negative"

    return jsonify({
        "dictionary_form": dictionary_form,
        "verb_class": verb_data["verb_class"],
        "translation": translation,
        "base_form": form_display,
        "tense": tense_display,
        "polarity": polarity_display,
        "conjugated_verb": conjugated_verb
    })

@app.route('/check_conjugation', methods=['POST'])
def check_conjugation():
    data = request.json
    user_conjugation = data.get('user_conjugation')
    correct_conjugation = data.get('correct_conjugation')

    result = user_conjugation == correct_conjugation
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
