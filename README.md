# Agents Conversation

**Agents Conversation** is a fun and interactive Streamlit application that simulates a conversation between two stand-up comedian chatbots. Using OpenAI’s GPT-3.5 Turbo model, the bots exchange jokes and witty banter in real time. The application features custom avatars, smooth character-by-character message streaming, and animated GIFs to simulate typing and laughing for a more engaging user experience.

## Features

- **Interactive Chat**: Watch two chatbots (Cathy and Joe) exchange jokes in a dynamic conversation.
- **Character-by-Character Streaming**: Messages are displayed one character at a time for a natural typing effect.
- **Custom Avatars**: Each chatbot uses a unique avatar, ensuring a personalized look and feel.
- **Animated Feedback**: Animated GIFs simulate typing and laughing, adding extra personality to the conversation.
- **Session State Persistence**: Chat history is maintained across interactions for a continuous conversation experience.

## Demo

![comedian_bots](https://github.com/user-attachments/assets/0f2b3a85-cd44-4867-91f9-5ef4c183c58a)


![Agents Conversation Demo](https://drive.google.com/file/d/1O_AEDHAqmqy5fAx5JiuZsUYgwUIa4rVf/view?usp=drive_link)

## Installation

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- Required Python packages (listed in `requirements.txt`)

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/regostar/agents_conversation.git
   cd agents_conversation
   ```
2. ** Create a Virtual Environment and Activate It:**

  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
3. **Set Up API Keys**

Ensure you have an OpenAI API key and place it in your environment or a configuration file as needed. The application expects a helper function in `utils.py` (e.g., `get_openai_api_key()`) to retrieve your key.

4. **Usage**

To start the application, run:

  ```bash
  streamlit run app.py
  ```

Open the provided local URL (usually [http://localhost:8501](http://localhost:8501)) in your browser. The chat between the two agents will begin automatically. Use the provided buttons to continue the conversation or end it.

## Project Structure

```bash
agents_conversation/
├── app.py             # Main Streamlit application
├── autogen/           # Module for managing ConversableAgent logic
├── utils.py           # Utility functions (e.g., get_openai_api_key)
├── requirements.txt   # List of required Python packages
└── README.md          # This file
