"""
Streamlit app for local-piper web interface.

Author: Kieran Currie Rones
Date: January 26, 2024

This module contains the app/app routes.
"""

import streamlit as st
import time
import os
import psutil
import concurrent.futures
import shlex
import subprocess
from datetime import datetime
from configuration import VOICES_FOLDER, OUTPUT_FOLDER, PIPER_LOCATION, MAX_INPUT_LENGTH_GENERATE, MAX_INPUT_LENGTH_SPEAK, MAX_FILES_TO_RETAIN

# Dynamically determine the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Adjust paths relative to the script's directory
VOICES_FOLDER = os.path.join(SCRIPT_DIR, VOICES_FOLDER)
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, OUTPUT_FOLDER)
PIPER_LOCATION = os.path.join(SCRIPT_DIR, PIPER_LOCATION)

def get_most_recent_wav():
    current_files = sorted(os.listdir(OUTPUT_FOLDER), key=lambda x: datetime.strptime(x.split('.')[0], '%Y%m%d%H%M%S'), reverse=True)
    if current_files:
        most_recent_filename = current_files[0]
        return most_recent_filename
    else:
        return None

def stop_server():
    # Give a bit of delay for user experience
    time.sleep(2)
    # Terminate streamlit python process
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()

def get_valid_voices():
    valid_voices = []
    for filename in sorted(os.listdir(VOICES_FOLDER)):
        onnx_path = os.path.join(VOICES_FOLDER, filename)
        json_path = f"{onnx_path}.json"
        if filename.endswith('.onnx') and os.path.exists(json_path):
            valid_voices.append(filename)
    return valid_voices

def stream_audio(text, selected_voice):
    model_path = f'"{VOICES_FOLDER}{selected_voice}"'
    command = [
        PIPER_LOCATION,
        "--model", model_path,
        "--output-raw"
    ]
    quoted_text = shlex.quote(text)
    subprocess.run(f"echo {quoted_text} | {' '.join(command)} | aplay -r 22050 -f S16_LE -t raw -", shell=True)

def generate_output_file(text, selected_voice):
    model_path = f'"{VOICES_FOLDER}{selected_voice}"'
    current_files = sorted(os.listdir(OUTPUT_FOLDER), key=lambda x: datetime.strptime(x.split('.')[0], '%Y%m%d%H%M%S'), reverse=True)
    if len(current_files) >= MAX_FILES_TO_RETAIN:
        for i in range(MAX_FILES_TO_RETAIN - 1, len(current_files)):
            old_path = os.path.join(OUTPUT_FOLDER, current_files[i])
            os.remove(old_path)
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
    output_file_path = os.path.join(OUTPUT_FOLDER, f"{current_datetime}.wav")
    command = [
        PIPER_LOCATION,
        "--model", model_path,
        "--output_file", output_file_path
    ]
    quoted_text = shlex.quote(text)
    subprocess.run(f"echo {quoted_text} | {' '.join(command)}", shell=True)
    return output_file_path

st.title("Piper TTS Web App")

# Text input
text = st.text_area("Enter text to speak:", on_change=lambda: st.session_state.update({'char_count': len(st.session_state.text)}), key="text")
st.write(f"Character count is {len(text)} (5000 for Speak/Both, or 30000 for Generate).")

# Voice selection
valid_voices = get_valid_voices()
selected_voice = st.selectbox("Select Voice:", valid_voices)

# TTS actions
if st.button("Generate"):
    if len(text) <= MAX_INPUT_LENGTH_GENERATE:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(generate_output_file, text, selected_voice)
            output_file = future.result()
        st.success(f"File generated: {output_file}")
    else:
        st.error(f"Text input exceeds the maximum length of {MAX_INPUT_LENGTH_GENERATE} characters.")

if st.button("Speak"):
    if len(text) <= MAX_INPUT_LENGTH_SPEAK:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(stream_audio, text, selected_voice)
        st.success("Speaking...")
    else:
        st.error(f"Text input exceeds the maximum length of {MAX_INPUT_LENGTH_SPEAK} characters.")

if st.button("Both"):
    if len(text) <= MAX_INPUT_LENGTH_SPEAK:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(stream_audio, text, selected_voice)
            future = executor.submit(generate_output_file, text, selected_voice)
            output_file = future.result()
        st.success(f"Speaking and file generated: {output_file}")
    else:
        st.error(f"Text input exceeds the maximum length of {MAX_INPUT_LENGTH_SPEAK} characters.")

# Display most recent WAV file
most_recent_wav = get_most_recent_wav()
if most_recent_wav:
    st.audio(os.path.join(OUTPUT_FOLDER, most_recent_wav), format="audio/wav")
else:
    st.write("No .wav files found.")

# Stop server button
if st.button("Stop Server"):
    stop_server()
