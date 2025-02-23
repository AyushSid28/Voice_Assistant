# Voice Assistant AI

## Project Overview
This is a voice-based AI assistant that listens to a wake word, processes commands, and responds with voice output. It can provide the time, open websites, set reminders, and answer general questions using OpenAI's API.

## Prerequisites
Before running the project, make sure you have the following installed:

1. Python (3.10 or higher)
2. Virtual environment (optional but recommended)
3. Required Python libraries

## Installation and Setup
Follow these steps to set up the project:

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Voice-Assistant-AI.git
   cd Voice-Assistant-AI
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key**
   - Create a `.env` file in the `backend/config` directory.
   - Add the following line to the `.env` file:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```

## Running the Backend
To test the backend functionality, run the script:
```bash
python backend/utils/helper.py
```
This will start the assistant's backend, allowing it to process text-based queries.

## Running the Streamlit App
To launch the Streamlit interface:
```bash
streamlit run frontend/app.py
```
This will start the web interface where you can interact with the voice assistant.

## Testing the Voice Assistant
1. Open the Streamlit app using the above command.
2. Click the "Activate Assistant" button.
3. Say "Ayush" to wake up the assistant.
4. Ask a question or give a command (e.g., "What time is it?" or "Open YouTube").
5. The assistant will respond with voice output.

## Features
- Listens for the wake word "Ayush" to activate.
- Provides the current time.
- Opens predefined websites.
- Sets and retrieves reminders.
- Answers general questions using OpenAI's API.

## Notes
- Ensure your microphone is working properly.
-You can Use Eleven Labs and Clone your own voice and add it here.
- If the assistant does not respond, check your microphone settings and background noise.
- The OpenAI API key should be kept secure and not shared.


