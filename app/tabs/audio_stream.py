import gradio as gr
from models.vertexai import imagen_edit
from models.whisper import pipe as transcriber
import numpy as np
IMG_MODELS = ["imagen"]

def transcribe(stream, new_chunk):
    sr, y = new_chunk
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    if stream is not None:
        stream = np.concatenate([stream, y])
    else:
        stream = y
    return stream, transcriber({"sampling_rate": sr, "array": stream})["text"]

def tab_audio_stream():

    return [
        gr.Interface(
            transcribe,
            ["state", gr.Audio(sources=["microphone"], streaming=False)],
            ["state", "text"],
            live=False,
        )
    ]
