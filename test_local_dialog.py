# test_local_dialog.py
import os
import sys
import json
from dotenv import load_dotenv
from agent import detect_cleanup_intent
from session_memory import clear_session

# ① 读取 .env，确保 API 密钥可用
load_dotenv()

def test_dialog(session_id: str = "test001"):
    print("=== 多轮清站意图识别测试 ===")
    print("输入 'exit' 退出\n")

    while True:
        try:
            user_input = input("用户：")
        except KeyboardInterrupt:
            print("\n退出测试")
            break

        if user_input.strip().lower() == "exit":
            break

        # ② 调用智能体
        result = detect_cleanup_intent(session_id, user_input)
        print(f"🤖 智能体：{result['message']} (type={result['type']})")

        # ③ 一旦确认意图，结束对话
        if result["type"] == "CLEAR_PASSENGER":
            print("✅ 已确认清站意图，结束对话")
            break

    # ④ 清理会话缓存，方便下次测试
    clear_session(session_id)

if __name__ == "__main__":
    # 可在命令行传入自定义 session_id：python test_local_dialog.py my_session
    sid = sys.argv[1] if len(sys.argv) > 1 else "test001"
    test_dialog(sid)
