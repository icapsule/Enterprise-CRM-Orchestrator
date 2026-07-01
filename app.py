import os
from dotenv import load_dotenv
import streamlit as st

# 加载环境变量
load_dotenv()

st.set_page_config(page_title="E2E Agent AI", page_icon="🤖", layout="wide")

st.title("📊 E2E Agent AI - Enterprise Dashboard")
st.markdown("Enterprise-grade Agent demonstration powered by LangGraph & Multi-System REST APIs.")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ Engine Status")
    st.success("LangGraph Core: Ready")
    st.success("HubSpot Plugin: Connected")
    st.success("Salesforce Plugin: Connected (Mock)")

# 核心聊天/展示区
from langchain_core.messages import HumanMessage
from agent.graph import app as agent_app

st.subheader("💡 CRM Data Insights")
user_input = st.chat_input("Ask the Agent (e.g., Compare recent HubSpot contacts with Salesforce leads)")

if user_input:
    st.chat_message("user").write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Agent is reasoning and orchestrating plugins..."):
            try:
                # 实际调用 LangGraph
                inputs = {"messages": [HumanMessage(content=user_input)]}
                response = agent_app.invoke(inputs)
                
                # 获取最后一条消息 (Agent 的回答)
                final_reply = response["messages"][-1].content
                st.write(final_reply)
                
            except Exception as e:
                st.error(f"Agent Execution Error: {str(e)}")
                st.info("💡 Tip: Ensure your .env file is correctly configured with required API tokens.")
