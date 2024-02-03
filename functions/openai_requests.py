import openai
from decouple import config

from functions.database import get_recent_messages


# Retrieve Enviornment Variables
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

# Open AI - Whisper
# Convert audio to text
def convert_audio_to_text(audio_file):
    try:
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
# Convert audio to text
def get_chat_response(message_input):

  messages = get_recent_messages()
  #user_message = {"role": "user", "content": message_input + " Only say two or 3 words in Spanish if speaking in Spanish. The remaining words should be in English"}
  user_message = {"role": "user", "content": message_input}
  messages.append(user_message)
  print(messages)

  try:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    message_text = response["choices"][0]["message"]["content"]
    
    return message_text
  except Exception as e:
    return
