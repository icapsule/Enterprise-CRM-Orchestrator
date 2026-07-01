import os
import itertools
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

# 1. 动态引入所有集成系统插件 (Plugin Registry)
from agent.plugins.registry import ALL_TOOLS

# 支持多 Key 轮询 (Round Robin) 机制
# 会自动将 GOOGLE_API_KEY 按逗号切分为列表，使用 itertools.cycle 实现高效、线程安全的无缝轮替
gemini_keys = [k.strip() for k in os.getenv("GOOGLE_API_KEY", "").split(",") if k.strip()]
key_cycle = itertools.cycle(gemini_keys)

# 备用模型 (Fallback): MiniMax (采用 Anthropic 兼容协议接入)
# 当 Gemini 触发 429 限流或服务中断时，大脑将在毫秒级内自动降级到 MiniMax 引擎，业务不中断
fallback_llm = ChatAnthropic(
    model_name="MiniMax-M2.7",
    api_key=os.getenv("MINIMAX_API_KEY"),
    base_url="https://api.minimax.chat/anthropic",
    max_retries=1
)

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

def get_agent():
    """
    动态获取编译好的 Agent 实例。每次调用时会自动轮换 GOOGLE_API_KEY。
    如果完全没有配置 GOOGLE_API_KEY，系统会自动降级将 MiniMax 作为唯一的主力模型运行。
    """
    # 如果没有配置任何 Gemini Key，直接使用 MiniMax 作为主力引擎
    if not gemini_keys:
        return create_react_agent(
            fallback_llm, 
            tools=ALL_TOOLS, 
            messages_modifier=system_prompt
        )
        
    current_key = next(key_cycle)
    
    # 实例化当前请求的 Primary LLM
    primary_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=current_key,
        max_retries=1
    )
    
    # 融合灾备降级机制
    llm = primary_llm.with_fallbacks([fallback_llm], exceptions_to_handle=[Exception])
    
    # 动态编译并返回 Agent 实例
    return create_react_agent(
        llm, 
        tools=ALL_TOOLS, 
        messages_modifier=system_prompt
    )
