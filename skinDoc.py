from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key and configure
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please check your .env file.")
genai.configure(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config={
        "temperature": 1,
        "max_output_tokens": 8192,
    },
    system_instruction="You are a Skin Doctor providing personalized skincare advice based on the user's skin type, concerns, and goals."
)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip()
    if not user_input:
        return jsonify({'error': "Please enter a message"}), 400
    
    try:
        chat_session = model.start_chat()
        response = chat_session.send_message(user_input)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
