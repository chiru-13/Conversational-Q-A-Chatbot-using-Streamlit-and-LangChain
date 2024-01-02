import streamlit as st
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv



# Set up Streamlit UI
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.title("Conversational Q&A Chatbot")

load_dotenv()
# Load OpenAI model
chat = ChatOpenAI(temperature=0.5)

# Initialize conversation history
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="Welcome! I'm here to chat with u")
    ]

# Define CSS styles for chat messages
st.markdown("""
<style>
    .message-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 10px;
    }
    .user-message {
        align-self: flex-end;
        background-color: #DCF8C6;
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 5px;
        max-width: 70%;
        text-align: left;
    }
    .ai-message {
        align-self: flex-start;
        background-color: #E0E0E0;
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 5px;
        max-width: 70%;
        text-align: left;
    }
    .system-message {
        align-self: center;
        background-color: #F5F5F5;
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 5px;
        max-width: 70%;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Function to display messages based on message type
def display_message(message):
    if isinstance(message, SystemMessage):
        st.markdown(f'<div class="message-container"><div class="system-message">{message.content}</div></div>', unsafe_allow_html=True)
    elif isinstance(message, HumanMessage):
        st.markdown(f'<div class="message-container"><div class="user-message">{message.content}</div></div>', unsafe_allow_html=True)
    elif isinstance(message, AIMessage):
        st.markdown(f'<div class="message-container"><div class="ai-message">{message.content}</div></div>', unsafe_allow_html=True)

# Display conversation history
for message in st.session_state['flowmessages']:
    display_message(message)

# Get user input
input_text = st.text_input("Input: ", key="input")

# Handle empty input
if not input_text:
    st.warning("Please enter a question.")
    st.stop()

# Function to get OpenAI model response
def get_chatmodel_response(question):
    st.session_state['flowmessages'].append(HumanMessage(content=question))
    answer = chat(st.session_state['flowmessages'])
    st.session_state['flowmessages'].append(AIMessage(content=answer.content))
    return answer.content

# Button to ask the question
submit_button = st.button("Ask the question")

# Display loading animation while processing
if submit_button:
    with st.spinner("Thinking..."):
        response = get_chatmodel_response(input_text)
        display_message(AIMessage(content=response))
