# AI Voice Assistant

A beginner-friendly AI Voice Assistant built with Python and Streamlit.

The application can:

- Record a spoken question
- Convert speech into text
- Generate an AI response
- Convert the response back into speech
- Play the spoken answer inside the application

This project is part of the **AI Projects Series** on **Karthik's Show**.

---

## How It Works

```text
Voice Input
   ↓
Speech-to-Text with Whisper
   ↓
AI Response with Groq LLM
   ↓
Text-to-Speech with gTTS
   ↓
Spoken Answer
```

---

## Technologies Used

- **Python**
- **Streamlit** — application interface and microphone input
- **Groq Whisper** — speech-to-text
- **Groq LLM** — AI response generation
- **gTTS** — text-to-speech
- **GitHub Copilot** — code review and software-testing suggestions

---

## Project Structure

```text
ai-voice-assistant/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/KarthiksShow/ai-voice-assistant
cd ai-voice-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variable

Create a `.env` file in the project folder:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Do not upload the `.env` file to GitHub.

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
```

---

## Run the Application

```bash
streamlit run app.py
```

Allow microphone access when prompted by the browser.

---

# Prompt Templates Used

## 1. Voice Assistant System Prompt

This prompt defines how the language model should answer the user's spoken question.

```text
You are a helpful AI voice assistant.
Answer clearly and concisely using simple language.
```

### Python version

```python
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
]
```

---

## 2. Reusable Voice Assistant Prompt Template

You can customize the assistant by changing the role, audience, tone, and response length.

```text
You are a [ROLE].

Answer the user's question using:
- Audience: [TARGET AUDIENCE]
- Tone: [TONE]
- Detail level: [SHORT / MEDIUM / DETAILED]
- Language: [LANGUAGE]

Keep the answer suitable for spoken output.
Avoid unnecessary formatting and overly long responses.

User question:
[TRANSCRIBED QUESTION]
```

### Example

```text
You are a beginner-friendly technology teacher.

Answer the user's question using:
- Audience: Beginners
- Tone: Friendly and conversational
- Detail level: Short
- Language: English

Keep the answer suitable for spoken output.
Avoid unnecessary formatting and overly long responses.

User question:
Explain machine learning in simple words.
```

---

## 3. GitHub Copilot Software-Tester Prompt

In this project, GitHub Copilot was used as a software tester rather than as a complete code generator.

```text
Review this AI Voice Assistant application as a software tester.

Identify important edge cases and failure scenarios related to:
- microphone recording
- empty or silent audio
- speech transcription
- Groq API failures
- empty AI responses
- text-to-speech errors

Do not rewrite the entire application.

Suggest only practical improvements that are suitable for a beginner project,
and explain why each one is useful.
```

---

## 4. General Copilot Code-Review Template

This reusable template can be applied to other projects in the series.

```text
Review this [APPLICATION TYPE] as a [REVIEWER ROLE].

Focus on:
- [AREA 1]
- [AREA 2]
- [AREA 3]
- error handling
- user experience

Do not rewrite the entire application.

List the most important issues first.
Suggest beginner-friendly improvements and explain why each one is useful.
```

---

## Example Questions

Try asking:

```text
What are three benefits of learning Python?
```

```text
Explain artificial intelligence in simple words.
```

```text
What is the difference between AI and machine learning?
```

```text
Give me three tips for learning programming.
```

---

## Important Notes

- The application requires an internet connection.
- The browser must have microphone permission.
- Never commit your Groq API key to GitHub.
- AI-generated answers may occasionally be incomplete or inaccurate.
- Keep spoken questions short and clear for better transcription.

---

## What We Learned

- Capturing microphone input with Streamlit
- Converting speech into text with Whisper
- Sending transcribed text to a language model
- Converting AI-generated text into speech
- Validating empty model responses
- Using GitHub Copilot to identify failure scenarios

---

## YouTube Channel

This project was created for **Karthik's Show**.

**Learn. Build. Grow.**

Subscribe to follow the complete AI Projects Series.

---

## License

This project is intended for learning and demonstration purposes.
