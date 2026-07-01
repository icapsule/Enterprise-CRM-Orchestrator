import os
import requests
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool

# 1. 定义状态机 (State)
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# 2. 定义原生 Tool (HubSpot REST API)
@tool
def fetch_hubspot_contacts(limit: int = 5):
    """
    通过 HubSpot REST API 获取最新的联系人列表。
    当用户询问关于客户、联系人等信息时调用此工具。
    """
    token = os.getenv("HUBSPOT_ACCESS_TOKEN")
    if not token or token.startswith("pat-na1-xxxxxx"):
        return "Error: HUBSPOT_ACCESS_TOKEN is missing or invalid. Please check your .env file."
    
    url = f"https://api.hubapi.com/crm/v3/objects/contacts?limit={limit}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # 提取关键信息以减少上下文占用
        results = []
        for contact in data.get('results', []):
            props = contact.get('properties', {})
            results.append({
                "id": contact.get('id'),
                "name": f"{props.get('firstname', '')} {props.get('lastname', '')}".strip(),
                "createdate": props.get('createdate')
            })
        return str(results)
    except Exception as e:
        return f"Error fetching contacts from HubSpot: {str(e)}"

# 将工具打包供大模型绑定
tools = [fetch_hubspot_contacts]

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# 3. 编排工作流
# 使用 Google Gemini 2.5 Flash (目前最新的主力模型)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 使用 LangGraph 预置的 ReAct Agent，它会自动帮我们处理工具的循环调用
app = create_react_agent(llm, tools=tools)
