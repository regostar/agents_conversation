
import streamlit as st
from autogen import ConversableAgent
from utils import get_openai_api_key
import time

# =============================================================================
# 1. OpenAI configuration
# =============================================================================
OPENAI_API_KEY = get_openai_api_key()
llm_config = {"model": "gpt-3.5-turbo"}

# =============================================================================
# 2. Initialize Agents
# =============================================================================
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

# =============================================================================
# 3. Custom Avatars & Animated GIFs
# =============================================================================
CATHY_AVATAR = "cathy1.png"
JOE_AVATAR = "joe1.png"

TYPING_GIF   = "https://media.giphy.com/media/sSgvbe1m3n93G/source.gif"
LAUGHING_GIF = "https://media.giphy.com/media/5xaOcLGvzHxDKjufnLW/source.gif"

# =============================================================================
# 4. Session State Setup
# =============================================================================
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "conversation_started" not in st.session_state:
    st.session_state["conversation_started"] = False

# =============================================================================
# 5. Utility Functions
# =============================================================================
def add_message(sender: str, content: str):
    """Append a message permanently to session state."""
    st.session_state["chat_history"].append({"sender": sender, "content": content})

def stream_message(sender: str, full_text: str, delay: float = 0.03):
    """
    Streams out full_text one character at a time.
    This function creates a temporary layout row with the sender's avatar
    and a placeholder for the text that updates gradually.
    """
    # Determine the correct avatar
    avatar_url = CATHY_AVATAR if sender == "cathy" else JOE_AVATAR

    # Create columns for avatar and text
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image(avatar_url, width=50)
    # Create a placeholder for the streaming text in the second column.
    text_placeholder = col2.empty()
    displayed_text = ""
    for char in full_text:
        displayed_text += char
        text_placeholder.markdown(displayed_text)
        time.sleep(delay)
    # Once streaming is complete, return the final text.
    return displayed_text

def stream_and_add_message(sender: str, full_text: str):
    """
    Streams the message character-by-character and then adds it permanently
    to the session state's chat history.
    """
    # Stream the message
    stream_message(sender, full_text)
    # Save the message for future reruns
    add_message(sender, full_text)

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
    """
    Displays the permanent chat messages (from session state) using a manual layout.
    These messages are already fully rendered.
    """
    st.subheader("Chat History")
    for idx, msg in enumerate(st.session_state["chat_history"]):
        sender = msg["sender"]
        content = msg["content"]
        # Skip any system messages if present
        if sender == "system":
            continue
        avatar_url = CATHY_AVATAR if sender == "cathy" else JOE_AVATAR
        col1, col2 = st.columns([1, 9])
        with col1:
            st.image(avatar_url, width=50)
        with col2:
            st.markdown(content)

def map_and_stream_messages(chat_result, initiator_name: str):
    """
    For each message in chat_result, streams it out character by character.
    Mapping rules:
      - If initiator_name is 'joe':
          "assistant" messages belong to Joe,
          "user" messages belong to Cathy.
      - If initiator_name is 'cathy':
          "assistant" messages belong to Cathy,
          "user" messages belong to Joe.
    """
    for msg in chat_result.chat_history:
        role = msg["role"]
        content = msg["content"]
        if role == "assistant":
            sender = initiator_name
        elif role == "user":
            sender = "cathy" if initiator_name == "joe" else "joe"
        else:
            continue  # Skip system messages
        stream_and_add_message(sender, content)

# =============================================================================
# 6. Start Conversation if not already started
# =============================================================================
if not st.session_state["conversation_started"]:
    st.title("Chatbot Comedy Hour 🎭")
    with st.spinner("Starting conversation..."):
        # Joe's initial message to Cathy
        joe_msg = "I'm Joe. Cathy, let's keep the jokes rolling."
        stream_and_add_message("joe", joe_msg)
        chat_result = joe.initiate_chat(
            recipient=cathy,
            message=joe_msg,
            max_turns=2
        )
        map_and_stream_messages(chat_result, initiator_name="joe")
        st.session_state["conversation_started"] = True
    st.rerun()

# =============================================================================
# 7. Main UI: Display Permanent Chat History
# =============================================================================
st.title("Chatbot Comedy Hour 🎭")
display_chat_history()

col_continue, col_end = st.columns(2)

# =============================================================================
# 8. Continue Conversation
# =============================================================================
with col_continue:
    if st.button("Continue Conversation"):
        # Cathy sends a new message
        with st.spinner("Cathy is thinking..."):
            show_animation("Cathy", "typing")
            cathy_msg = "What's the last joke we talked about?"
            stream_and_add_message("cathy", cathy_msg)
            cathy.send(message=cathy_msg, recipient=joe)
        # Joe responds with a new joke
        with st.spinner("Joe is responding..."):
            chat_result = joe.initiate_chat(
                recipient=cathy,
                message=cathy_msg,
                max_turns=2
            )
            map_and_stream_messages(chat_result, initiator_name="joe")
            # Show a single laughing GIF after Joe's joke
            show_animation("Joe", "laughing")
        st.rerun()

# =============================================================================
# 9. End Conversation
# =============================================================================
with col_end:
    if st.button("End Conversation"):
        with st.spinner("Cathy is ending the conversation..."):
            show_animation("Cathy", "typing")
            cathy_msg = "I gotta go."
            stream_and_add_message("cathy", cathy_msg)
            cathy.send(message=cathy_msg, recipient=joe)
            chat_result = joe.initiate_chat(
                recipient=cathy,
                message=cathy_msg,
                max_turns=2
            )
            map_and_stream_messages(chat_result, initiator_name="joe")
        st.rerun()
