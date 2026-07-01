import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

# 1. 动态引入所有集成系统插件 (Plugin Registry)
from agent.plugins.registry import ALL_TOOLS

# 2. 编排工作流 (Enterprise-grade Resilience)
# 主模型 (Primary): Google Gemini 2.5 Flash
primary_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    max_retries=1 # 快速失败，立即触发 Fallback
)

# 备用模型 (Fallback): MiniMax (采用 Anthropic 兼容协议接入)
# 当 Gemini 触发 429 限流或服务中断时，大脑将在毫秒级内自动降级到 MiniMax 引擎，业务不中断
fallback_llm = ChatAnthropic(
    model_name="MiniMax-M3",
    api_key=os.getenv("MINIMAX_API_KEY"),
    base_url="https://api.minimax.chat/anthropic",
    max_retries=1
)

# 绑定多模型灾备链 (Failover Chain)
llm = primary_llm.with_fallbacks([fallback_llm])

# 3. 语义路由指南 (Semantic Routing Prompt)
# 针对单租户多系统的定制化场景，我们在这里强加给大模型极其明确的系统分发指令，避免模型在多系统之间迷失。
system_prompt = """
You are the central Enterprise Integration Hub Agent. Your job is to route user queries to the correct internal system and execute B2B sales automation workflows.
RULES:
1. If the user asks about "Contacts", "Customers", or anything explicitly related to HubSpot, you MUST use the `fetch_hubspot_contacts` tool.
2. If the user asks about "Leads", "Prospects", or anything explicitly related to Salesforce, you MUST use the `fetch_salesforce_leads` tool.
3. If the user asks a question requiring data from both, you must call BOTH tools sequentially and combine the results into a unified report.
4. Default to Professional English for responses, but if the user asks in another language, respond in that language.
5. You possess the power to TAKE ACTION on leads:
   - To schedule follow-ups, use `schedule_crm_followup_task`.
   - To notify the team of high-value updates, use `send_slack_alert`.
6. When a user asks you to "follow up" or "take action" on a lead:
   - First, gather the lead data.
   - Draft a highly personalized outreach email or proposal.
   - Call `schedule_crm_followup_task` to lock in the follow-up workflow.
   - Call `send_slack_alert` if it's a high-value lead (estimated value >= $200k) or if explicitly requested.
   - Summarize the actions taken and show the drafted outreach in your final response.
"""

# 4. 初始化具备多系统能力的 Agent
app = create_react_agent(
    llm, 
    tools=ALL_TOOLS, 
    prompt=system_prompt
)
