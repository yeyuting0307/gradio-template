#%%
import gradio as gr 
import logging
from gradio_pdf import PDF
from utils.pdf import PdfParser
from utils.embed import Embedder
from models.vertexai import gemini

def retriever_qa(question, relate_docs, reply_language, user_id):
    prompt = f''' 
        Reply questions based on the following <context>:
        <context>
        {"".join([doc.page_content for doc in relate_docs])}
        </context>

        Question: {question}
        Answer(in {reply_language} language):
    '''
    logging.debug(f"Prompt: {prompt}")
    answer = gemini(prompt, user_id)
    return answer

def pdf_interpreter(
        question, 
        reply_language, 
        pdf_path,
        include_images, 
        request:gr.Request
    ):
    user_id = request.headers.get('cookie')
    pdf_parser = PdfParser(include_images=include_images)
    contents = []
    for page, _ in pdf_parser.lazy_parse(pdf_path):
        contents.append(page)
    embed = Embedder(contents)
    relate_docs = embed.retrieve_docs(question)
    answer = retriever_qa(question, relate_docs, reply_language, user_id)

    return answer

def tab_pdf():
    input_question = gr.Textbox(lines=3, label="關於PDF內容的問題")
    input_language = gr.Radio(value="繁體中文", choices=["繁體中文", "English"], label="回覆語系")
    input_pdf = PDF(label="上傳您的PDF")
    input_img_check = gr.Checkbox(value=False, label="使用OCR解析PDF文字")

    output_answer = gr.Textbox(label="Answer", lines=7)

    return gr.Interface(
        fn = pdf_interpreter,
        inputs = [input_question, input_language, input_pdf, input_img_check],
        outputs = output_answer,
        title="Chat PDF",
    )

