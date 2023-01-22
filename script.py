import os
import urllib.request
from bs4 import BeautifulSoup
from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio(audio_url):
    # download audio file from url
    urllib.request.urlretrieve(audio_url, "audio.wav")
    # read audio file
    with open("audio.wav", "rb") as audio_file:
        content = audio_file.read()
    # setup client with api key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_API_KEY")
    client = speech.SpeechClient()
    # transcribe audio file
    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')
    response = client.recognize(config, audio)
    # get transcribed
    return response

def get_audio_urls():
    # download page source
    page = urllib.request.urlopen("https://oksenate.gov/live-chamber")
    soup = BeautifulSoup(page, "html.parser")
    # find audio file urls
    audio_urls = []
    for link in soup.find_all("a"):
        if "audio" in link.get("href"):
            audio_urls.append(link.get("href"))
    return audio_urls

def transcribe_all():
    audio_urls = get_audio_urls()
    for audio_url in audio_urls:
        response = transcribe_audio(audio_url)
        print(response)
