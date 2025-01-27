import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
warnings.filterwarnings("ignore", category=UserWarning, module="torchaudio")

import requests
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering, Wav2Vec2Processor, Wav2Vec2ForCTC
import os
import torchaudio

processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

audio_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
audio_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

def answer_visual_question(image_path_or_url: str, question: str) -> str:
    if os.path.isfile(image_path_or_url):
        raw_image = Image.open(image_path_or_url).convert('RGB')
    else:
        raw_image = Image.open(requests.get(image_path_or_url, stream=True).raw).convert('RGB')
    
    inputs = processor(raw_image, question, return_tensors="pt")
    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)

def transcribe_audio(audio_path: str) -> str:
    waveform, sample_rate = torchaudio.load(audio_path)
    inputs = audio_processor(waveform, sampling_rate=sample_rate, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = audio_model(inputs.input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = audio_processor.batch_decode(predicted_ids)
    return transcription[0]