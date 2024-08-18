import requests
from decouple import config
import re

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")
VOICE_ID = "jBpfuIE2acCO8z3wKNLl"
API_ENDPOINT = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

def convert_text_to_speech(message):
    sentences = [sentence.strip() for sentence in re.split(r'[.!]', message) if sentence]
    
    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }
    
    audio_data_list = []

    for sentence in sentences:
        body = {
            "text": sentence,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.9,
                "similarity_boost": 0.9
            }
        }

        try:
            response = requests.post(API_ENDPOINT, json=body, headers=headers)
            if response.status_code == 200:
                audio_data_list.append(response.content)
        except requests.RequestException as e:
            print(f"Error processing sentence: {sentence}. Error: {e}")

    return audio_data_list

def save_audio_files(audio_data_list):
    for i, audio_data in enumerate(audio_data_list):
        with open(f"output_{i}.mp3", "wb") as f:
            f.write(audio_data)
        print(f"Saved output_{i}.mp3")

if __name__ == "__main__":
    input_text = "(gülme). bunu da nereden çıkarttın? Araştırmalar gösteriyor ki, ben ve benim gibi sosyal robot arkadaşlar, otizmli çocukların becerilerini geliştirmede çok etkili bir materyal olabiliriz. Problem çözme, ortak dikkat, iletişim becerileri ve sosyal beceriler çalışılırken uzmanlara destek olabiliriz. Çocuklar, biz robotları oyuncak ya da oyun arkadaşı gibi görüyorlar. Yani, ben bir tabletten daha fazlasıyım. Aslında, daha fazla etkileşim için motivasyon sağlıyoruz. Kim demiş robotlar soğuk ve duygusuz diye? geleceğin öğrenme yolculuğunda çok önemli bir rol oynayacağız gibi görünüyor."
    
    audio_data_list = convert_text_to_speech(input_text)
    save_audio_files(audio_data_list)