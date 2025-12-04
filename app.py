import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# .env から環境変数を読み込む
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY が設定されていません。.env を確認してください。")
    st.stop()



st.title("専門家と話せるStreamlit アプリ 🧠💬")

st.write("##### 動作モード1: 歴史の専門家")
st.write("歴史について質問してください。")
st.write("##### 動作モード2: 投資の専門家")
st.write("投資について質問してください。")

expert_type = st.radio(
    "動作モードを選択してください。",
    ["歴史の専門家", "投資の専門家"]
)

st.markdown("---")

answer_placeholder = st.empty()




def get_expert_response(user_input, expert_type) :
    
    
    # 専門家タイプに応じたシステムメッセージを設定
    if expert_type == "歴史の専門家":
        system_message = "あなたは歴史の専門家です。歴史に関する質問に対して、正確で詳細な情報を提供してください。"
    else:  # 投資の専門家
        system_message = "あなたは投資の専門家です。投資に関する質問に対して、専門的なアドバイスを提供してください。"
    
    # LangChainを使用してLLMに問い合わせ
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=api_key)
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_input)
    ]
    
    result = llm.invoke(messages)
    return result.content

if expert_type == "歴史の専門家":
    user_input = st.text_input("歴史について質問してください。", key="history_input")
else:  # 投資の専門家
    user_input = st.text_input("投資について質問してください。", key="investment_input")
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("専門家が回答を考えています..."):
            answer = get_expert_response(user_input, expert_type)
        
        answer_placeholder.markdown("### 専門家の回答")
        answer_placeholder.write(answer)
        