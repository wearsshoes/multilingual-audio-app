import os
import concurrent.futures
import json
import hashlib
from flask import Flask, request, render_template
from dotenv import load_dotenv
from openai import OpenAI
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
from languages import LANGUAGES

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CACHE_FILE = 'cache.json'

def load_cache():
    try:
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return an empty dictionary if the file doesn't exist or if an error occurs

def save_cache(cache):
    with open(CACHE_FILE, 'w') as file:
        json.dump(cache, file, indent=4)

# Load environment variables
load_dotenv()
cache = load_cache()

# Set up clients
dz_client = DeepgramClient()
dz_client.api_key = os.getenv("DEEPGRAM_API_KEY")

tr_client = OpenAI()
tr_client.api_key = os.getenv("OPENAI_API_KEY")

def diarize(audio_file_path, file_hash):
    # Generate a unique key for the cache based on the file's hash
    cache_key = f"{file_hash}_diarize"

    # Check if the result is already in the cache
    if cache_key in cache:
        return cache[cache_key]

    # If not in cache, process the audio file and add the result to the cache
    with open(audio_file_path, "rb") as file:
        buffer_data = file.read()
    payload: FileSource = {
        "buffer": buffer_data,
    }
    options = PrerecordedOptions(
        model="nova-2",
        diarize=True
    )
    response = dz_client.listen.prerecorded.v("1").transcribe_file(payload, options)
    formatted_json = response.to_json(indent=4)
    cache[cache_key] = formatted_json
    save_cache(cache)  # Save changes to the cache file
    return formatted_json

def transcribe(audio_file_path, file_hash, language):
    # Generate a unique key for the cache based on the file's hash and language
    cache_key = f"{file_hash}_{language}"

    # Check if the result is already in the cache
    if cache_key in cache:
        return cache[cache_key]

    # If not in cache, process the audio file and add the result to the cache
    with open(audio_file_path, "rb") as audio_file:
        transcription = tr_client.audio.transcriptions.create(
            model="whisper-1",
            language=language,
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
    cache[cache_key] = transcription
    save_cache(cache)  # Save changes to the cache file

    return json.dumps(transcription.model_dump(), indent=4)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files or 'languages' not in request.form:
            return 'No file or languages specified'
        
        file = request.files['file']
        languages = request.form['languages'].split(',')

        if file.filename == '':
            return 'No selected file'
        if not languages:
            return 'No languages specified'
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file_hash = hashlib.md5(open(filename, 'rb').read()).hexdigest()
            file.save(filename)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_transcriptions = {
                    lang: executor.submit(transcribe, filename, file_hash, lang.strip())
                    for lang in languages
                }
                transcriptions = {
                    lang: future.result()
                    for lang, future in future_transcriptions.items()
                }

                future_diarization = executor.submit(diarize, filename, file_hash)
                diarization = future_diarization.result()

                # transcriptions_html = "<br>".join(
                # f"{lang} Transcript:<br><pre>{transcription}</pre>"
                # for lang, transcription in transcriptions.items()
                # )

            return render_template('upload.html', languages=LANGUAGES, diarization=diarization, transcriptions=transcriptions)
    return render_template('upload.html', languages=LANGUAGES)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=5001)