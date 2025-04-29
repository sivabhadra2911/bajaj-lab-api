from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import tempfile
import os

from utils.ocr_utils import extract_text_from_image
from utils.parser import parse_lab_tests

app = FastAPI()

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        text = extract_text_from_image(tmp_path)
        lab_data = parse_lab_tests(text)

        os.unlink(tmp_path)  # Clean up temp file

        return JSONResponse(content={
            "is_success": True,
            "data": lab_data
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "is_success": False,
            "error": str(e)
        })
