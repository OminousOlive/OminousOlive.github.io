from flask import Flask, render_template, request
from japverbconj.constants.enumerated_types import VerbClass, BaseForm, Formality, Tense, Polarity
from japverbconj.verb_form_gen import generate_japanese_verb_by_str

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/conjugate', methods=['POST'])
def conjugate():
    verb = request.form['verb']
    formality = request.form['formality']  # Will be either 'plain' or 'polite' from the form
    tense = request.form['tense']  # Will be either 'present' or 'past' from the form

    try:
        # Map formality and tense strings to the actual enumerations
        formality_enum = Formality.PLAIN if formality == 'plain' else Formality.POLITE
        tense_enum = Tense.NONPAST if tense == 'present' else Tense.PAST
        
        # Verb class can be GODAN or ICHIDAN (this is an example assuming GODAN)
        conjugated_verb = generate_japanese_verb_by_str(
            verb,
            VerbClass.GODAN,  # Update based on actual verb class
            "pla" if formality == 'plain' else "pol",
            "nonpast" if tense == 'present' else "past"
        )
        print(f"Conjugated verb: {conjugated_verb}")
        return render_template('index.html', conjugated_verb=conjugated_verb, verb=verb)
    except Exception as e:
        return render_template('index.html', error=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
