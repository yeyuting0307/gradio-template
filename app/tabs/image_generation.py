import gradio as gr
from models.vertexai import imagen

IMG_MODELS = ["imagen", "dall-e-3"]

def gen_image(text:str, model: str, count:int, request:gr.Request):
    if model == "imagen":
        img_url = imagen(text, count)
    elif model == "dall-e-3":
        # TODO: Implement dall-e-3 image generation function
        return "https://qrup.files.wordpress.com/2017/03/working-on-it-large.gif" 
    else:
        return "https://i.pinimg.com/originals/a6/35/e5/a635e54a651dafb7e2edd1605de98087.png"
    return img_url

def tab_img_gen():
    # Generate Image
    input_text = gr.Textbox(label="描述您想生成的圖片", lines=7)
    input_model = gr.Radio(choices=IMG_MODELS, value = IMG_MODELS[0], label="選擇AI模型")
    input_count = gr.Number(label="生成張數", value=1, minimum=1, maximum=4)
    output_gen = gr.Image(label="生成的圖片(可複製或下載)")

    return [
        gr.Interface(
            fn=gen_image, 
            inputs=[input_text, input_model, input_count], 
            outputs=[output_gen], 
            title="Image Generator"
        )
    ]
