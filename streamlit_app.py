import os
from dotenv import load_dotenv
import streamlit as st

# 加载环境变量
load_dotenv()

st.set_page_config(page_title="E2E Agent AI", page_icon="🦜", layout="wide")

# Inject Custom CSS to match LangSmith/LangChain website brand identity
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Font & Background */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* Header border line */
    [data-testid="stHeader"] {
        background-color: rgba(248, 250, 252, 0.8) !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }

    /* Streamlit success/info alerts custom styling to match LangSmith panels */
    div[data-testid="stNotification"] {
        border-radius: 8px !important;
        background-color: #ffffff !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05) !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Link Button Styling (LangChain Green) */
    .stLinkButton > a {
        background-color: #10b981 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        text-decoration: none !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .stLinkButton > a:hover {
        background-color: #059669 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2) !important;
    }

    /* Expander styling as clean dashboard cards */
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 20px !important;
    }
    
    /* Chat Input Bar */
    [data-testid="stChatInput"] {
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom Brand Header (LangChain style)
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 15px; margin-top: -45px; margin-bottom: 25px; border-bottom: 1px solid #e2e8f0; padding-bottom: 20px;">
        <div style="background-color: #0f172a; padding: 12px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 32px;">🦜</span>
        </div>
        <div>
            <h1 style="margin: 0; font-size: 26px; font-weight: 700; color: #0f172a; letter-spacing: -0.03em;">E2E Agent AI</h1>
            <p style="margin: 0; color: #64748b; font-size: 14px; font-weight: 450;">Enterprise-grade Agent demonstration powered by LangGraph & Multi-System REST APIs.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ Engine Status")
    st.success("LangGraph Core: Ready")
    st.success("HubSpot Plugin: Connected")
    st.success("Salesforce Plugin: Connected (Mock)")
    
    st.markdown("---")
    st.header("🔍 Observability")
    st.link_button("🛠️ Open LangSmith Trace", "https://eu.smith.langchain.com")
    
    st.markdown("---")
    st.header("💬 IM Integrations")
    st.info("MS Teams (To be developed)")
    st.info("Slack Bot (To be developed)")
    st.info("Telegram Bot (To be developed)")

# 核心聊天/展示区
from langchain_core.messages import HumanMessage, AIMessage
from agent.engine import get_agent

st.subheader("💡 CRM Data Insights")

# 10 Suggested Demonstration Queries for Clients
with st.expander("📋 Recommended Enterprise Demo Scenarios (Click to expand)"):
    st.markdown("### ⚡ Level 2: B2B Business Process Automation (Autonomous Agent)")
    st.markdown("""
    These scenarios demonstrate the Agent's ability to **take action, make decisions, and execute multi-step workflows** (Read -> Decide -> Generate -> Write/Notify):
    
    *   **Scenario A: B2B Lead Follow-up & CRM Task creation:**  
        `Find our highest-value B2B lead in Salesforce, write a personalized email to them in Swedish, and schedule a CRM follow-up task.`
    *   **Scenario B: High-Value Alerting & Slack Notification:**  
        `Check if we have any lead from Klarna. If their budget is over $200k, send a Slack alert to #sales-vip and schedule a follow-up task to call them tomorrow.`
    *   **Scenario C: Cross-System Automated Audit:**  
        `Check if we have a contact matching Volvo Group in HubSpot. If yes, schedule a CRM follow-up task to sync details and alert the owner Sven Lindberg via Slack.`
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔍 Level 1: CRM Data Analytics & Inquiry (RAG)")
    st.markdown("""
    These queries demonstrate the Agent's ability to **search, aggregate, and reason over data** from HubSpot and Salesforce:
    
    1. **Pipeline Summary:** `Summarize all B2B leads currently in our Salesforce pipeline.`
    2. **High-Value Targets:** `List all Salesforce leads with an estimated deal value greater than $200,000.`
    3. **Hot Prospects:** `Find all 'Hot Lead' status prospects in Salesforce and show their contact emails.`
    4. **Sales Rep Load:** `Which Salesforce leads are currently assigned to Sven Lindberg?`
    5. **Source ROI:** `What is the total estimated value of leads generated from 'Web Inquiry'?`
    6. **Cross-System Analysis:** `Compare HubSpot contacts with Salesforce leads to see if we have any company overlaps.`
    7. **Priority Ranking:** `Rank our top 3 highest-value Salesforce leads and show their budget.`
    8. **Contact Validation:** `Check if we have a contact in HubSpot that matches Lars Andersson from Volvo Group.`
    9. **Total Pipeline Valuation:** `Calculate the total pipeline budget value of all Salesforce leads combined.`
    10. **Multilingual Email Drafting:** `Draft a professional B2B follow-up email in Swedish to Sofia Lindqvist from Klarna Bank regarding her $300,000 lead.`
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
                
                # Invoke LangGraph (dynamically get agent with rotated API Key)
                inputs = {"messages": chat_history}
                response = get_agent().invoke(inputs)
                
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
