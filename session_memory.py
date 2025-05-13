# session_memory.py

from collections import defaultdict

# 保存对话历史 + 是否已确认意图
session_history = defaultdict(list)
session_confirmed = defaultdict(bool)

def get_history(session_id):
    return session_history[session_id]

def add_user(session_id, content):
    session_history[session_id].append({"role": "user", "content": content})

def add_assistant(session_id, content):
    session_history[session_id].append({"role": "assistant", "content": content})

def mark_confirmed(session_id):
    session_confirmed[session_id] = True

def is_confirmed(session_id):
    return session_confirmed[session_id]

def clear_session(session_id):
    session_history[session_id].clear()
    session_confirmed[session_id] = False
