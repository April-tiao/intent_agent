# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from agent import detect_cleanup_intent

app = FastAPI()

# 修改字段名以匹配入参结构
class InputData(BaseModel):
    content: str
    sessionId: str

@app.get("/")
async def root():
    return {"message": "Welcome to Intent Detection API", "docs_url": "/docs"}

@app.post("/intent")
async def handle_intent(data: InputData):
    # 使用新的字段名
    result = detect_cleanup_intent(data.sessionId, data.content)

    # 类型映射：1表示“清站”
    mapped_type = "1" if result["type"] == "CLEAR_PASSENGER" else "0"

    return {
        "message": result["message"],
        "sessionId": data.sessionId,
        "type": mapped_type
    }
