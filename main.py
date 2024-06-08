from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # CORS 미들웨어 추가
import uvicorn
from typing import List
import subprocess
import shutil
import os

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.post("/predict/")
async def create_upload_files(file: UploadFile = File(...)):
    with open("temp.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # detect.py를 subprocess로 실행
    result = subprocess.run(['python3', './Gender-and-Age-Detection/detect.py', '--image', 'temp.jpg'], capture_output=True, text=True)
    
    # 결과 파싱 (연령 정보만 추출)
    age_info = result.stdout.strip()  # 연령 정보만 있는 줄을 기반으로, 앞뒤 공백을 제거합니다.
    
    # 연령 정보를 JSON 형태로 반환
    return JSONResponse(content={"message": "Detection completed", "age": age_info})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
