import speech_recognition as sr
from gtts import gTTS
import tempfile
from pydub import AudioSegment

class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def audio_to_text(self, audio_file):
        """Process an uploaded audio file and convert it to text."""
        try:
            # Convert audio file to WAV format
            audio = AudioSegment.from_file(audio_file)
            wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            audio.export(wav_file.name, format="wav")
            print(f"Converted audio to WAV: {wav_file.name}")  # Debug statement

            with sr.AudioFile(wav_file.name) as source:
                audio = self.recognizer.record(source)
                try:
                    text = self.recognizer.recognize_google(audio)
                except sr.UnknownValueError:
                    text = "Could not understand audio"
                except sr.RequestError:
                    text = "Could not request results"
            print(f"Recognized text: {text}")  # Debug statement
            return text
        except Exception as e:
            print(f"Error processing audio file: {e}")  # Debug statement
            return f"Error processing audio file: {e}"

    def text_to_speech(self, text):
        """Convert text to speech using gTTS and save as a .mp3 file."""
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
            return temp_audio.name