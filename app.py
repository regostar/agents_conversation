import streamlit as st
from autogen import ConversableAgent
from utils import get_openai_api_key
import time

# 1. OpenAI configuration
OPENAI_API_KEY = get_openai_api_key()
llm_config = {"model": "gpt-3.5-turbo"}

# 2. Initialize Agents
cathy = ConversableAgent(
    name="cathy",
    system_message="Your name is Cathy and you are a stand-up comedian.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

joe = ConversableAgent(
    name="joe",
    system_message=(
        "Your name is Joe and you are a stand-up comedian. "
        "Start the next joke from the punchline of the previous joke."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# 3. Custom Avatars (replace with your own image URLs)
CATHY_AVATAR = "cathy1.png"
JOE_AVATAR = "joe1.png"

# 4. Animated GIFs (for typing and laughing)
TYPING_GIF = "https://media.giphy.com/media/sSgvbe1m3n93G/source.gif"
LAUGHING_GIF = "https://media.giphy.com/media/5xaOcLGvzHxDKjufnLW/source.gif"

# 5. Session State Setup
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "conversation_started" not in st.session_state:
    st.session_state["conversation_started"] = False

# 6. Utility Functions

def add_message(sender: str, content: str):
    """Append a message to the chat history."""
    st.session_state["chat_history"].append({"sender": sender, "content": content})

def show_animation(agent_name: str, animation_type: str = "typing", duration: float = 1.5):
    """
    Displays an animation (typing or laughing) above the chat area,
    then removes it after the given duration.
    """
    gif_url = LAUGHING_GIF if animation_type == "laughing" else TYPING_GIF
    st.image(gif_url, width=100, caption=f"{agent_name} is {animation_type}...")
    time.sleep(duration)
    st.empty()

def display_chat_history():
    """Display chat messages using a manual layout (avatar + text)."""
    st.subheader("Chat History")
    for idx, msg in enumerate(st.session_state["chat_history"]):
        sender = msg["sender"]
        content = msg["content"]

        # Skip any system messages
        if sender == "system":
            continue

        # Determine the avatar to use based on the sender.
        if sender == "cathy":
            avatar_url = CATHY_AVATAR
        elif sender == "joe":
            avatar_url = JOE_AVATAR
        else:
            continue

        # Layout: first column shows the avatar, second shows the message text.
        col1, col2 = st.columns([1, 9])
        with col1:
            st.image(avatar_url, width=50)
        with col2:
            st.markdown(content)

def map_and_add_messages(chat_result, initiator_name: str):
    """
    Maps messages in chat_result to the correct sender:
    If initiator_name == 'joe', then:
      - 'assistant' messages are from Joe
      - 'user' messages are from Cathy
    If initiator_name == 'cathy', then:
      - 'assistant' messages are from Cathy
      - 'user' messages are from Joe
    """
    for msg in chat_result.chat_history:
        role = msg["role"]
        content = msg["content"]
        if role == "assistant":
            add_message(initiator_name, content)
        elif role == "user":
            add_message("cathy" if initiator_name == "joe" else "joe", content)
        # Skip 'system' messages

# 7. Start Conversation if not already started
if not st.session_state["conversation_started"]:
    st.title("Chatbot Comedy Hour 🎭")
    with st.spinner("Starting conversation..."):
        joe_msg = "I'm Joe. Cathy, let's keep the jokes rolling."
        add_message("joe", joe_msg)
        chat_result = joe.initiate_chat(
            recipient=cathy,
            message=joe_msg,
            max_turns=2
        )
        map_and_add_messages(chat_result, initiator_name="joe")
        st.session_state["conversation_started"] = True
    st.rerun()  # Rerun to load the conversation

# 8. Main UI
st.title("Chatbot Comedy Hour 🎭")
display_chat_history()

col_continue, col_end = st.columns(2)

# 9. Continue Conversation Button
with col_continue:
    if st.button("Continue Conversation"):
        with st.spinner("Cathy is thinking..."):
            show_animation("Cathy", "typing")
            cathy_msg = "What's the last joke we talked about?"
            add_message("cathy", cathy_msg)
            cathy.send(message=cathy_msg, recipient=joe)
        with st.spinner("Joe is responding..."):
            chat_result = joe.initiate_chat(
                recipient=cathy,
                message=cathy_msg,
                max_turns=2
            )
            map_and_add_messages(chat_result, initiator_name="joe")
            # Display one laughing GIF after Joe's joke
            show_animation("Joe", "laughing")
        st.rerun()

# 10. End Conversation Button
with col_end:
    if st.button("End Conversation"):
        with st.spinner("Cathy is ending the conversation..."):
            show_animation("Cathy", "typing")
            cathy_msg = "I gotta go."
            add_message("cathy", cathy_msg)
            cathy.send(message=cathy_msg, recipient=joe)
            chat_result = joe.initiate_chat(
                recipient=cathy,
                message=cathy_msg,
                max_turns=2
            )
            map_and_add_messages(chat_result, initiator_name="joe")
        st.rerun()
