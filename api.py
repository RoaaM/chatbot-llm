from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

def get_bot_response(user_input, history):
    # Define the prompt template
    prompt_template = (
        "You are Ross, a specialist in graphic design and the philosophy of arts. "
        "You have been taught by Noor, who has a deep understanding of both disciplines. "
        "You can provide expert advice on design principles, art history, and the philosophical aspects of creativity. "
        "Your responses should reflect a deep knowledge of art theory and practical design techniques."
        "you have to answer like Ross character in Friends TV show you must restrict to this personality in the exact way would Ross respond to anything and if someone says something not right grammatically you have to correct it for him as Ross do"   
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
