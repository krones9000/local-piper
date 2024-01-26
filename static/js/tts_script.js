/*
    JavaScript file written by Kieran Currie Rones
    Date: January 26, 2024
*/

// Function to update the audio source
function updateAudioSource(filename) {
    var audioPlayer = document.getElementById('audioPlayer');
    var audioSource = document.getElementById('audioSource');

    // Set the new source
    audioSource.src = '/static/output/' + filename;

    // Load the updated source
    audioPlayer.load();

    // Pause the audio at 0 seconds
    audioPlayer.pause();
    audioPlayer.currentTime = 0;
}

// Function to update processing status
function updateProcessingStatus(status) {
    $("#processingStatus").text(status);
}

// Clear the text box
function clearTextBox() {
    // Get the textarea element
    var textBox = document.getElementById("text");

    // Clear the content of the textarea
    textBox.value = "";

    // Log a message to the console to check if the function is being called
    console.log("Text box cleared!");
}

// stop the server
function stopServer() {
    $.ajax({
        type: "POST",
        url: "/stop_server",
        success: function (response) {
            console.log(response.message);
            // You can update the page to indicate that the server is stopping
        },
        error: function (error) {
            console.error("Error stopping server:", error);
            alert("An error occurred while stopping the server.");
        }
    });
}

// Function to populate the dropdown menu with valid voices
function populateVoiceDropdown() {
    $.ajax({
        type: "GET",
        url: "/get_valid_voices",
        success: function (response) {
            if (response.status === 'success') {
                var voiceDropdown = $("#voice");

                // Clear existing options
                voiceDropdown.empty();

                // Add each valid voice as an option
                for (var i = 0; i < response.voices.length; i++) {
                    // Create an option element with data-onnx attribute
                    var option = new Option(response.voices[i], response.voices[i]);
                    option.setAttribute('data-onnx', response.voices[i]); // Use the voice name as data-onnx
                    voiceDropdown.append(option);
                }
            } else {
                console.error("Error fetching valid voices:", response.message);
                alert("An error occurred while fetching valid voices.");
            }
        },
        error: function (error) {
            console.error("Error fetching valid voices:", error);
            alert("An error occurred while fetching valid voices.");
        }
    });
}

// Load the most recent .wav file and populate the dropdown menu on page load
$(document).ready(function () {
    getMostRecentWav();
    populateVoiceDropdown();
});

// Function to get the most recent .wav file
function getMostRecentWav() {
    $.ajax({
        type: "GET",
        url: "/get_most_recent_wav",
        success: function (response) {
            if (response.status === 'success') {
                updateAudioSource(response.filename);
            } else {
                console.error("Error getting most recent .wav:", response.message);
                alert("An error occurred while getting the most recent .wav.");
            }
        },
        error: function (error) {
            console.error("Error getting most recent .wav:", error);
            alert("An error occurred while getting the most recent .wav.");
        }
    });
}

function triggerSpeak() {
    triggerTTSCommand('speak');
}

function triggerGenerate() {
    triggerTTSCommand('generate');
}

function triggerBoth() {
    triggerTTSCommand('both');
}

function triggerTTSCommand(command) {
    var textToSpeak = $("#text").val();
    var selected_voice = document.getElementById('voice').value;  // Get the selected voice from the dropdown

    if (textToSpeak.trim() === "") {
        alert("Please enter text to speak.");
        return;
    }

    if (selected_voice.trim() === "") {
        alert("Please select a voice.");
        return;
    }

    updateProcessingStatus("Processing output.");

    $.ajax({
        type: "POST",
        url: "/tts",
        data: { text: textToSpeak, command: command, selected_voice: selected_voice },  // Send the selected voice to the server
        success: function (response) {
            $("#ttsStatus").text(response.message);

            if (response.status === 'success') {
                getMostRecentWav();  // Update to the most recent .wav file
                updateProcessingStatus('Output processed (most recent "Generate"/"Both" output available below).');
            } else {
                updateProcessingStatus('Processing error.');
                var audioPlayer = document.getElementById('audioPlayer');
                audioPlayer.src = '';
            }
        },
        error: function (error) {
            console.error("Error triggering TTS:", error);
            alert("An error occurred while triggering TTS.");
        }
    });
}


// Load the most recent .wav file on page load
$(document).ready(function () {
    getMostRecentWav();
});

function checkTTSStatus() {
    $.ajax({
        url: '/tts_status',
        type: 'GET',
        dataType: 'json',
        success: function (response) {
            // Check if the response has a 'status' property
            if (response.hasOwnProperty('status')) {
                if (response.status === 'success') {
                    $('#ttsStatus').html('TTS is running.');
                } else {
                    // Log the full response to the console
                    console.error('Error in TTS status response:', response);
                    $('#ttsStatus').html('TTS is not running.');
                }
            } else {
                console.error('Unexpected response format:', response);
                $('#ttsStatus').html('Unexpected response format.');
            }
        },
        error: function (error) {
            // Log the error details to the console
            console.error('Error in TTS status request:', error);
            $('#ttsStatus').html('Error checking TTS status.');
        }
    });
}


