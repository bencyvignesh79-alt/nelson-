import os
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎙️",
    layout="centered"
)

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("GROQ_API_KEY was not found in the .env file.")
    st.stop()

client = Groq(api_key=groq_api_key)

def generate_ai_response(question):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI voice assistant. "
                    "Answer clearly and concisely using simple language."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=300
    )

    return chat_completion.choices[0].message.content

def convert_text_to_speech(text):
    audio_buffer = BytesIO()

    speech = gTTS(
        text=text,
        lang="en"
    )

    speech.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    return audio_buffer

st.title("🎙️ AI Voice Assistant")

st.write(
    "Ask a question using your voice, "
    "and the AI assistant will respond."
)

audio_value = st.audio_input("Record your question")

if audio_value is not None:
    audio_bytes = audio_value.getvalue()

    if not audio_bytes:
        st.warning(
            "No audio was recorded. "
            "Please allow microphone access and try again."
        )
        st.stop()
    st.audio(audio_value)
    try:
        with st.spinner("Converting speech to text..."):
            transcription = client.audio.transcriptions.create(
                file=(
                    "recording.wav",
                    audio_value.getvalue()
                ),
                model="whisper-large-v3-turbo",
                response_format="json",
                temperature=0.0
            )
    except Exception:
        st.error(
        "Unable to transcribe the recording. "
        "Please check your connection and try again."
        )
        st.stop()
    transcribed_text = getattr(
        transcription,
        "text",
        ""
    ).strip()

    st.subheader("You asked")

    if transcribed_text:
        st.write(transcribed_text)
        with st.spinner("Generating AI response..."):
            ai_response = generate_ai_response(
            transcribed_text
             )
        
        if not ai_response or not ai_response.strip():
            st.error(
                "The assistant could not generate a response. "
                "Please try asking the question again."
            )
            st.stop()

        st.subheader("AI Assistant")
        st.write(ai_response)

        with st.spinner("Generating voice response..."):
            response_audio = convert_text_to_speech(
            ai_response
            )
        st.audio(
            response_audio,
            format="audio/mp3"
        )
    
    else:
        st.warning(
            "No speech was detected. "
            "Please record your question again."
        )