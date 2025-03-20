import streamlit as st
from streamlit_chat import message
from autogen import ConversableAgent
from utils import get_openai_api_key
import time

# Set up the OpenAI API key and LLM configuration
OPENAI_API_KEY = get_openai_api_key()
llm_config = {"model": "gpt-3.5-turbo"}

# Initialize the agents
cathy = ConversableAgent(
    name="cathy",
    system_message="Your name is Cathy and you are a stand-up comedian.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

joe = ConversableAgent(
    name="joe",
    system_message="Your name is Joe and you are a stand-up comedian. Start the next joke from the punchline of the previous joke.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# Assets: distinct avatars for each agent
CATHY_AVATAR = "cathy1.png"  # Replace with a unique URL for Cathy
JOE_AVATAR = "joe1.png"    # Replace with a unique URL for Joe

# Animated GIFs for when the agents are "typing" or "laughing"
TYPING_GIF = "https://media.giphy.com/media/sSgvbe1m3n93G/source.gif"
LAUGHING_GIF = "https://media.giphy.com/media/5xaOcLGvzHxDKjufnLW/source.gif"

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Utility: add a message to the chat history
def add_message(sender, content):
    st.session_state.chat_history.append({"sender": sender, "content": content})

# Utility: show a short animation (typing or laughing) for an agent
def show_animation(agent_name, animation_type="typing", duration=1.5):
    gif_url = LAUGHING_GIF if animation_type == "laughing" else TYPING_GIF
    st.image(gif_url, width=100, caption=f"{agent_name} is {animation_type}...")
    time.sleep(duration)
    st.empty()  # Remove animation after duration

# Display the chat history with each agent's avatar
def display_chat_history():
    st.subheader("Chat History")
    for idx, msg in enumerate(st.session_state["chat_history"]):
        col1, col2 = st.columns([1, 9])
        with col1:
            if msg["sender"] == "cathy":
                st.image(CATHY_AVATAR, width=50)
            elif msg["sender"] == "joe":
                st.image(JOE_AVATAR, width=50)
        with col2:
            message(msg["content"], is_user=False, key=f"{msg['sender']}_{idx}")

# For controlling whether conversation started
if "conversation_started" not in st.session_state:
    st.session_state["conversation_started"] = False

# Helper function to handle an LLM exchange and map roles to the correct agent
def map_and_add_messages(chat_result, initiator_name):
    """
    If initiator_name == 'joe', then:
      - 'assistant' role is from Joe
      - 'user' role is from Cathy
    If initiator_name == 'cathy', then:
      - 'assistant' role is from Cathy
      - 'user' role is from Joe
    """
    for msg in chat_result.chat_history:
        if msg["role"] == "assistant":
            add_message(initiator_name, msg["content"])
        elif msg["role"] == "user":
            # The other agent
            other_name = "cathy" if initiator_name == "joe" else "joe"
            add_message(other_name, msg["content"])
        # If you want to handle 'system' or other roles, you can do so here.

# 1. Start conversation if not started
if not st.session_state["conversation_started"]:
    st.title("Chatbot Comedy Hour 🎭")
    with st.spinner("Starting conversation..."):
        joe_message = "I'm Joe. Cathy, let's keep the jokes rolling."
        # Manually add Joe's initial message
        add_message("joe", joe_message)

        # Joe initiates chat with Cathy
        chat_result = joe.initiate_chat(
            recipient=cathy,
            message=joe_message,
            max_turns=2
        )
        # Map roles from chat_result to "joe" or "cathy"
        map_and_add_messages(chat_result, initiator_name="joe")

        st.session_state["conversation_started"] = True
    st.rerun()

# 2. If conversation started, show the chat
st.title("Chatbot Comedy Hour 🎭")
display_chat_history()

# 3. Buttons for continuing or ending the conversation
col_continue, col_end = st.columns(2)

with col_continue:
    if st.button("Continue Conversation"):
        # Cathy says something
        with st.spinner("Cathy is thinking..."):
            show_animation("Cathy", "typing")
            cathy_message = "What's the last joke we talked about?"
            add_message("cathy", cathy_message)
            cathy.send(message=cathy_message, recipient=joe)

        # Joe responds (with a single laughing GIF after the joke)
        with st.spinner("Joe is responding..."):
            chat_result = joe.initiate_chat(
                recipient=cathy,
                message=cathy_message,
                max_turns=2
            )
            map_and_add_messages(chat_result, initiator_name="joe")
            # Show Joe laughing once after he responds
            show_animation("Joe", "laughing")

        st.rerun()

with col_end:
    if st.button("End Conversation"):
        # Cathy ends the conversation
        with st.spinner("Cathy is ending the conversation..."):
            show_animation("Cathy", "typing")
            cathy_message = "I gotta go."
            add_message("cathy", cathy_message)
            cathy.send(message=cathy_message, recipient=joe)

            chat_result = joe.initiate_chat(
                recipient=cathy,
                message=cathy_message,
                max_turns=2
            )
            map_and_add_messages(chat_result, initiator_name="joe")
