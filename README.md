# local-piper

## This project is built around [**Piper**](https://github.com/rhasspy/piper).

**local-piper** currently only supports **Linux** and uses the **2023.11.14-2 Linux x86_64 Piper release**. However, I can't actually code. I wrote this using LLMs. So I'm sure you could figure out forking it for **Windows** if you wanted to! Just make sure you choose the right Piper version for you and replace the files in **./Piper**. I'm primarily a **Linux** user and have no plans to port this project at present.

**local-piper** is a browser-based front-end for the local neural text to speech (TTS) system called [**Piper**](https://github.com/rhasspy/piper). **local-piper** was built using **Flask**. It allows users to convert text into speech using various pre-trained voice models.

## [Voices can be downloaded from here.](https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0)

I would recommend the "[en_US-libritts_r-medium](https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0/en/en_US/libritts_r/medium)" voice model for a clear English speaking voice. See "*[Prerequisites/Installation and Setup](https://github.com/krones9000/local-piper/blob/main/README.md#prerequisitesinstallation-and-setup)*" for voice model installation.

## Features

- Convert text input into spoken audio directly using selected voice models.
- Choose from a variety of voices available in the application.
- Real-time feedback on the processing status of TTS commands.
- Store and play generated audio directly in the browser.
- Options for direct to speaker-output (**Speak**), .wav file generation (**Generate**), or both (**Both**).

## Prerequisites/Installation and Setup

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your_username/local-piper.git
   ```

2. Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. Populate the *./static/voices* folder with your chosen voice model files from [huggingface](https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0).
   ## **You must have *.onnx* and *.json* files for any given voice. If these are not both present, the voice will not be available in the web app. Piper requires that voice models use the following format:**

   ```
   NAME.onnx
   NAME.onnx.json.
   ```
   **You will note that [huggingface](https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0) does not provide names in this naming format and you will need to rename the files.** 


## Usage

1. Run the Flask application:

   ```bash
   gunicorn -b 127.0.0.1:5000 -w 4 app:app --timeout 600
   ```

*A timeout instruction is given to avoid timeouts during long generations. You can adjust this if desired but you may encounter errors.*

2. Access the application in your web browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

3. Enter the text you want to convert to speech in the text input area.

4. Select a voice from the dropdown menu.

5. Click the "**Speak**", "**Generate**", or "**Both**" button to initiate the TTS command.

6. Monitor the processing status for feedback on the command execution.

7. Listen to the generated audio through your speakers or by using the embedded audio player depending one which generation approach you selected.

## Additional Functionality

- **Output Generations**: outputs are stored in **./static/output**. The 5 most recent outputs are retained and stored with datetime name format. To change this you can edit **MAX_FILES_TO_RETAIN** in the the **tts_handler.py** file.

- **Stopping the Server**: To stop the server, click the "Stop Server" button at the bottom of the page. Or press **ctrl+c** in the console. 

- **Voice Selection**: The dropdown menu dynamically populates with available voice models retrieved from the server.

- **Clear Text Box**: Use the "**Clear Text Box**" button to clear the text input area.

- **App Icon Setup**: Files are included to help you set up the app to be run from the app menu should you choose to do so.

## Things to note

- **Streaming Parameters**: Streaming parameters are below. I used the one's from the **Piper** repo Readme, which states: "*This is raw audio and not a WAV file, so make sure your audio player is set to play 16-bit mono PCM samples at the correct sample rate for the voice.*" You could change them if you like by editting the line below in, **tts_handler.py**

     ```
     subprocess.run(f"echo {quoted_text} | {' '.join(command)} | aplay -r 22050 -f S16_LE -t raw -", shell=True)
     ```

- **CUDA**: There seems to be some issues with CUDA implementation in **Piper** at the moment and I honestly couldn't figure out if it's being used or not. It is commented out of **stream_audio** and **generate_output_file** in **tts_hander.py** by default but I have them both enabled and it doesn't cause issues whether they're *actually* working or not.

- **Piper Release Versions**: This version is built using **piper_linux_x86_64.tar.gz** from the **[Piper Releases Page](https://github.com/rhasspy/piper/releases)** 

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for bug fixes, enhancements, or new features.

## Acknowledgments

This project makes use of the following third-party libraries and tools:

- [Piper](https://github.com/rhasspy/piper)
- [Hugging Face](https://huggingface.co/)
- [Flask](https://flask.palletsprojects.com/)

## License

This project is licensed under the [MIT License](LICENSE).

