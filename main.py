# pm2 start fastapi.json
# source venv/bin/activate
# uvicorn main:app
# uvicorn main:app --reload 
# pm2 logs fastapi-app 
# sudo nano /etc/nginx/sites-enabled/fastapi_nginx


# Main imports
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
from datetime import datetime
import os
from io import BytesIO
from typing import List




# Custom function imports
from functions.text_to_speech import convert_text_to_speech
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages
from functions.jokes import get_joke
from functions.dance import dancing
from functions.musics import play_music

openai.organization = os.getenv("OPEN_AI_ORG", "org-tLC3pK3Zbdk5EHdc2RCzOvbd")
openai.api_key = os.getenv("OPEN_AI_KEY", "sk-proj-yCY7HWbCxinXxzvF4FuwT3BlbkFJVbvYNbIo0qZQmbSmpTQM")
# Get Environment Vars

# Initiate App
app = FastAPI()


# CORS - Origins
origins = [
    "https://joybot.fennaver.com/",
    "https://master.dwiknvwkzox6t.amplifyapp.com/",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
]


# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin"],
)


# Check health
@app.get("/api/health")
async def check_health():
    return {"response": "healthy"}


# Reset Conversation
@app.get("/api/reset")
async def reset_conversation():
    reset_messages()
    return {"response": "conversation reset"}


# Post bot response
# Note: Not playing back in browser when using post request.
@app.post("/api/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}, Content-Type: {file.content_type}")
    
    # Save the file temporarily
    # Read the file content
    content = await file.read()
    print(f"File size: {len(content)} bytes")


    # ************* Decode audio
    message_decoded = convert_audio_to_text(content)
    print(f"The audio converted to text by whisper api: {message_decoded}")
    
    # Guard: Ensure output
    if message_decoded is None:
        raise HTTPException(status_code=400, detail="Failed to decode audio")
    
    # Check if "dance" keyword is present in the decoded message
    if "dans" in message_decoded.lower():
        # Example dance routine
        dance_moves = [
            ('forward', 'start'),
            ('right', 'start'),
            ('backward', 'start'),
            ('left', 'start'),
            ('stop', 'stop')
        ]
        """
         # Loop through the dance moves
        for move in dance_moves:
            dancing(*move)
            time.sleep(2)  # Adjust sleep duration as need
        """
       

    elif "fıkra" in message_decoded.lower():
        joke = get_joke() + "fıkrayı beğendin mi?"
        # Convert chat response to audio
        audio_streams = convert_text_to_speech(joke) 
        print("audio output from elevenLabs TTS is done")
        #print ("SST", datetime.now())

        # Guard: Ensure output
        if audio_streams:
            raise HTTPException(status_code=400, detail="Failed audio output")

        # Create a generator that yields chunks of data
        def iterfile():
            for stream in audio_streams:
                if isinstance(stream, BytesIO):
                    stream.seek(0)
                    yield from stream
                else:
                    yield stream
    

        # Use for Post: Return output audio
        return StreamingResponse(iterfile(), media_type="audio/mpeg")

    elif "müzik" in message_decoded.lower():

        print("Müzik")

        try:
            with open("assests/konusma.mp3", "rb") as music_file:
                music_for_dance = music_file.read()
        except Exception as e:
            print("Error reading audio file:", e)

        print("Audio Data Length:", len(music_for_dance))
        
        
        def iterfile():
            yield music_for_dance

        # Use for Post: Return output audio
        return StreamingResponse(iterfile(), media_type="application/octet-stream")
    

    # Check if "video" keyword is present in the decoded message
    elif "videooo" in message_decoded.lower():
        # Redirect to a YouTube URL (you can replace this with the desired URL)

        print ("YouTube")
        youtube_url = "https://www.youtube.com/"
        # Use create_task to run this asynchronously in the background
        return RedirectResponse(youtube_url, status_code=status.HTTP_303_SEE_OTHER)
    
    else:
        # Get chat response
        chat_response = get_chat_response(message_decoded)
        print("chatGPT Response: ",chat_response)
        #print ("chatGPT", datetime.now())
        # Store messages
        store_messages(message_decoded, chat_response)

        # Guard: Ensure output
        if not chat_response:
            raise HTTPException(status_code=400, detail="Failed chat response")
        

        #chat_response = "Merhaba Ben Kiki! Sana birkaç bilgi anlatayım mı?"
        # Convert chat response to audio
        audio_streams = convert_text_to_speech(chat_response)
        print("audio output from elevenLabs TTS is done")
        #print ("SST", datetime.now())

        # Guard: Ensure output
        if not audio_streams:
            raise HTTPException(status_code=400, detail="Failed audio output")

        # Create a generator that yields chunks of data
        # Create a generator that yields chunks of data
        def iterfile():
            for stream in audio_streams:
                if isinstance(stream, BytesIO):
                    stream.seek(0)
                    yield from stream
                else:
                    yield stream

        # Use for Post: Return output audio
        return StreamingResponse(iterfile(), media_type="audio/mpeg")
    