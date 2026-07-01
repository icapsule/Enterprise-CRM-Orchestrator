import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

# 1. 动态引入所有集成系统插件 (Plugin Registry)
from agent.plugins.registry import ALL_TOOLS

# 2. 编排工作流
# 使用 Google Gemini 2.5 Flash (目前最新的主力模型)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 3. 语义路由指南 (Semantic Routing Prompt)
# 针对单租户多系统的定制化场景，我们在这里强加给大模型极其明确的系统分发指令，避免模型在多系统之间迷失。
system_prompt = """
You are the central Enterprise Integration Hub Agent. Your job is to route user queries to the correct internal system via the provided tools.
RULES:
1. If the user asks about "Contacts", "Customers", or anything explicitly related to HubSpot, you MUST use the `fetch_hubspot_contacts` tool.
2. If the user asks about "Leads", "Prospects", or anything explicitly related to Salesforce, you MUST use the `fetch_salesforce_leads` tool.
3. If the user asks a question requiring data from both, you must call BOTH tools sequentially and combine the results into a unified report.
4. Default to Professional English for responses, but if the user asks in another language, respond in that language.
"""

# 4. 初始化具备多系统能力的 Agent
app = create_react_agent(
    llm, 
    tools=ALL_TOOLS, 
    state_modifier=system_prompt
)
