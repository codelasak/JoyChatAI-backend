import requests
from decouple import config

# Define the JoyBot and Replik sentences
joybot_sentences = [
    "Parkta kaydırak var.",
    "Kaydırak çok güzel.",
    "Top oynamak eğlencelidir.",
    "Herkes parkta eğleniyor.",
    "Arkadaşlarımızı çok severiz.",
    "Kediler tüylü ve yumuşaktır.",
    "Kediler süt içmeyi sever.",
    "Kediler çok hızlı koşabilir.",
    "Kediler oyun oynamayı sever.",
    "Yatmadan önce dişlerimizi fırçalarız.",
    "Uyumadan önce pijamalarımızı giyeriz.",
    "Uyumadan önce hikaye dinlemek güzeldir.",
    "Hikaye kitapları renkli ve resimlidir."
]

replik_sentences = [
    "Kaydıraktan  kayarım.",
    "Parkta  top  oynarım.",
    "Arkadaşlarım  da  parka gider.",
    "Arkadaşlarımla  oynarken  mutluyum.",
    "Kedileri  okşamayı  severim.",
    "Süt  çok  sağlıklıdır.",
    "Kediler  hızlıca  ağaca  tırmanır.",
    "Kedilerle  oynarken  iplik  sallarım.",
    "Fırçalayınca  dişlerim  beyaz  olur.",
    "Pijamalarım  çok  rahattır.",
    "Gece  annem  bana  hikaye  okur.",
    "Resimlere  bakıp  hikayeyi  dinlerim."
]

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")
voice_kid = "jBpfuIE2acCO8z3wKNLl" # Turkish kid voice
voice_kid2 = "5x4OabTaxKEADQiUryOC" # Replik kid voice

# Function to convert text to speech using Eleven Labs API
def convert_text_to_speech(text):
    api_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_kid2}"
    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }
    body = {
        "text": text.strip(),
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    response = requests.post(api_url, json=body, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Function to sanitize filenames
def sanitize_filename(filename):
    return "".join(c if c.isalnum() else "_" for c in filename)

# Convert each JoyBot sentence to speech and save the audio file
for sentence in replik_sentences:
    try:
        audio_data = convert_text_to_speech(sentence)
        filename = f"{sanitize_filename('replik_' + sentence)}.mp3"
        with open(filename, "wb") as f:
            f.write(audio_data)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Failed to convert '{sentence}': {e}")