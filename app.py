from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import json
app = Flask(__name__)

# Load the JSON data
data = {
    "Adeline Goh": {
        "drink_preference": "Iced Passionfruit",
        "dietary_restrictions": "Nil"
    },
    "Benjamin Liang": {
        "drink_preference": "Iced latte",
        "dietary_restrictions": "Nil"
    },
    "Beth Goh Rae Shuen": {
        "drink_preference": "Blue lagoon",
        "dietary_restrictions": "Nil"
    },
    "Dan Sin Lin Tammy": {
        "drink_preference": "Lychee Soda",
        "dietary_restrictions": "Nil"
    },
    "Demot John Nathan Tantoco": {
        "drink_preference": "Passion Fruit Soda",
        "dietary_restrictions": "Nil"
    },
    "Elicia Kuo Yi Xuan": {
        "drink_preference": "Passion Fruit Soda",
        "dietary_restrictions": "Nil"
    },
    "Genevieve Lee Xin En": {
        "drink_preference": "Passion Fruit Soda",
        "dietary_restrictions": "Prawn"
    },
    "Ivy Tan Poh Luan": {
        "drink_preference": "Sugar Free",
        "dietary_restrictions": "Peanuts"
    },
    "Jeremy Sim": {
        "drink_preference": "Black Coffee",
        "dietary_restrictions": "Dairy"
    },
    "LUTFIAH AMANI BINTE ROSLAN": {
        "drink_preference": "Matcha Frappe",
        "dietary_restrictions": "Nil"
    },
    "Low Zi Jian Jordan": {
        "drink_preference": "Hot Coffee/Latte",
        "dietary_restrictions": "Nil"
    },
    "NOOR ASHAAKIRIN BINTE MOHAMAD SHAIFUL": {
        "drink_preference": "Iced pandan coconut frappe",
        "dietary_restrictions": "Halal"
    },
    "Oon Si Qi Nyx": {
        "drink_preference": "Passion Fruit Soda",
        "dietary_restrictions": "Nil"
    },
    "Syadiyah Binte Muhammad Masyudi": {
        "drink_preference": "Ice drink Butterscotch",
        "dietary_restrictions": "Halal"
    },
    "Vincent Low": {
        "drink_preference": "Tea",
        "dietary_restrictions": "Nuts"
    },
    "யோகன்.": {
        "drink_preference": "கோப்பி.",
        "dietary_restrictions": "நில்"
    },
    "操你妈": {
        "drink_preference": "茶",
        "dietary_restrictions": "奶制品"
    },
    "黑鬼": {
        "drink_preference": "可乐",
        "dietary_restrictions": "蔬菜过敏"
    }
}
# Load the NLP model
nlp_pipeline = pipeline("question-answering")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data_received = request.get_json()
    question = data_received.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    # Prepare context
    context = " ".join([f"{name} prefers {info['drink_preference']} and has dietary restrictions: {info['dietary_restrictions']}" 
                        for name, info in data.items()])
    
    # Ask question
    answer = nlp_pipeline(question=question, context=context)
    
    return jsonify({'answer': answer['answer']})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host="0.0.0.0")

