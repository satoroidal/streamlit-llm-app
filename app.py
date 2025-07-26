import streamlit as st
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

# Webアプリの概要・操作説明
st.title("専門家アドバイスアプリ")
st.write("""
このアプリは、選択した領域について専門家の視点でのアドバイスがもらえます。
下記の手順でご利用ください。

1. 専門家の種類をラジオボタンで選択してください。
2. 入力フォームに質問や相談内容を入力してください。
3. 「送信」ボタンを押すと、選択した専門家の視点でLLMが回答します。
""")

# 専門家の種類
experts = {
    "野球": "あなたは野球の専門家です。野球に関する質問に専門的かつ分かりやすく答えてください。",
    "サッカー": "あなたはサッカーの専門家です。サッカーに関する質問に専門的かつ分かりやすく答えてください。",
}

# ラジオボタンで専門家選択
selected_expert = st.radio("専門家の種類を選択してください", list(experts.keys()))

# 入力フォーム
user_input = st.text_input("質問や相談内容を入力してください")

def get_llm_response(user_text, expert_key):
    """入力テキストと専門家種別をもとにLLMから回答を取得"""
    system_prompt = experts[expert_key]
    chat = ChatOpenAI(temperature=0.7)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_text)
    ]
    response = chat(messages)
    return response.content

if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問内容を入力してください。")
    else:
        with st.spinner("LLMが回答中..."):
            answer = get_llm_response(user_input, selected_expert)
        st.markdown("#### 回答")
        st.write(answer)

