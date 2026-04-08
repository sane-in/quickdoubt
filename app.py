from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    question = data.get('question', '')
    grade = data.get('grade', '6')

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    prompt = f"""You are a friendly math tutor helping a Grade {grade} student.
Solve this math problem step by step in simple language a Grade {grade} student would understand.
Use numbered steps. Be encouraging. At the end, write the final answer clearly.

Problem: {question}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)