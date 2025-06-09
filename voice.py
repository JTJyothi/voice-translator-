import gradio as gr
import assemblyai as aai
from translate import Translator
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from pathlib import Path

def voice_to_voice(audio_file):
    #transcribe audio
    transcription_response=audio_transcription(audio_file)

    if transcription_response.status==aai.TranscriptStatus.error:
        raise gr.Error(transcription_response.error)
    else:
        text=transcription_response.text
    es_translation,de_translation,hi_translation,te_translation=text_translation(text)
    es_audio_path=text_to_speech(es_translation)
    de_audio_path=text_to_speech(de_translation)
    hi_audio_path=text_to_speech(hi_translation)
    te_audio_path=text_to_speech(te_translation)

    es_path=Path(es_audio_path)
    de_path=Path(de_audio_path)
    hi_path=Path(hi_audio_path)
    te_path=Path(te_audio_path)

    return es_path,de_path,hi_path,te_path


def audio_transcription(audio_file):
    aai.settings.api_key="your api key"
    transcriber=aai.Transcriber()
    transcription=transcriber.transcribe(audio_file)

    

    return transcription


def text_translation(text):
    Translator_es=Translator(from_lang="en",to_lang="es")
    es_text=Translator_es.translate(text)

    Translator_de=Translator(from_lang="en",to_lang="de")
    de_text=Translator_de.translate(text)

    Translator_hi=Translator(from_lang="en",to_lang="hi")
    hi_text=Translator_hi.translate(text)

    Translator_te=Translator(from_lang="en",to_lang="te")
    te_text=Translator_te.translate(text)
    return es_text,de_text,hi_text,te_text  


def text_to_speech(text):
    #sk_5a1835e01b6d5d2b0522b00131d6794cc2d0524216e67aee
    
    client = ElevenLabs(
        api_key='your eleven lab api',
)
    response = client.text_to_speech.convert(
        voice_id="your voice id", # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2", # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=1.0,
            style=0.5,
            use_speaker_boost=True,
        ),
    )


    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path
audio_input =gr.Audio(
    sources=["microphone"],
    type="filepath"
    
    )


demo=gr.Interface(
    fn=voice_to_voice,
    inputs=audio_input,
    outputs=[gr.Audio(label="German"),gr.Audio(label="Spanish"),gr.Audio(label="Hindi"),gr.Audio(label="Telugu")]
)

if __name__=="__main__":
    demo.launch(share=True)
