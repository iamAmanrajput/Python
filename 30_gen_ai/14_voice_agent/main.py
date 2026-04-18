import asyncio
# Async operations handle karne ke liye (non-blocking execution)

from dotenv import load_dotenv
# .env file se environment variables load karne ke liye

import speech_recognition as sr  
# Speech-to-text (STT) ke liye library

from openai import OpenAI
# Normal (sync) OpenAI client for chat completion

from openai.helpers import LocalAudioPlayer
# Generated audio ko local system pe play karne ke liye helper

import os
# Environment variables access karne ke liye

from openai import AsyncOpenAI
# Async OpenAI client → TTS ke liye (non-blocking + streaming)


# Load .env variables (API keys etc.)
load_dotenv()

# API key fetch kar rahe hain (Gemini API key)
API_KEY = os.getenv("GEMINI_API_KEY")


# Sync client → text generation (LLM response)
client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Async client → text-to-speech (TTS)
async_client = AsyncOpenAI()


# -------------------- TTS FUNCTION --------------------
async def tts(speech: str):
    # Async function jo text ko audio me convert karega

    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",  
        # TTS model (text → speech)

        voice="coral",  
        # Voice type (natural sounding voice)

        instructions="Always speak in cheerful manner with full of delight and happy",
        # Tone / speaking style control

        input=speech,  
        # Jo text bolna hai

        response_format="pcm",  
        # Audio format (PCM = raw audio stream)
        
    ) as response:
        # Streaming response → audio chunk by chunk aata hai

        await LocalAudioPlayer().play(response)
        # Audio ko real-time me play karte hain (no full wait)


# -------------------- MAIN FUNCTION --------------------
def main():
    r = sr.Recognizer()  
    # Recognizer object → speech ko text me convert karega

    with sr.Microphone() as source:  
        # Microphone ko input source bana rahe hain

        r.adjust_for_ambient_noise(source)  
        # Background noise reduce karta hai → accuracy improve hoti hai

        r.pause_threshold = 2  
        # User bolna band kare to kitna wait kare (seconds)

        SYSTEM_PROMPT = f"""
        You're an expert voice agent. You are given the transcript of what 
        user has said using voice.

        You need to output as if you are an voice agent and whatever you speak 
        will be converted back to audio using AI and played back to user.
        """
        # System prompt → AI ko role define karta hai (voice assistant)

        messages = [{'role': "system", "content": SYSTEM_PROMPT}]
        # Conversation history store karne ke liye list

        while True:
            # Infinite loop → continuous conversation

            print("Speak Something...")
            audio = r.listen(source)  
            # User ki voice record karna

            print("Processing Audio... (STT)")
            stt = r.recognize_google(audio)  
            # Speech → Text conversion (Google STT)

            print("You Said:", stt)  
            # User ka input print karna

            messages.append({"role": "user", "content": stt})
            # User message history me add karna

            response = client.chat.completions.create(
                model="gemini-2.5-flash",  
                # LLM model (text response generate karega)

                messages=messages
            )

            ai_reply = response.choices[0].message.content
            # AI ka generated response extract karna

            print("AI Response:", ai_reply)

            messages.append({"role": "assistant", "content": ai_reply})
            # AI response bhi history me add (context maintain ke liye)

            asyncio.run(tts(speech=ai_reply))
            # Async TTS function run kar rahe hain → text ko speech me convert karke play


# Program start point
main()
# Main function call → pura voice agent start ho jata hai


# Output
# Speak Something...
# Processing Audio... (STT)
# You Said: hey there agent how are you doing