from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from gtts import gTTS
import os
import base64
import tempfile
import google.generativeai as genai
import time


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate  # Optional if using PromptTemplate



# # # Retrieve API key from Streamlit secrets
# # # GEMINI_API_KEY = st.secrets['gemini']['API_KEY']
genai.configure(api_key =os.getenv('GOOGLE_API_KEY'))





# Initialize session state to store chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Main function
def main():
    st.markdown(
        
        """
        <style>
        # .stApp {
        #     background: linear-gradient(80deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 50%, rgba(0,212,255,1) 100%);
        # }
        .header-text {
            color: blackish;
            text-shadow: 2px 2px 4px #000000;
            text-align: right;
        }
        .avatar {
            border-radius: 50%;
            margin-right: 60px;
        }
        .chatbot-avatar {
            width: 50px;
            height: 30px;
            border-radius: 80%;
        }
        .user-text {
            background-color: #c4ffff;
            padding: 10px;
            border-radius: 10px;
            color: black;
            margin-bottom: 10px;
        }
        .bot-text {
            background-color: #ccf4f4;
            padding: 10px;
            border-radius: 10px;
            color: black;
            margin-bottom: 10px;
        }
        .footer {
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 12px;
            position: fixed;
            bottom: 0;
            width: 100%;
            
        }
         @keyframes fadein {
            from { opacity: 0; }
            to { opacity: 1; }
        }
                
            
        /* Add more specific selectors */
        .stApp .mic-bar {
            padding: 20px;
            border: 2px solid #ccc;
            border-radius: 10px;
            background-color: #f9f9f9;
            text-align: center;
        }

        .stApp .mic-bar span.button.svg.svg-inline--fa.fa-microphone.fa-4x {
            background-color: blue;
            border-radius: 50px;
            padding: 50px;
            color: black;
        }

        .stApp #root > span > button > svg {
            width: 24px;
            height: 24px;
            fill: white;
        }



        
        
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("<h1 class='header-text'>اردو بوٹ</h1>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<h3>📝 Chat History</h3>", unsafe_allow_html=True)
        with st.container():
            # Display chat history in the sidebar
            if st.session_state['chat_history']:
                st.markdown("<div class='chat-history'>", unsafe_allow_html=True)
                for message in st.session_state['chat_history']:
                    if message['type'] == 'user':
                        st.markdown(f"<div class='user-text'>🧑 {message['content']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='bot-text'>🤖 {message['content']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("No chat history yet.")


  

   

    

    # Define columns to left the recorder
    col1, col2, col3 = st.columns([1, 2, 1])  # Center the recorder

    with col3:
        # left the entire audio recorder within this column
        audio_data = audio_recorder(text='', icon_size="5x", icon_name="microphone", key="urdu_recorder")




    
    
    
    if audio_data is not None:
        with st.container():
            col1, col2 = st.columns(2)

            with col2:
                # Display the recorded user audio
                st.markdown('<h2 class="avatar">🧑</h2>', unsafe_allow_html=True)
                st.audio(audio_data, format="audio/wav")  # Play user audio

                # Save the recorded audio to a temporary file
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
                    temp_audio_file.write(audio_data)
                    temp_audio_file_path = temp_audio_file.name

                # Convert audio file to text
                text = convert_audio_to_text(temp_audio_file_path)
                st.markdown(f'<div class="user-text">{text}</div>', unsafe_allow_html=True)

                # Append the user's input text to the chat history
                st.session_state['chat_history'].append({'type': 'user', 'content': text})

                # Remove the temporary file
                os.remove(temp_audio_file_path)

        # Get response from the LLM model
        response_text = get_llm_response(text)

        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                # Convert the response text to speech
                st.markdown('<h2 class="avatar">🤖</h2>', unsafe_allow_html=True)
                response_audio_html = convert_text_to_audio(response_text)
                
                st.markdown(f'<div class="bot-text">{response_text}</div>', unsafe_allow_html=True)
                # Append the bot response to chat history
                st.session_state['chat_history'].append({'type': 'bot', 'content': response_text})


def convert_audio_to_text(audio_file_path):
    # Convert Urdu audio to text using speech recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ur")
            return text
        except sr.UnknownValueError:
            return "آپ کا سوال سمجھ نہیں آیا۔"
        except sr.RequestError:
            return "Sorry, my speech service is down"

def convert_text_to_audio(text, lang='ur'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts_audio_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
        tts.save(tts_audio_path)

        # Directly use st.audio with the file path
        st.audio(tts_audio_path, format='audio/mp3')
    except Exception as e:
        st.error(f"Error converting text to audio: {e}")

def encode_audio_to_base64(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    return base64.b64encode(audio_bytes).decode()

def get_llm_response(text, retries=3, delay=5):
    
    prompt = f"""
    Please respond to the following question exclusively in the Urdu language. 
    Ensure that no words or characters from any other language are used in your response.
    Start and end your answer with appropriate Urdu words that are relevant to the topic or question.
    Keep your response concise and to the point.
    You may also ask a follow-up question in Urdu if needed.
    If you don't understand the question or cannot provide an answer, 
    reply with: 'آپ کا سوال سمجھ نہیں آیا، براہ کرم دوبارہ کوشش کریں۔'
    Here is the question: {text}
    """


    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    for attempt in range(retries):
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
            )

            chat_session = model.start_chat()
            response = chat_session.send_message(prompt)

            return response.text
        except Exception as e:
            st.error(f"Error while fetching response from LLM: {e}")
            time.sleep(delay)  # Wait before retrying
            if attempt == retries - 1:
                return "Sorry, there was an error processing your request."

if __name__ == "__main__":
    main()

