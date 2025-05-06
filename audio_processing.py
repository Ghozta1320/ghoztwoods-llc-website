import librosa
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
from datetime import datetime
import threading
import queue

class AudioAnalyzer:
    def __init__(self):
        self.sample_rate = 44100
        self.channels = 2
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.recognizer = sr.Recognizer()
        
    def start_recording(self):
        """Start audio recording"""
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()
        return "Recording started..."
        
    def stop_recording(self):
        """Stop audio recording"""
        self.is_recording = False
        self.recording_thread.join()
        return "Recording stopped..."
        
    def _record_audio(self):
        """Internal method to handle audio recording"""
        audio_data = []
        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, callback=self._audio_callback):
            while self.is_recording:
                frame = self.audio_queue.get()
                audio_data.extend(frame)
                
        # Save recording
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.wav"
        write(filename, self.sample_rate, np.array(audio_data))
        return filename
        
    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio stream"""
        self.audio_queue.put(indata.copy())
        
    def analyze_audio(self, audio_file):
        """Analyze recorded audio file"""
        # Load audio file
        y, sr = librosa.load(audio_file)
        
        results = {
            "voice_analysis": self._analyze_voice(y, sr),
            "background_noise": self._analyze_noise(y, sr),
            "accent_detection": self._detect_accent(audio_file),
            "transcription": self._transcribe_audio(audio_file)
        }
        
        return results
        
    def _analyze_voice(self, y, sr):
        """Analyze voice characteristics"""
        # Extract voice features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        
        # Pitch detection
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_mean = np.mean(pitches[magnitudes > np.max(magnitudes)*0.7])
        
        return {
            "pitch": float(pitch_mean),
            "energy": float(np.mean(librosa.feature.rms(y=y))),
            "speech_rate": self._calculate_speech_rate(y, sr)
        }
        
    def _analyze_noise(self, y, sr):
        """Analyze background noise"""
        # Separate harmonics and percussives
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        
        # Calculate noise metrics
        noise_level = np.mean(np.abs(y_percussive))
        signal_to_noise = np.mean(np.abs(y_harmonic)) / (noise_level + 1e-10)
        
        return {
            "noise_level": float(noise_level),
            "signal_to_noise_ratio": float(signal_to_noise)
        }
        
    def _detect_accent(self, audio_file):
        """Detect accent from audio"""
        # This is a placeholder for accent detection
        # In a real implementation, you would use a trained model
        return {
            "detected_accent": "Analysis pending...",
            "confidence": 0.0
        }
        
    def _transcribe_audio(self, audio_file):
        """Transcribe audio to text"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return {"text": text, "success": True}
        except Exception as e:
            return {"text": str(e), "success": False}
            
    def _calculate_speech_rate(self, y, sr):
        """Calculate approximate speech rate"""
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        return float(tempo[0])

# Example usage
if __name__ == "__main__":
    analyzer = AudioAnalyzer()
    print("Audio Analyzer initialized and ready for recording...")
