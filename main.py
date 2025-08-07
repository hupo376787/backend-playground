from fastapi import FastAPI, Query, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
from datetime import datetime
from PIL import Image
import io
from pydantic import BaseModel

app = FastAPI()

# 可选：允许跨域（前端访问用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定你的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-time")
def get_temperature():
    timestamp = datetime.now().isoformat()
    return{
        "timestamp": timestamp
    }

@app.get("/get-temperature")
def get_temperature(city: str = Query(..., description="城市名称")):
    temperature = round(random.uniform(32, 36.5), 2)
    timestamp = datetime.now().isoformat()
    return{
        "city": city,
        "temperature": temperature,
        "timestamp": timestamp
    }

@app.post("/get-image-info")
async def get_image_info(file: UploadFile = File(...)):
    contents = await file.read()

    try:
        # 使用 PIL 解析图片尺寸
        image = Image.open(io.BytesIO(contents))
        width, height = image.size

        return {
            "filename": file.filename,
            "width": width,
            "height": height
        }
    except Exception as e:
        return {
            "error": "无法识别图片",
            "detail": str(e)
        }
    

    
# 模拟数据库中的用户信息（实际应查数据库）
fake_user_db = {
    "vincent": {
        "username": "vincent",
        "password": "123456",  # 实际应加密存储
        "full_name": "Vincent Wang"
    }
}

# 登录返回模型
class LoginResponse(BaseModel):
    message: str
    token: str = None
    full_name: str = None

@app.post("/login", response_model=LoginResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    user = fake_user_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 模拟生成 token（实际应用 JWT 等）
    token = f"token-{username}"

    return {
        "message": "登录成功",
        "token": token,
        "full_name": user["full_name"]
    }