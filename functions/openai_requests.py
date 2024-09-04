import openai
from decouple import config
import io
from functions.database import get_recent_messages

# Retrieve Environment Variables
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

# Open AI - Whisper
# Convert audio to text
def convert_audio_to_text(audio_data):
    try:
        # Create a file-like object from the bytes
        audio_file = io.BytesIO(audio_data)
        audio_file.name = 'audio.wav'  # Add a name attribute

        # Transcribe audio
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        message_text = transcript["text"]
        print("convert_audio_to_text is ok")
        return message_text

    except ValueError as ve:
        # Handle short audio file error
        print(f"Error in convert_audio_to_text: {ve}")
        return None

    except Exception as e:
        # Handle other exceptions
        print(f"Error in convert_audio_to_text: {e}")
        return None

# Open AI - Chat GPT
# Get chat response
def get_chat_response(message_input):
    if message_input is None or message_input.strip() == "":
        print("Error: Empty or None message input")
        return "I couldn't understand that. Can you please repeat?"

    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)
    print(messages)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages
        )
        message_text = response["choices"][0]["message"]["content"]
        return message_text
    except openai.error.InvalidRequestError as e:
        print(f"OpenAI API Invalid Request Error: {e}")
        return "I'm sorry, I encountered an error. Can you try rephrasing your message?"
    except Exception as e:
        print(f"Error in get_chat_response: {e}")
        return "I'm having trouble processing your request. Please try again later."

