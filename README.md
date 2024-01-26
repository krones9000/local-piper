# local-piper
A simple program to use piper through a web browser interface. The code is not quite ready for primetime. But you can view a demo below.

[![Click here to view a demo on YouTube.](https://img.youtube.com/vi/Ym2KmWeqd84/0.jpg)](https://www.youtube.com/watch?v=Ym2KmWeqd84)

local-piper is a browser-based front-end for the text-to-speech (TTS) application called [Piper](https://github.com/rhasspy/piper). local-piper was built using Flask. It allows users to convert text into speech using various pre-trained voice models.

## [Voices can be downloaded from here.](https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0)

I would recommend the "[en_US-libritts_r-medium](https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0/en/en_US/libritts_r/medium)" voice for a clear English speaking voice.

## Features

- Convert text input into spoken audio using selected voice models.
- Choose from a variety of voices available in the application.
- Real-time feedback on the processing status of TTS commands.
- Play generated audio directly in the browser.
- Dark mode styling for comfortable viewing.

## Prerequisites/Installation and Setup

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your_username/local-piper.git
   ```

2. Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the "piper" TTS engine is correctly installed and configured.

## Usage

1. Run the Flask application:

   ```bash
   gunicorn -b 127.0.0.1:5000 -w 4 --daemon app:app --timeout 600
   ```

2. Access the application in your web browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

3. Enter the text you want to convert to speech in the text input area.

4. Select a voice from the dropdown menu.

5. Click the "Speak", "Generate", or "Both" button to initiate the TTS command.

6. Monitor the processing status for feedback on the command execution.

7. Listen to the generated audio using the embedded audio player.

## Additional Functionality

- **Output Generations**: outputs are stored in ./static/output. The 5 most recent outputs are retain and stored with datetime name format. To change this you can edit MAX_FILES_TO_RETAIN in the the tts_handler.py file.

- **Stopping the Server**: To stop the server, click the "Stop Server" button. This action requires appropriate authentication/authorization checks.

- **Voice Selection**: The dropdown menu dynamically populates with available voice models retrieved from the server.

- **Clear Text Box**: Use the "Clear Text Box" button to clear the text input area.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for bug fixes, enhancements, or new features.

## License

This project is licensed under the [MIT License](LICENSE).
