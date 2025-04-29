# Bajaj_qualifier_2
The project made as part of Babaj plcement exam
# Lab Test Extraction API

A simple web application that extracts lab‐test values (name, numeric result, units, reference range) from an uploaded image, flags out-of-range results, displays them in a clean HTML table, and immediately serves a downloadable JSON file of the data.

---

## 🚀 Features

- **Image Upload** via browser form  
- **Preprocessing** (grayscale → blur → Otsu threshold) with OpenCV  
- **OCR** using Tesseract (`pytesseract`)  
- **Regex Parsing** to extract:  
  - Test Name  
  - Numeric Value  
  - Unit (e.g. %, µ)  
  - Reference Range (low–high)  
  - Boolean flag for “out of range”  
- **Results Page** rendered with Jinja2 templates  
- **Immediate JSON Download** of parsed results  
- **Responsive, Modern UI** with vanilla CSS  

---

## 🔧 Prerequisites

1. **Python 3.8+**  
2. **Tesseract OCR** installed on your system  
   - **macOS (Homebrew):**  
     ```bash
     brew install tesseract
     ```  
   - **Ubuntu / Debian:**  
     ```bash
     sudo apt update
     sudo apt install tesseract-ocr
     ```  
   - **Windows:**  
     Download and install from [github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract).  
     Ensure the install directory (e.g. `C:\Program Files\Tesseract-OCR`) is in your `PATH`, or set `pytesseract.pytesseract.tesseract_cmd` accordingly in `app.py`.  

---
