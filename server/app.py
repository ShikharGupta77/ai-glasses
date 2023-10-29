from google.oauth2 import service_account
import sounddevice as sd
import numpy as np
import wave
from google.cloud import speech_v1
import io
import time
import together

together.api_key = '85ef951589f8fd8bfe69e6ef83d82dd664050bbe22ecddc7eee53c6b07718b5d'

# Choose the duration of the recording in seconds and the sampling frequency
duration = 5  # seconds
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

def main():
    credentials_path = "glimpseai-057eb119bbce.json"

    # # Record audio
    # audio_data = record_audio(duration, fs)

    # # Convert to bytes
    # audio_bytes = convert_np_audio_to_bytes(audio_data, fs)
    
    # audio_data_int = np.int16(audio_data * 32767)  # Assuming your original data is float64

    # with wave.open('output.wav', 'w') as wf:
    #     wf.setnchannels(1)  # mono recording
    #     wf.setsampwidth(2)  # 16-bit recording
    #     wf.setframerate(fs)  # Sample rate used for the recording
    #     wf.writeframes(audio_data_int.tobytes())

    # print("Recording saved as 'output.wav'.")
    # time.sleep(2)
    # print("Transcribing the audio file...")
    # transcription = transcribe_audio_file("output.wav", credentials_path)

    # # Print the transcription
    # print("Transcription: ", transcription)

# DELETE THIS CODE ASAP!!!!!
    transcription = "lets have dinner at 8pm? No? You want to do 6 pm? okay dinner at 6pm sounds good!"
    prompt = "if there is any mention of a date or time that has been finalized, write it in the format of: month/date/year, Hour:Minute. If there isn't a date, use today's date: '10/28/2023'. Then if there is any mention of an office issue in the following transcription, generate a short 3 sentence task list of the things needed to get done (leave blank if there aren't issues). Then, state all the facts from the following text: [" + transcription + "]"
    for token in together.Complete.create_streaming(prompt=prompt, model="garage-bAInd/Platypus2-70B-instruct"):
      print(token, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    main()
