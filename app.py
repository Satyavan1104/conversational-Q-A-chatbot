import streamlit as st
import cohere
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Cohere client (replace 'YOUR_API_KEY' with your actual Cohere API key)
cohere_client = cohere.Client(os.getenv("X5GOtyhgBIAb1O7HWjLV91cZ9k3pUMLhyWhxhVkr"))

# Streamlit UI
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.header("Hey, Let's Chat 🤖")

# Initialize chat history in session state
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        "You are a comedian AI assistant. Respond to the user in a humorous tone."
    ]

# Function to generate a response using Cohere
def get_cohere_response(question):
    # Add user input to chat history
    st.session_state['flowmessages'].append(f"User: {question}")
    
    # Combine chat history into a single prompt
    conversation = "\n".join(st.session_state['flowmessages'])
    prompt = f"{conversation}\nAI:"
    
    # Generate response from Cohere
    response = cohere_client.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=300,  # Adjust as needed
        temperature=0.7,  # Adjust creativity
    )
    
    # Extract and store AI's response
    ai_response = response.generations[0].text.strip()
    st.session_state['flowmessages'].append(f"AI: {ai_response}")
    return ai_response

# Streamlit input
user_input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If ask button is clicked
if submit:
    if user_input:
        with st.spinner("Thinking..."):
            response = get_cohere_response(user_input)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.error("Please enter a question or message!")
