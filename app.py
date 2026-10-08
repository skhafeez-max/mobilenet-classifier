from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import numpy as np
import io

from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)

app = FastAPI(title="MobileNet Image Classifier")

# Load pretrained MobileNetV2 model
model = MobileNetV2(weights="imagenet")

# Serve CSS and JavaScript
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "MobileNetV2"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()

    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image = image.resize((224, 224))

    image_array = np.array(image, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)

    image_array = preprocess_input(image_array)

    predictions = model.predict(image_array, verbose=0)

    decoded = decode_predictions(predictions, top=3)[0]

    results = []

    for _, label, confidence in decoded:
        results.append({
            "label": label,
            "confidence": float(confidence)
        })

    return {
        "filename": file.filename,
        "predictions": results
    }