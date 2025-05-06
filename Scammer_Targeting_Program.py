import librosa
import numpy as np
import sounddevice as sd
import soundfile as sf
from vosk import Model, KaldiRecognizer
from langdetect import detect, DetectorFactory
import warnings
import time
import json
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import requests

warnings.filterwarnings("ignore")
DetectorFactory.seed = 0  # Ensure consistent results

# Step 1: Record or Load the Scammer's Audio
def record_audio(duration=10, sample_rate=16000):
    try:
        print("Recording audio for", duration, "seconds...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()  # Wait until recording is finished
        return audio.flatten()
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None

# Step 2: Extract Audio Features for Analysis
def extract_audio_features(audio, sample_rate=16000):
    y = audio
    sr = sample_rate
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs.T, axis=0)
    stft = np.abs(librosa.stft(y))
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(S=stft, sr=sr))
    spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(S=stft, sr=sr))
    return mfccs_mean, spectral_centroid, spectral_rolloff

# Step 3: Classify Accent Using Vosk and LangDetect
def classify_accent(audio_file_path):
    try:
        print("Transcribing audio using Vosk...")
        # Load the Vosk model
        model = Model("models/vosk-model-small-en-us-0.15")  # Path to the downloaded model
        recognizer = KaldiRecognizer(model, 16000)  # 16000 is the sample rate

        # Open the audio file
        with sf.SoundFile(audio_file_path) as audio_file:
            while True:
                data = audio_file.read(4000, dtype="int16")
                if len(data) == 0:
                    break
                recognizer.AcceptWaveform(data)

        # Get the transcription result
        result = json.loads(recognizer.FinalResult())
        transcript = result.get("text", "")
        print(f"Transcript: {transcript}")

        # Use langdetect to detect the language of the transcript
        if transcript:
            language = detect(transcript)
            print(f"Detected Language: {language}")
            return language
        else:
            print("No speech detected.")
            return "Unknown"
    except Exception as e:
        print(f"Error during transcription: {e}")
        return "Unknown"

# Step 4: Analyze Background Noise for Location Clues
def analyze_background_noise(audio, sample_rate=16000):
    _, spectral_centroid, spectral_rolloff = extract_audio_features(audio, sample_rate)
    if spectral_centroid > 3000:
        return "Urban environment (possible city noise)"
    elif spectral_rolloff < 2000:
        return "Rural environment (possible natural sounds)"
    else:
        return "Mixed environment"

# Step 5: OSINT for Phone Number Tracing
def trace_phone_number(phone_number):
    query = f"{phone_number} scam report"
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        print(f"Searching DuckDuckGo for reports about phone number: {phone_number}")
        time.sleep(5)  # Add delay to avoid being flagged
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract search result titles and links
        results = soup.find_all("a", class_="result__a")  # DuckDuckGo search result titles
        if results:
            print("Found the following reports:")
            for i, result in enumerate(results[:5]):  # Limit to the first 5 results
                print(f"{i + 1}. {result.text}")
        else:
            print("No reports found for this number.")
    except requests.exceptions.RequestException as e:
        print(f"Error during phone number tracing: {e}")

# Main Function
def analyze_scammer(audio_file_path=None, phone_number=None, call_timestamp=None):
    try:
        if audio_file_path is None:
            sample_rate = 16000
            audio = record_audio(duration=10, sample_rate=sample_rate)
            if audio is None:
                print("Recording failed. Please check your microphone or provide an audio file.")
                return
            sf.write("scammer_audio.wav", audio, sample_rate)
            audio_file_path = "scammer_audio.wav"
        else:
            audio, sample_rate = librosa.load(audio_file_path, sr=16000)
    except Exception as e:
        print(f"Error loading audio: {e}")
        return

    mfccs, spectral_centroid, spectral_rolloff = extract_audio_features(audio, sample_rate)
    print("Audio Features Extracted:")
    print(f"MFCCs (mean): {mfccs}")
    print(f"Spectral Centroid: {spectral_centroid}")
    print(f"Spectral Rolloff: {spectral_rolloff}")

    try:
        accent = classify_accent(audio_file_path)
        print(f"Detected Language: {accent}")
    except Exception as e:
        print(f"Error in language detection: {e}")
        accent = "Unknown"

    noise_context = analyze_background_noise(audio, sample_rate)
    print(f"Background Noise Context: {noise_context}")

    if phone_number:
        print("\nPhone Number Tracing:")
        trace_phone_number(phone_number)
    else:
        print("No phone number provided for tracing.")

# Initialize the geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

def get_location_from_gps(latitude, longitude):
    # Get the location from GPS coordinates
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    return location.address

def get_gps_data_from_service(device_id):
    # This is a placeholder function. Replace it with actual API calls to your GPS service.
    # For example, you might use an API like Google Maps Geolocation API or a custom service.
    api_url = f"https://api.yourgpsservice.com/get_location?device_id={device_id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data['latitude'], data['longitude']
    else:
        raise Exception("Failed to get GPS data")

def main():
    device_id = "your_device_id_here"  # Replace with the actual device ID
    try:
        latitude, longitude = get_gps_data_from_service(device_id)
        address = get_location_from_gps(latitude, longitude)
        print(f"Device is located at: {address}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

# Example Usage
if __name__ == "__main__":
    audio_file = None
    phone_number = input("Enter the phone number of the scammer (optional): ")
    call_timestamp = input("Enter the call timestamp (optional): ")
    analyze_scammer(audio_file, phone_number, call_timestamp)