from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from PIL import Image
from rembg import remove
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-psd")
async def process_psd(file: UploadFile = File(...)):
    contents = await file.read()
    img_rgb = Image.open(io.BytesIO(contents)).convert("RGB")
    width, height = img_rgb.size

    # 1. فصل العنصر/الشخصية
    fg = remove(img_rgb).convert("RGBA")

    # 2. ترقيع وترميم الخلفية وراء العناصر
    alpha = np.array(fg)[:, :, 3]
    mask = (alpha > 10).astype(np.uint8) * 255
    kernel = np.ones((12, 12), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel, iterations=1)
    
    bg_np = cv2.inpaint(np.array(img_rgb), dilated_mask, 7, cv2.INPAINT_TELEA)
    bg = Image.fromarray(bg_np).convert("RGBA")

    # 3. إنشاء وتجميع طبقات PSD المفتوحة
    psd = PSDImage.new("RGB", (width, height))
    psd.append(PixelLayer.frompil(bg, psd, "Background"))
    psd.append(PixelLayer.frompil(fg, psd, "Objects"))

    output_path = "/tmp/full_magic_layers.psd"
    psd.save(output_path)
    
    return FileResponse(output_path, media_type="application/octet-stream", filename="magic_layers.psd")
