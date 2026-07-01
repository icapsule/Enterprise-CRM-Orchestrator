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
from langchain_core.messages import HumanMessage, AIMessage
from agent.engine import app as agent_app

st.subheader("💡 CRM Data Insights")

# 10 Suggested Demonstration Queries for Clients
with st.expander("📋 10 Recommended Enterprise Demo Scenarios (Click to expand)"):
    st.markdown("""
    Here are 10 B2B business scenarios. The first 3 demonstrate **Autonomous Task Execution (Actions)**, while the rest showcase intelligent data analysis:
    
    1. **🤖 Task Execution: B2B Lead Follow-up:**  
       `Find our highest-value B2B lead in Salesforce, write a personalized email to them in Swedish, and schedule a CRM follow-up task.`
       *(Agent will fetch leads -> identify Ericsson -> draft a Swedish proposal email -> call CRM Task tool)*
       
    2. **🤖 Multi-Step: High-Value Alerting:**  
       `Check if we have any lead from Klarna. If their budget is over $200k, send a Slack alert to #sales-vip and schedule a follow-up task to call them tomorrow.`
       *(Agent will fetch leads -> find Klarna -> execute Slack webhook notification -> call CRM Task tool)*

    3. **🤖 Automated Integration Check:**  
       `Check if we have a contact matching Volvo Group in HubSpot. If yes, schedule a CRM follow-up task to sync Ericsson details and alert the owner Sven Lindberg via Slack.`
       *(Agent will call HubSpot API -> search contacts -> trigger CRM Task tool -> send Slack notification)*

    4. **Pipeline Summary:** `Summarize all B2B leads currently in our Salesforce pipeline.`
    5. **High-Value Targets:** `List all Salesforce leads with an estimated deal value greater than $200,000.`
    6. **Hot Prospects:** `Find all 'Hot Lead' status prospects in Salesforce and show their contact emails.`
    7. **Sales Rep Load:** `Which Salesforce leads are currently assigned to Sven Lindberg?`
    8. **Source ROI:** `What is the total estimated value of leads generated from 'Web Inquiry'?`
    9. **Priority Ranking:** `Rank our top 3 highest-value Salesforce leads and show their budget.`
    10. **Total Pipeline Valuation:** `Calculate the total pipeline budget value of all Salesforce leads combined.`
    """)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask the Agent...")

if user_input:
    # Display user message immediately
    st.chat_message("user").write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Agent is reasoning and orchestrating plugins..."):
            try:
                # Build the chat history for LangGraph memory
                chat_history = []
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        chat_history.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        chat_history.append(AIMessage(content=msg["content"]))
                
                # Append current user input
                chat_history.append(HumanMessage(content=user_input))
                
                # Invoke LangGraph
                inputs = {"messages": chat_history}
                response = agent_app.invoke(inputs)
                
                # Extract only the text content (handle Gemini block format)
                final_reply = response["messages"][-1].content
                if isinstance(final_reply, list):
                    text_parts = []
                    for part in final_reply:
                        if isinstance(part, dict) and "text" in part:
                            text_parts.append(part["text"])
                        elif isinstance(part, str):
                            text_parts.append(part)
                    final_reply = "\n".join(text_parts)
                
                # Render response
                st.write(final_reply)
                
                # Save to session state history
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "assistant", "content": final_reply})
                
            except Exception as e:
                st.error(f"Agent Execution Error: {str(e)}")
                st.info("💡 Tip: Ensure your .env file is correctly configured with required API tokens.")
