# UrduChatBot

This project is a Streamlit-based Urdu voice chatbot that combines natural language processing (NLP), audio processing, and generative AI to create a conversational agent. The chatbot processes Urdu voice inputs, responds in Urdu text and audio

# Features
**Voice Input:** Records Urdu audio input using audio_recorder_streamlit.
**Speech-to-Text:** Converts audio to Urdu text using SpeechRecognition.
**Text-to-Speech:** Generates Urdu audio responses using gTTS.
**Dynamic Chatbot Responses:** Powered by Google's Gemini (PaLM API) for generating intelligent Urdu responses.
**Interactive Interface:** User-friendly Streamlit interface with customizable UI styles.

**Clone the repository**
git clone <https://github.com/zrtashi/UrduChatBot/tree/main>
cd <https://github.com/zrtashi/UrduChatBot/tree/main/chat_bot>
**Create a virtual environment**
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
**Install dependencies:**
pip install -r requirements.txt
**streamlit run app.py**
streamlit run app.py

**Record Voice Input:**
Use the microphone icon in the app to record your Urdu query.
**Chat with the Bot:**
The chatbot will display Urdu responses in text and play Urdu audio replies.
**View Chat History:**
The sidebar displays a complete conversation log.




