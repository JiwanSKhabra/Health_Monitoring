from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import base64
import uuid
import os

# === FastAPI setup ===
app = FastAPI()

# === Template and Static setup ===
BASE_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
SAVE_DIR = os.path.join(BASE_DIR, "face_images")

os.makedirs(SAVE_DIR, exist_ok=True)

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# === Data model for POSTed image ===
class ImageData(BaseModel):
    image: str

# === Route to render form ===
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# === Route to accept base64 image and save ===
@app.post("/verify-face")
async def verify_face(data: ImageData):
    try:
        # Determine format from base64 prefix
        if "," in data.image:
            header, base64_data = data.image.split(",", 1)
            if "image/jpeg" in header:
                ext = "jpg"
            elif "image/png" in header:
                ext = "png"
            else:
                ext = "img"  # fallback
        else:
            base64_data = data.image
            ext = "img"

        # Decode and save
        image_bytes = base64.b64decode(base64_data)
        filename = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(SAVE_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        return {"status": "success", "filename": filename}

    except Exception as e:
        return {"status": "error", "message": str(e)}
