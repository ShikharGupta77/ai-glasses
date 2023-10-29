from google.oauth2 import service_account
import sounddevice as sd
import numpy as np
import wave
from google.cloud import speech_v1
import io
import time
import together
import re
from actions import calendar_add, slack_add  # Importing functions
from datetime import datetime, timedelta
from flask import Flask
from flask_cors import CORS, cross_origin

together.api_key = '85ef951589f8fd8bfe69e6ef83d82dd664050bbe22ecddc7eee53c6b07718b5d'

# Choose the duration of the recording in seconds and the sampling frequency
duration = 2  # seconds
fs = 16000

# Function to record audio
def record_audio(duration, fs):
    print("Recording...")
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
    sd.wait()  # Wait until recording is finished
    print("Recording complete.")
    return myrecording

# Convert the NumPy array to bytes
def convert_np_audio_to_bytes(audio, fs):
    audio = np.int16(audio * 32767).tobytes()
    # Here, you can stream these bytes directly to Google API instead of saving to a file
    return audio
def clean_date_string(s):
    """
    Remove all characters from the input string except digits and slashes.

    :param s: str, the input string (potentially containing a date)
    :return: str, the cleaned string containing only digits and slashes
    """
  
    pattern = r'[^0-9/]'
    
    cleaned_string = re.sub(pattern, '', s)
    
    return cleaned_string
def add_one_hour(time_str):
    """
    Add one hour to the input time.

    :param time_str: str, a time string in the format of "H:MM AM/PM"
    :return: str, the time string one hour later in the same format
    """
    # Define the time format
    time_format = '%I:%M %p'
    
    # Convert the time string to a datetime object
    time_obj = datetime.strptime(time_str, time_format)
    
    # Add one hour
    time_obj += timedelta(hours=1)
    
    # Convert the datetime object back to a string
    # and return it
    return time_obj.strftime(time_format)

def transcribe_audio_file(file_path, credentials_path):
    """
    Transcribe the given audio file using Google Cloud Speech-to-Text.

    Args:
    file_path (str): Path to the audio file.

    Returns:
    str: Transcription result.
    """
    # Load the credentials from the file
    credentials = service_account.Credentials.from_service_account_file(credentials_path)

    # Create a speech client using the credentials
    client = speech_v1.SpeechClient(credentials=credentials)

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech_v1.types.RecognitionAudio(content=content)
    config = speech_v1.types.RecognitionConfig(
        encoding=speech_v1.types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript

    return transcription

def extract_time(s):
    """
    Extract time from a string.

    :param s: str, input string potentially containing time
    :return: str, extracted time in "H:MM AM/PM" format or an error message if time is not found
    """
    # Define a regular expression pattern to match a time in "H:MM AM/PM" format
    # \d matches any decimal digit; [AP]M matches either "AM" or "PM".
    pattern = r'(\d{1,2}:\d{2} [AP]M)'

    # Search the string for a match
    match = re.search(pattern, s)

    # If a match is found, return the time
    if match:
        time_str = match.group(1)
        
        # Validate and format the extracted time
        try:
            time_obj = datetime.strptime(time_str, '%I:%M %p')  # Parse the time string into a datetime object
            return time_obj.strftime('%I:%M %p')  # Format the time in the desired format
        except ValueError:
            return "11:30 AM"
    else:
        # If no match is found, return an error message
        return "12:30 AM"
    
def main():
    credentials_path = "glimpseai-329a24febe19.json"

    # Record audio
    audio_data = record_audio(duration, fs)

    # Convert to bytes
    audio_bytes = convert_np_audio_to_bytes(audio_data, fs)
    
    audio_data_int = np.int16(audio_data * 32767)  # Assuming your original data is float64

    with wave.open('output.wav', 'w') as wf:
        wf.setnchannels(1)  # mono recording
        wf.setsampwidth(2)  # 16-bit recording
        wf.setframerate(fs)  # Sample rate used for the recording
        wf.writeframes(audio_data_int.tobytes())

    print("Recording saved as 'output.wav'.")
    time.sleep(2)
    print("Transcribing the audio file...")
    transcription = transcribe_audio_file("output.wav", credentials_path)

    # Print the transcription
    print("Transcription: ", transcription)

    prompt = "if there is any mention of a date or time that has been finalized in the following text, write it in the format of: year/month/day. If there isn't a date, use today's date: '2023/10/28'. This is the following text: [" + transcription + "]"
    promptStage2 = "If there is any mention of a task in the following transcription, generate a short 3 sentence task list of the things needed to get done (leave blank if there aren't issues). Transcription: [" + transcription + "]"
    promptStage3 = "State all the facts from the following text: [" + transcription + "]"
    dateTime = ""
    timeTime = ""
    slackMessage=""
    output=""

    for token in together.Complete.create_streaming(prompt=prompt, model="garage-bAInd/Platypus2-70B-instruct"):
      print(token, end="", flush=True)
      dateTime+=token
    print("\n")
    newDateTime = clean_date_string(dateTime)

    for token in together.Complete.create_streaming(prompt="if there is any mention of a time that has been finalized in the following text, write it in the format of: hour:minute PM. If there isn't a time, use '6:00 PM'. This is the following text: [" + transcription + "]", model="garage-bAInd/Platypus2-70B-instruct"):
      print(token, end="", flush=True)
      timeTime+=token
    print("\n")
    print(newDateTime)
    newTimeTime = extract_time(timeTime)

    print(newTimeTime)
    endTime = add_one_hour(newTimeTime)
    print(endTime)

    try:
        calendar_add(newDateTime, newTimeTime, endTime, "test meeting")
    except:
        pass

    for token in together.Complete.create_streaming(prompt=promptStage2, model="garage-bAInd/Platypus2-70B-instruct"):
      print(token, end="", flush=True)
      slackMessage+=token
    print("\n")

    try: 
        slack_add(slackMessage)
    except:
        pass

    for token in together.Complete.create_streaming(prompt=promptStage3, model="garage-bAInd/Platypus2-70B-instruct"):
      print(token, end="", flush=True)
      output += token
    print("\n")

    return transcription, output

if __name__ == "__main__":
    t, f = main()
    #t, f = "transcript", "facts"

    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    @app.route('/transcript')
    @cross_origin()
    def transcript():
        print('trasncription', t)
        return t
    
    @app.route('/facts')
    @cross_origin()
    def facts():
        return f
    app.run()

