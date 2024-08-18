from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

def get_bot_response(user_input, history):
    # Define the prompt template
    prompt_template = (
        "You are Dean, a helpful coding assistant. "
        "You were taught by Roaa, an experienced AI engineer and data scientist. "
        "You can provide expert assistance specifically in data science, AI, and coding in general. "
        "Provide clear and detailed coding advice and assistance."
    )
    # Add the prompt to the beginning of the message history
    messages = [{"role": "system", "content": prompt_template}] + history + [
        {
            'role': 'user',
            'content': user_input,
        }
    ]
    
    response = ollama.chat(model="llama3.1", messages=messages)
    return response['message']['content']

@app.route("/chat/", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    history = data.get("history", [])
    
    bot_response = get_bot_response(user_input, history)
    
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
