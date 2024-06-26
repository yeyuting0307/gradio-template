import gradio as gr
import os
import sys
from os.path import abspath, join, dirname
from dotenv import load_dotenv

sys.path.append(abspath(join(dirname(__file__), '..')))
load_dotenv()

from app.tabs.question_answer import tab_qa
from app.tabs.image_generation import tab_img_gen
from app.tabs.image_editing import tab_img_edit
from app.tabs.chat_pdf import tab_pdf
from app.tabs.audio_stream import tab_audio_stream
def main():
    layout = gr.Blocks()

    with layout:
        with gr.Tab("問答系統"):
            tab_qa()
        with gr.Tab("圖片生成"):
            tab_img_gen()
        with gr.Tab("圖片編輯"):
            tab_img_edit()
        with gr.Tab("PDF問答"):
            tab_pdf()
        with gr.Tab("語音辨識"):
            tab_audio_stream()
            
    layout.launch(debug = True)

if __name__ == "__main__":
    main()
