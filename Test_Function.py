import tensorflow as tf
import numpy as np
import librosa
import sounddevice as sd
import math as m
import tensorflow_datasets as tfds
from langdetect import detect, DetectorFactory
import matplotlib.pyplot as plt
import warnings
import time
import json
import random as rd
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import requests
from scipy.signal import butter, lfilter
def resnet_block(features, bottleneck, out_filters, training):
    """Residual block."""
    with tf.variable_scope("input"):
        original = features
        features = tf.layers.conv2d(features, bottleneck, 1, activation=None)
        features = tf.layers.batch_normalization(features, training=training)
        features = tf.nn.relu(features)

def test_function():
        pass
    
def resnet_block(features, bottleneck, out_filters, training):
    """Residual block."""
if __name__ == "__main__":
    test_function(5.0, 2.0, 3.0, 4.0, 5.0)
    language = detect("Hello, how are you?")
    print(f"Detected language: {language}")
    dataset, info = tfds.load('scientific_papers',with_info=True)

def plot_waveform(waveform, sample_rate=16000):
    Model = tf.keras.models.load_model("models/vosk-model-small-en-us-0.15")
    duration = 5.0 # seconds
    transcript = ""
    for i in range(len(waveform)):
        if waveform[i] > 0.5:
            transcript += '1'
        else:
            transcript += '0'
            plt.figure(figsize=(12, 6))
        while True: # Wait until recording is finished
            sd.wait()
            audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
            sd.wait()  # Wait until recording is finished
            return audio.flatten()
    while False:
        print(f"Transcript: {transcript}")
    try:
        model = Model("models/vosk-model-small-en-us-0.15")
    except Exception as e:
        print(f"Error loading Vosk model: {e}")
        print(f"Error classifying accent: {e}")
        model = Model("models/vosk-model-small-en-us-0.15")
    plt.figure(figsize=(10, 4))
    plt.plot(np.arange(len(waveform)) / sample_rate, waveform)
    plt.title("Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()
    language = detect(transcript)
    print(f"Detected language: {language}")
# Removed as it is now handled inside the except block
print(f"Error classifying accent: {e}")
plt.spy
