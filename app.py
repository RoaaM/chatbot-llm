import ollama
import streamlit as st

# Function to get a response from the Ollama model
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

# Streamlit app layout
def main():
    # Set the page background color to white
    st.markdown(
        """
        <style>
        body {
            background-color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("Coding Assistant")
    
    # Initialize chat history if not present
    if "history" not in st.session_state:
        st.session_state.history = []

    # Form for user input
    with st.form(key='input_form', clear_on_submit=True):
        user_input = st.text_input("You:", "")
        submit_button = st.form_submit_button(label="Send")

        if submit_button and user_input:
            # Store user input
            st.session_state.history.append({"role": "user", "content": user_input})
            
            # Get bot response with prompt template
            bot_response = get_bot_response(user_input, st.session_state.history)
            
            # Store bot response
            st.session_state.history.append({"role": "bot", "content": bot_response})

    # Display chat history with styling
    for message in st.session_state.history:
        if message["role"] == "user":
            st.markdown(f"""
                <div style="padding:10px; border-radius:10px; margin:5px 0; max-width:70%; word-wrap:break-word;">
                    <strong style="color: #FF5F1F;">You:</strong> <span style="color: #FF5F1F;">{message['content']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="padding:10px; border-radius:10px; margin:5px 0; max-width:70%; word-wrap:break-word;">
                    <strong style="color: #00a86b;">Bot:</strong> <span style="color: #00a86b;">{message['content']}</span>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
