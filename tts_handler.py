"""
Piper TTS functionality for local-piper web interface.

Author: Kieran Currie Rones
Date: January 26, 2024

This module contains the different stream and generation routes for TTS.
"""

import subprocess
import shlex
import os
from datetime import datetime
from configuration import MAX_FILES_TO_RETAIN, VOICES_FOLDER, OUTPUT_FOLDER

def stream_audio(text, selected_voice):
    model_path = f'"{VOICES_FOLDER}{selected_voice}"'
    
    # Add a proper condition here if needed
    command = [
        "./piper/./piper",
#        "--cuda",
        "--model", model_path,
        "--output-raw"
    ]
    quoted_text = shlex.quote(text)
    subprocess.run(f"echo {quoted_text} | {' '.join(command)} | aplay -r 22050 -f S16_LE -t raw -", shell=True)

def generate_output_file(text, selected_voice):
    model_path = f'"{VOICES_FOLDER}{selected_voice}"'
    
    current_files = sorted(os.listdir(OUTPUT_FOLDER), key=lambda x: datetime.strptime(x.split('.')[0], '%Y%m%d%H%M%S'), reverse=True)

    # Check if the number of files exceeds the limit, delete the oldest ones
    if len(current_files) >= MAX_FILES_TO_RETAIN:
        for i in range(MAX_FILES_TO_RETAIN - 1, len(current_files)):
            old_path = os.path.join(OUTPUT_FOLDER, current_files[i])
            os.remove(old_path)

    # Generate the new output file with datetime format
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
    output_file_path = os.path.join(OUTPUT_FOLDER, f"{current_datetime}.wav")
    command = [
        "./piper/./piper",
#        "--cuda",
        "--model", model_path,
        "--output_file", output_file_path
    ]
    quoted_text = shlex.quote(text)
    subprocess.run(f"echo {quoted_text} | {' '.join(command)}", shell=True)


