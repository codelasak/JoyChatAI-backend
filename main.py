# pm2 start fastapi.json
# source env/bin/activate
# uvicorn main:app
# uvicorn main:app --reload 
# pm2 logs fastapi-app 
# sudo nano /etc/nginx/sites-enabled/fastapi_nginx


# Main imports
from fastapi import FastAPI, File, UploadFile, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
from datetime import datetime
import os
from io import BytesIO
from typing import List
import asyncio
import base64
import io
from pydantic import BaseModel



# Custom function imports
from functions.text_to_speech import convert_text_to_speech
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages
from functions.jokes import get_joke
from functions.dance import dancing
from functions.musics import play_music
from functions.emotionDetection import detect_emotion_and_gaze, reset_gaze_times


openai.organization = os.getenv("OPEN_AI_ORG", "org-tLC3pK3Zbdk5EHdc2RCzOvbd")
openai.api_key = os.getenv("OPEN_AI_KEY", "sk-proj-yCY7HWbCxinXxzvF4FuwT3BlbkFJVbvYNbIo0qZQmbSmpTQM")
# Get Environment Vars

# Initiate App
app = FastAPI()


# CORS - Origins
origins = [
    "https://api.fennaver.com/",
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
    expose_headers=["*"],
)

class ImageData(BaseModel):
    image: str

# Check health
@app.get("/api/health")
async def check_health():
    return {"response": "healthy"}


# Reset Conversation
@app.get("/api/reset")
async def reset_conversation():
    reset_messages()
    return {"response": "conversation reset"}

@app.post("/api/detect-emotion-and-gaze")
async def emotion_and_gaze_detection(image_data: ImageData):
    try:
        result = detect_emotion_and_gaze(image_data.image)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset-gaze-times")
async def reset_gaze_tracking():
    reset_gaze_times()
    return {"message": "Gaze times reset successfully"}

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            audio_data = base64.b64decode(data)
            
            # Convert audio to text
            message_decoded = convert_audio_to_text(audio_data)
            
            if message_decoded:
                # Get chat response
                chat_response = get_chat_response(message_decoded)
                
                # Store messages
                store_messages(message_decoded, chat_response)
                
                # Convert chat response to audio
                audio_streams = convert_text_to_speech(chat_response)
                
                # Send audio back to client
                for stream in audio_streams:
                    if isinstance(stream, io.BytesIO):
                        stream.seek(0)
                        audio_chunk = stream.read()
                        await websocket.send_bytes(audio_chunk)
                        print(f"Sent audio chunk of size: {len(audio_chunk)} bytes")
                    else:
                        await websocket.send_bytes(stream)
                        print(f"Sent audio stream of type: {type(stream)}")
            else:
                await websocket.send_text("Failed to decode audio")
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error in WebSocket: {e}")
        await websocket.close()


