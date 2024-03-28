import os
from dotenv import load_dotenv
import requests

load_dotenv()

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")


url = "https://api.runpod.ai/v2/faster-whisper/run"

payload = {
    "input": {
        "audio": "http://docs.google.com/uc?export=open&id=1CIvP2H3rvEK-GgE93FzNoJVSFkwn0J-1",
        "model": "large-v2",
        "transcription": "plain_text",
        "translate": False,
        "language": "en",
        "temperature": 0,
        "best_of": 5,
        "beam_size": 5,
        "patience": 1,
        "suppress_tokens": "-1",
        "condition_on_previous_text": False,
        "temperature_increment_on_fallback": 0.2,
        "compression_ratio_threshold": 2.4,
        "logprob_threshold": -1,
        "no_speech_threshold": 0.6,
        "word_timestamps": True
    },
    "enable_vad": False
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": RUNPOD_API_KEY

}

response = requests.post(url, json=payload, headers=headers)

print(response.text)