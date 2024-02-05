"""import requests
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

# Eleven Labs
# Convert text to speech
def convert_text_to_speech(message):
  body = {
    "text": message,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.9
    }
  }

  voice_shaun = "mTSvIrm2hmcnOvb21nW2"
  voice_rachel = "21m00Tcm4TlvDq8ikWAM"
  voice_antoni = "ErXwobaYiN019PkySvjV"
  voice_kid ="jBpfuIE2acCO8z3wKNLl"

  # Construct request headers and url
  headers = { "xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg" }
  endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_kid}/stream"

  try:
    response = requests.post(endpoint, json=body, headers=headers)
  except Exception as e:
     return

  if response.status_code == 200:
      #with open("output.wav", "wb") as f:
        #f.write(audio_data)
      return response.content
  else:
    return
"""
import requests
from decouple import config
import re


ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

# Eleven Labs
# Convert text to speech
def convert_text_to_speech(message):
    # Split the input text into sentences based on "." or "!"
    sentences = [sentence.strip() for sentence in re.split(r'[.!]', message) if sentence]

    
    voice_kid = "jBpfuIE2acCO8z3wKNLl"

    # Construct request headers and url
    headers = { "xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg" }
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_kid}/stream"

    audio_data_list = []

    for sentence in sentences:
        body = {
            "text": sentence.strip(),
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.9,
                "similarity_boost": 0.9
            } 
        }

        try:
            response = requests.post(endpoint, json=body, headers=headers)
        except Exception as e:
            continue

        if response.status_code == 200:
            audio_data_list.append(response.content)

    return audio_data_list

"""# Example usage:
input_text = "Çok teşekkür ederim! Sana yardımcı olabilmek benim için büyük bir mutluluk. Eğer başka bir konuda konuşmak veya yardıma ihtiyacın olursa her zaman buradayım. Keyifli bir gün geçirmeni dilerim!"
audio_data_list = convert_text_to_speech(input_text)

# Save the audio data to files or process as needed
for i, audio_data in enumerate(audio_data_list):
    with open(f"output_{i}.mp3", "wb") as f:
        f.write(audio_data)"""
