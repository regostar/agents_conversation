import streamlit as st
from autogen import ConversableAgent
from utils import get_openai_api_key

# -----------------------------------------------------------------------------
# 1. OpenAI configuration
# -----------------------------------------------------------------------------
OPENAI_API_KEY = get_openai_api_key()
llm_config = {"model": "gpt-3.5-turbo"}

# -----------------------------------------------------------------------------
# 2. Initialize Agents
# -----------------------------------------------------------------------------
cathy = ConversableAgent(
    name="cathy",
    system_message=(
        "Your name is Cathy and you are a stand-up comedian. "
        "Keep track of the conversation context but do not repeat it in your responses."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

joe = ConversableAgent(
    name="joe",
    system_message=(
        "Your name is Joe and you are a stand-up comedian. "
        "Continue the conversation using context from previous turns, "
        "but do not repeat the conversation context in your response. "
        "Only reply to the latest query."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# -----------------------------------------------------------------------------
# 3. Session State Setup
# -----------------------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False

# -----------------------------------------------------------------------------
# 4. Utility Functions
# -----------------------------------------------------------------------------
def add_message(sender: str, message: str):
    """Append a message to the chat history."""
    st.session_state.chat_history.append({"sender": sender, "content": message})

def build_context() -> str:
    """
    Build a conversation context string from chat history.
    Each message is formatted as "Sender: message".
    This context is used only for API calls and is not displayed.
    """
    context = ""
    for msg in st.session_state.chat_history:
        context += f"{msg['sender'].capitalize()}: {msg['content']}\n"
    return context

def display_history():
    """Display individual chat messages to the user (without full context)."""
    st.subheader("Chat History")
    for msg in st.session_state.chat_history:
        st.markdown(f"**{msg['sender'].capitalize()}:** {msg['content']}")

# -----------------------------------------------------------------------------
# 5. Start Conversation (only once)
# -----------------------------------------------------------------------------
st.title("Chatbot Conversation with Context")

if not st.session_state.conversation_started:
    # Joe sends an opening message.
    joe_msg = "I'm Joe. Cathy, let's start the conversation."
    add_message("joe", joe_msg)
    chat_result = joe.initiate_chat(
        recipient=cathy,
        message=joe_msg,
        max_turns=2
    )
    for msg in chat_result.chat_history:
        if msg["role"] == "assistant":
            add_message("joe", msg["content"])
        elif msg["role"] == "user":
            add_message("cathy", msg["content"])
    st.session_state.conversation_started = True
    st.rerun()

# -----------------------------------------------------------------------------
# 6. Main UI: Display Chat History (only individual messages)
# -----------------------------------------------------------------------------
display_history()

col_continue, col_end = st.columns(2)

# -----------------------------------------------------------------------------
# 7. Continue Conversation
# -----------------------------------------------------------------------------
with col_continue:
    if st.button("Continue Conversation"):
        # Build the conversation context (not displayed to the user)
        context = build_context()
        cathy_msg = "What's the last joke we talked about?"
        add_message("cathy", cathy_msg)
        
        # Build the message for the API call.
        # Append an instruction not to echo previous context.
        message_for_api = (
            f"{context}\n{cathy_msg}\n\n"
            "Please respond only to the latest query without repeating previous context."
        )
        
        chat_result = joe.initiate_chat(
            recipient=cathy,
            message=message_for_api,
            max_turns=2
        )
        for msg in chat_result.chat_history:
            if msg["role"] == "assistant":
                add_message("joe", msg["content"])
            elif msg["role"] == "user":
                add_message("cathy", msg["content"])
        st.rerun()

# -----------------------------------------------------------------------------
# 8. End Conversation
# -----------------------------------------------------------------------------
with col_end:
    if st.button("End Conversation"):
        context = build_context()
        cathy_msg = "I gotta go."
        add_message("cathy", cathy_msg)
        message_for_api = (
            f"{context}\n{cathy_msg}\n\n"
            "Please respond only to the latest query without repeating previous context."
        )
        chat_result = joe.initiate_chat(
            recipient=cathy,
            message=message_for_api,
            max_turns=2
        )
        for msg in chat_result.chat_history:
            if msg["role"] == "assistant":
                add_message("joe", msg["content"])
            elif msg["role"] == "user":
                add_message("cathy", msg["content"])
        st.rerun()
