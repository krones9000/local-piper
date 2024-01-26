"""
Flask app for local-piper web interface.

Author: Kieran Currie Rones
Date: January 26, 2024

This module contains the app/app routes.
"""

from flask import Flask, request, render_template, jsonify
from configuration import VOICES_FOLDER, MAX_INPUT_LENGTH, OUTPUT_FOLDER
from tts_handler import stream_audio, generate_output_file
import concurrent.futures
import os
import signal
import sys
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/get_most_recent_wav', methods=['GET'])
def get_most_recent_wav():
    current_files = sorted(os.listdir(OUTPUT_FOLDER), key=lambda x: datetime.strptime(x.split('.')[0], '%Y%m%d%H%M%S'), reverse=True)

    if current_files:
        most_recent_filename = current_files[0]
        return jsonify(status='success', filename=most_recent_filename)
    else:
        return jsonify(status='error', message='No .wav files found.')

@app.route('/stop_server', methods=['POST'])
def stop_server():
    # Add authentication/authorization checks if needed
    os.system("pkill gunicorn")
    return jsonify(status='success', message='Server stopped successfully!')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_valid_voices', methods=['GET'])
def get_valid_voices():
    valid_voices = []

    # Iterate through files in the voices folder
    for filename in sorted(os.listdir(VOICES_FOLDER)):
        onnx_path = os.path.join(VOICES_FOLDER, filename)
        json_path = f"{onnx_path}.json"

        # Check if both .onnx and .json files exist for the selected voice
        if filename.endswith('.onnx') and os.path.exists(json_path):
            # Add the full model name to the valid_voices list
            valid_voices.append(filename)

    return jsonify(status='success', voices=valid_voices)

@app.route('/tts', methods=['POST'])
def tts_command():
    text = request.form.get('text')
    selected_voice = request.form.get('selected_voice')  # Update this line
    command = request.form.get('command')

    # Check if the input text exceeds the maximum allowed length
    if len(text) > MAX_INPUT_LENGTH:
        return jsonify(status='error', message=f'Text input exceeds the maximum length of {MAX_INPUT_LENGTH} characters.')

    if text and selected_voice:
        if command == 'speak':
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(stream_audio, text, selected_voice)
        elif command == 'generate':
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(generate_output_file, text, selected_voice)
        elif command == 'both':
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(stream_audio, text, selected_voice)
                executor.submit(generate_output_file, text, selected_voice)

        return jsonify(status='success', message='TTS command completed successfully!')
    else:
        return jsonify(status='error', message='An error has occurred.')
