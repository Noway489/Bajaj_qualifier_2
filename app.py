import os
import re
import cv2
import numpy as np
import pytesseract
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
# Set up Jinja2 templates directory
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# 1) Preprocessing (same as before)
def preprocess(img_bytes: bytes):
    nparr = np.frombuffer(img_bytes, np.uint8)
    img   = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur  = cv2.GaussianBlur(gray, (5,5), 0)
    _, th = cv2.threshold(blur, 0, 255,
                         cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    return th

# 2) (Optional) Text-region detection with EAST or simple full-page OCR
def detect_text_regions(img):
    # for simplicity you can just return the full-image bbox
    h, w = img.shape[:2]
    return [(0, 0, w, h)]

def ocr_crop(img, bbox):
    x1, y1, x2, y2 = bbox
    roi = img[y1:y2, x1:x2]
    return pytesseract.image_to_string(roi, config='--psm 6').strip()

# 3) Improved regex to capture name, value, unit, and the “low-high”
LINE_PATTERN = re.compile(
    r'(?P<test_name>[\w \(\)\%/]+?)\s+'           # name
    r'(?P<test_value>[\d\.]+)\s*'                 # value
    r'(?P<test_unit>[\w/%µ]+)?\s*'                # optional unit
    r'\(?(?P<bio_reference_range>[\d\.]+[-–][\d\.]+)\)?'  # range
)

def parse_line(line: str):
    m = LINE_PATTERN.search(line)
    if not m:
        return None

    val = float(m.group('test_value'))
    lo, hi = map(float, m.group('bio_reference_range').replace('–','-').split('-'))
    return {
        "test_name":           m.group('test_name').strip(),
        "test_value":          m.group('test_value'),
        "bio_reference_range": m.group('bio_reference_range'),
        "test_unit":           (m.group('test_unit') or "").strip(),
        "lab_test_out_of_range": not (lo <= val <= hi)
    }

# 4) Upload page
@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

# 5) Processing endpoint
@app.post("/get-lab-tests", response_class=HTMLResponse)
async def get_lab_tests(request: Request, file: UploadFile = File(...)):
    img_bytes = await file.read()
    pre = preprocess(img_bytes)
    regions = detect_text_regions(pre)
    extracted = []
    for bbox in regions:
        text = ocr_crop(pre, bbox)
        for line in text.splitlines():
            parsed = parse_line(line)
            if parsed:
                extracted.append(parsed)

    # Render results page
    return templates.TemplateResponse(
        "results.html", {"request": request, "data": extracted}
    )

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
