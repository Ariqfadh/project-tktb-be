from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import requests
from io import BytesIO

app = FastAPI()

MODEL_SERVER_URL = "http://127.0.0.1:8080/predictions/skin_model"

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    # Read file contents
    image_data = await file.read()
    
    # Send the image to the model server
    response = requests.post(MODEL_SERVER_URL, files={"data": image_data})

    # Check if the request was successful
    if response.status_code != 200:
        return {"error": "Failed to process image"}

    # Get the annotated image from the response
    annotated_image = response.content

    # Send back the annotated image to the client
    return StreamingResponse(BytesIO(annotated_image), media_type="image/jpeg")