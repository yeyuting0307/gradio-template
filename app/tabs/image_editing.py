import gradio as gr
from models.vertexai import imagen_edit

IMG_MODELS = ["imagen"]

def edit_image(
        img:gr.components.image.Image, 
        text:str,  
        model:str,
        count:int
    ):
    if model == "imagen":
        ## TODO: Implement image editing function here
        img_url = imagen_edit(text, img, count)
    else:
        return "https://qrup.files.wordpress.com/2017/03/working-on-it-large.gif" 
    return img_url

def tab_img_edit():
    input_edit_image = gr.Image(label="貼上或上傳您的圖片", sources = ['clipboard', 'upload', 'webcam'])
    input_edit_text = gr.Textbox(label="描述您想怎麼修改圖片", lines=3)
    input_model = gr.Radio(choices=IMG_MODELS, value = IMG_MODELS[0], label="選擇AI模型")
    input_count = gr.Number(label="生成張數", value=1, minimum=1, maximum=4)
    output_edit = gr.Image(label="已修改的圖片")

    return [
        gr.Interface(
            fn=edit_image, 
            inputs=[input_edit_image, input_edit_text, input_model, input_count], 
            outputs=[output_edit], 
            title="Image Editor"
        )
    ]
