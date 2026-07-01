import os
from dotenv import load_dotenv
import streamlit as st

# 加载环境变量
load_dotenv()

st.set_page_config(page_title="E2E Agent AI", page_icon="🤖", layout="wide")

st.title("📊 E2E Agent AI - Enterprise Dashboard")
st.markdown("基于 LangGraph + HubSpot REST API 的企业级 Agent 演示")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 引擎状态")
    st.success("LangGraph 核心: 已就绪")
    st.warning("HubSpot API: 待接通...")

# 核心聊天/展示区
from langchain_core.messages import HumanMessage
from agent.graph import app as agent_app

st.subheader("💡 CRM 数据洞察")
user_input = st.chat_input("向 Agent 提问 (例如: 帮我查一下最近新增的客户)")

if user_input:
    st.chat_message("user").write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Agent 正在思考并调用 HubSpot API..."):
            try:
                # 实际调用 LangGraph
                inputs = {"messages": [HumanMessage(content=user_input)]}
                response = agent_app.invoke(inputs)
                
                # 获取最后一条消息 (Agent 的回答)
                final_reply = response["messages"][-1].content
                st.write(final_reply)
                
            except Exception as e:
                st.error(f"Agent 执行出错: {str(e)}")
                st.info("💡 提示：请确保你的 .env 文件里配置了正确的 HUBSPOT_ACCESS_TOKEN 和 MINIMAX_API_KEY！")
