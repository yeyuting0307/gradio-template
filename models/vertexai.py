#%%
import os
import uuid
import requests

GEMINI_API_URL = os.environ.get("GEMINI_API_URL")
IMAGEN_API_URL = os.environ.get("IMAGEN_API_URL")

def gemini(prompt:str, user_id:str = uuid.uuid4().hex):
    api_url = GEMINI_API_URL
    body = {
        "prompt": prompt,
        "user_id": user_id
    }
    res = requests.post(url=api_url, json=body)
    if res.status_code == requests.codes.ok:
        return res.json()
    else:
        return "gemini went wrong!"

def imagen(prompt:str, count:int=1):
    api_url = IMAGEN_API_URL
    body = {
        "prompt": prompt,
        "count": count
    }
    res = requests.post(url=api_url, json=body)
    if res.status_code == requests.codes.ok:
        return res.json()
    else:
        return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTV1eEqTbJiyge1htlBwZQ1rkhVZ4ItkweMEd4UFXih2w&s"

def imagen_edit(prompt:str, img, count):
    # TODO: Implement image editing function
    return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7Lb419S2crju9hKAXduBAN6rucZrp8-SxS_H2tWH_IFdBwcR8OrnHB_tIUE4UMAw6jPE&usqp=CAU"
