import os
from io import BytesIO
from typing import IO, List
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs


client = ElevenLabs(
    api_key="1a9d6e09ff52cb6597eb93d2298ffe4d",
)

def text_to_speech_stream(text: str) -> IO[bytes]:
    """
    Converts text to speech and returns the audio data as a byte stream.
    
    Args:
        text (str): The text content to be converted into speech.
    
    Returns:
        IO[bytes]: A BytesIO stream containing the audio data.
    """
    response = client.text_to_speech.convert(
        voice_id="jBpfuIE2acCO8z3wKNLl",  
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.5,
            style=0.3,
            use_speaker_boost=True,
        ),
    )
    print("Streaming audio data...")
    audio_stream = BytesIO()
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)
    audio_stream.seek(0)
    return audio_stream

def convert_text_to_speech(message: str) -> List[IO[bytes]]:
    sentences = [sentence.strip() for sentence in message.split('.') if sentence.strip()]
    
    audio_data_list = []
    for sentence in sentences:
        try:
            audio_stream = text_to_speech_stream(sentence)
            audio_data_list.append(audio_stream)
        except Exception as e:
            print(f"Error processing sentence: {sentence}. Error: {e}")
    
    return audio_data_list

def save_audio_files(audio_data_list: List[IO[bytes]]):
    for i, audio_stream in enumerate(audio_data_list):
        with open(f"output_{i}.mp3", "wb") as f:
            f.write(audio_stream.getvalue())
        print(f"Saved output_{i}.mp3")

if __name__ == "__main__":
    input_text = "(gülme). bunu da nereden çıkarttın? Araştırmalar gösteriyor ki, ben ve benim gibi sosyal robot arkadaşlar, otizmli çocukların becerilerini geliştirmede çok etkili bir materyal olabiliriz. Problem çözme, ortak dikkat, iletişim becerileri ve sosyal beceriler çalışılırken uzmanlara destek olabiliriz. Çocuklar, biz robotları oyuncak ya da oyun arkadaşı gibi görüyorlar. Yani, ben bir tabletten daha fazlasıyım. Aslında, daha fazla etkileşim için motivasyon sağlıyoruz. Kim demiş robotlar soğuk ve duygusuz diye? geleceğin öğrenme yolculuğunda çok önemli bir rol oynayacağız gibi görünüyor."
    
    audio_data_list = convert_text_to_speech(input_text)
    save_audio_files(audio_data_list)