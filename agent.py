import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from session_memory import (
    get_history, add_user, add_assistant,
    mark_confirmed, is_confirmed, clear_session
)

# 1) 读取 .env 中的变量
load_dotenv()
api_key   = os.getenv("OPENAI_API_KEY")      # 必填
base_url  = os.getenv("OPENAI_BASE_URL")     # 必填
model     = os.getenv("MODEL_NAME", "moonshot-v1-8k")   # 有默认值也行

# 2) 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

def build_confirmation_prompt(session_id, user_input):
    add_user(session_id, user_input)
    history = get_history(session_id)

    prompt = f"""
你是一个只能识别“是否要开始清站”这一指令的助手。

请判断以下上下文是否能确认用户意图为“开始清站”，并严格返回如下 JSON：
{{
  "confirmed": true/false,
  "reason": "简短说明，帮助调试"
}}

上下文对话内容如下：
{json.dumps(history, ensure_ascii=False)}
"""
    return prompt

def detect_cleanup_intent(session_id, user_input):
    if is_confirmed(session_id):
        return {
            "confirmed": True,
            "message": "已确认用户意图为清站。",
            "type": "CLEAR_PASSENGER"
        }

    prompt = build_confirmation_prompt(session_id, user_input)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    result = json.loads(response.choices[0].message.content.strip())
    if result.get("confirmed"):
        mark_confirmed(session_id)
        clear_session(session_id)
        return {
            "confirmed": True,
            "message": "已确认用户意图为清站。",
            "type": "CLEAR_PASSENGER"
        }
    else:
        add_assistant(session_id, "请问您是要开始清站吗？")
        return {
            "confirmed": False,
            "message": "请问您是要开始清站吗？",
            "type": "UNKNOWN"
        }
