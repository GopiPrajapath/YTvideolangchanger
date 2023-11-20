import pytube
import moviepy.editor as mpe
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import requests
# Imports the Google Cloud Translation library
from google.cloud import translate
# Define the function to download audio from YouTube

def download_audio(yt_url):
    yt = pytube.YouTube(yt_url)
    audio_mp4 = yt.streams.get_audio_only().download()
    return audio_mp4
# Define the function to convert audio to WAV
def convert_to_wav(audio_mp4):
    audio_clip = mpe.AudioFileClip(audio_mp4).set_fps(44100)
    audio_clip.write_audiofile("converted.wav")

# Define the function to transcribe audio
def transcribe_audio():
    r = sr.Recognizer()
    with sr.AudioFile("converted.wav") as source:
        audio_data = r.record(source)
    result = r.recognize_google(audio_data)
    return result

# Define the function to translate text to Telugu
def translate_to_hindi(text):
    try:
        # Translate the text to Telugu
        translation = translate_text(text)
        # Check if the translation is successful
        if translation is None:
            raise Exception("Translation failed")
        # Print the translated text for debugging
        #print("Translated Text:", translation)
        # Save the translation as an audio file
        tts = gTTS(translation, lang='hi')

        # Save the audio file
        tts.save("hindi.mp3")


    except Exception as e:
        # Handle the error
        print(e)

    # Initialize Translation client
def translate_text(text, project_id="rapid-hall-389114"):
  client = translate.TranslationServiceClient()
  location = "global"
  parent = f"projects/{project_id}/locations/{location}"
  response = client.translate_text(
      request={
          "parent": parent,
          "contents": [text],
          "mime_type": "text/plain",
          "source_language_code": "en-US",
          "target_language_code": "hi",
      }
  )
  # Get the translated text from the response
  translated_text = response.translations[0].translated_text
  return translated_text
# Define the function to save audio to a file
# Define the function to play audio
def play_audio(filename):
    os.system(f"start {filename}")

# Download audio from YouTube
url =input("enter the url of a short:")

audio_mp4 = download_audio(url)

# Convert audio to WAV
convert_to_wav(audio_mp4)

# Transcribe audio
transcribed_text = transcribe_audio()

# Translate text to Telugu
hindi_text = translate_to_hindi(transcribed_text)

# Save audio to a file

# Play audio
play_audio("hindi.mp3")
