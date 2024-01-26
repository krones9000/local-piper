"""
Configuration settings for local-piper web interface.

Author: Kieran Currie Rones
Date: January 26, 2024

This module contains configuration parameters for the TTS application.
"""

# Add the path to your voices folder
VOICES_FOLDER = "./static/voices/"

# Add the path to your voices folder
OUTPUT_FOLDER = "./static/output/"

# Maximum input length for text-to-speech conversion
MAX_INPUT_LENGTH = 10000  # Adjust this value based on your requirements

# Number of output files to retain in the output folder
MAX_FILES_TO_RETAIN = 5

