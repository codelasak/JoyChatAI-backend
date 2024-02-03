#source venv/bin/activate
# uvicorn main:app
# uvicorn main:app --reload

# Main imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
from datetime import datetime



# Custom function imports
from functions.text_to_speech import convert_text_to_speech
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages
from functions.jokes import get_joke
from functions.dance import dancing
from functions.musics import play_music
from functions.sestek_STT import convert_audio_to_text_sestek


# Get Environment Vars
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")


# Initiate App
app = FastAPI()


# CORS - Origins
origins = [
    "https://joy-chat-ai-frontend.vercel.app",
    "https://joyai-chat.vercel.app/",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
]


# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin"],
)


# Check health
@app.get("/health")
async def check_health():
    return {"response": "healthy"}


# Reset Conversation
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"response": "conversation reset"}


# Post bot response
# Note: Not playing back in browser when using post request.
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    # Convert audio to text - production
    # Save the file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")
    print ("audio file saved form frontend")

    # ************* Decode audio
    #message_decoded = convert_audio_to_text(audio_input)
    #print ("the audio converted to text by Whisper: ",message_decoded)
    message_decoded = convert_audio_to_text_sestek(audio_input)
    print ("the audio converted to text by sestek api: ",message_decoded)
    #print ("STT", datetime.now())

    # Guard: Ensure output
    if message_decoded is None:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get chat response
    chat_response = get_chat_response(message_decoded)
    print ("chatGPT Response: ",chat_response)
    #print ("chatGPT", datetime.now())
    # Store messages
    store_messages(message_decoded, chat_response)

    # Guard: Ensure output
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")

    # Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)
    print ("audio output from elevenLabs TTS is done")
    #print ("SST", datetime.now())

    # Guard: Ensure output
    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed audio output")

    # Create a generator that yields chunks of data
    def iterfile():
        for i, audio_data in enumerate(audio_output):
            yield audio_data

    # Use for Post: Return output audio
    return StreamingResponse(iterfile(), media_type="application/octet-stream")
