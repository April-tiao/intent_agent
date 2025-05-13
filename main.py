# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from agent import detect_cleanup_intent

app = FastAPI()

class InputData(BaseModel):
    input_q: str
    session_id: str

@app.get("/")
async def root():
    return {"message": "Welcome to Intent Detection API", "docs_url": "/docs"}

@app.post("/intent")
async def handle_intent(data: InputData):
    result = detect_cleanup_intent(data.session_id, data.input_q)

    # 类型映射：1表示“清站”
    mapped_type = "1" if result["type"] == "CLEAR_PASSENGER" else "0"

    return {
        "message": result["message"],
        "sessionId": data.session_id,
        "type": mapped_type
    }




