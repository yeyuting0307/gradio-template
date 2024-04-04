import gradio as gr
from models.vertexai import gemini

LLM_OPTIONS = ["gemini-1.0-pro", "gpt-3.5-turbo"]

def call_llm(question:str, llm_option:str, request:gr.Request):
    user_id = request.headers.get('cookie')
    if llm_option == "gemini-1.0-pro":
        answer = gemini(question, user_id)
    elif llm_option == "gpt-3.5-turbo":
        answer = "GPT-3.5 Turbo is not available yet."
    else:
        answer = "Model not found."
    return answer

def tab_qa():
    input_text = gr.Textbox(label="輸入您的問題", lines=7)
    input_llm = gr.Radio(choices=LLM_OPTIONS, value = LLM_OPTIONS[0], label="選擇AI模型")
    output_text = gr.Textbox(label="AI提供的參考回答", lines=7)
    return [
        gr.Interface(
            fn=call_llm,
            inputs=[input_text, input_llm], 
            outputs=[output_text], 
            title="Question Answering"
        )
    ]
