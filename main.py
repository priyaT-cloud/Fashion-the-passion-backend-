from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

# Use Hugging Face Kolors-Virtual-Try-On as demo API
HF_TRYON_URL = "https://kwai-kolors-kolors-virtual-try-on.hf.space/api/predict"

@app.post("/try-on/")
async def try_on(user_photo: UploadFile = File(...), garment_photo: UploadFile = File(...)):
    user_image = await user_photo.read()
    clothing_image = await garment_photo.read()
    # Send both images to the Hugging Face demo API
    response = requests.post(
        HF_TRYON_URL,
        files={
            "data": (user_photo.filename, user_image, user_photo.content_type),
            "data": (garment_photo.filename, clothing_image, garment_photo.content_type)
        }
    )
    tryon_image_url = ""
    if response.ok:
        # The demo returns JSON with output image url/base64
        result = response.json()
        if "data" in result and result["data"]:
            tryon_image_url = result["data"][0]
    return {"result_image": tryon_image_url}

@app.post("/recommend/")
async def recommend(query: dict):
    user_message = query.get("query", "")
    # For a true AI assistant, connect to OpenAI or Hugging Face NLP API
    # Here, static advice is returned for demo
    if any(word in user_message.lower() for word in ["color", "combination", "trend"]):
        advice = "Earth tones and pastel combinations are really trending right now. Try pairing beige with mint green or lavender!"
    elif any(word in user_message.lower() for word in ["celebrity", "style"]):
        advice = "Zendaya’s red carpet looks are a top celebrity trend—consider statement accessories and bold colors!"
    else:
        advice = "You look fantastic! Try gold accessories for a luxe finish."
    return {"advice": advice}



