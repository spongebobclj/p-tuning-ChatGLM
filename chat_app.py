import streamlit as st
import requests

st.set_page_config(page_title="医疗助手 ChatGLM2", layout="centered")

# 自定义样式
st.markdown("""
    <style>
    body {
        background-color: #f0fdf4;
    }
    .message-container {
        display: flex;
        margin: 10px 0;
        max-width: 700px;
        word-wrap: break-word;
    }
    .user-message {
        justify-content: flex-end;
    }
    .bot-message {
        justify-content: flex-start;
    }
    .message-bubble {
        padding: 12px 16px;
        border-radius: 20px;
        max-width: 80%;
        font-size: 16px;
        line-height: 1.5;
    }
    .user-bubble {
        background-color: #bbf7d0;
        color: #065f46;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .bot-bubble {
        background-color: #ecfdf5;
        color: #047857;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .title-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# 顶部标题 + 清空按钮
st.markdown('<div class="title-bar"><h2>🤖 ChatGLM2 医疗助手</h2>', unsafe_allow_html=True)
clear = st.button("🧹 清空对话", key="clear")
st.markdown('</div>', unsafe_allow_html=True)

# 初始化历史记录
if "history" not in st.session_state:
    st.session_state.history = []

# 处理清空按钮
if clear:
    st.session_state.history = []
    st.rerun()

# 聊天记录显示
for user_msg, bot_msg in st.session_state.history:
    st.markdown(f"""
        <div class="message-container user-message">
            <div class="message-bubble user-bubble">🧑‍⚕️ {user_msg}</div>
        </div>
        <div class="message-container bot-message">
            <div class="message-bubble bot-bubble">🤖 {bot_msg}</div>
        </div>
    """, unsafe_allow_html=True)

# 输入框
user_input = st.chat_input("请输入您的问题...")

if user_input:
    with st.spinner("思考中..."):
        payload = {
            "prompt": user_input,
            "history": st.session_state["history"],
            "max_length": 2048,
            "top_p": 0.7,
            "temperature": 0.95
        }

        try:
            response = requests.post("http://localhost:6006/", json=payload)
            result = response.json()
            bot_response = result["response"]

            st.session_state.history.append((user_input, bot_response))
            st.rerun()

        except Exception as e:
            st.error(f"请求出错：{e}")
