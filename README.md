# E2E Enterprise Agent AI: CRM Integration MVP

> An enterprise-grade, autonomous AI Agent architecture demonstrating dynamic tool-calling and real-time CRM data reasoning.

## 📌 Executive Summary

This project is a Minimum Viable Product (MVP) designed to validate an **End-to-End (E2E) AI Agent pipeline**. It connects a modern chat interface with a powerful Large Language Model (LLM) orchestration engine, enabling the AI to autonomously fetch, analyze, and render live customer data from an external CRM system (HubSpot) using REST APIs.

## 🏗 Architecture & Tech Stack

The architecture is built upon industry-standard, production-ready frameworks, emphasizing modularity, security, and scalability.

- **Frontend / UI:** [Streamlit](https://streamlit.io/) (Provides a responsive, chat-based Enterprise Dashboard)
- **API Gateway:** [FastAPI](https://fastapi.tiangolo.com/) (Exposes a headless REST API with auto-generated Swagger UI interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs))
- **Orchestration Engine:** [LangGraph](https://python.langchain.com/docs/langgraph/) (Handles stateful multi-agent workflows and Tool Calling cycles)
- **LLM Foundation:** [Google Gemini 2.5 Flash](https://ai.google.dev/) (Chosen for its extreme speed and state-of-the-art native tool-calling capabilities)
- **Data Source:** [HubSpot REST API](https://developers.hubspot.com/) (Live CRM backend)

---

## ⚙️ System Workflow Diagram

The following diagram illustrates the lifecycle of a user request within the system:

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as Streamlit Dashboard
    participant Graph as LangGraph Engine
    participant LLM as Gemini 2.5 (Google AI)
    participant API as HubSpot REST API

    User->>UI: "Fetch recent contacts"
    UI->>Graph: Submit State (User Message)
    
    rect rgb(240, 248, 255)
        note right of Graph: Agentic ReAct Loop
        Graph->>LLM: Analyze intent & available tools
        LLM-->>Graph: Decision: Call `fetch_hubspot_contacts`
        Graph->>API: Execute authenticated HTTP GET
        API-->>Graph: Return JSON (Contact records)
        Graph->>LLM: Provide raw JSON context
        LLM-->>Graph: Synthesize human-readable response
    end
    
    Graph-->>UI: Return Final State
    UI->>User: Render polished response
```

## 🔐 Enterprise-Grade Design Decisions

1. **Principle of Least Privilege (PoLP):** 
   The AI Agent is strictly sandboxed. The HubSpot Private App token is scoped **exclusively** to `crm.objects.contacts.read` and `crm.objects.deals.read`. The agent physically cannot modify or delete CRM data, completely eliminating the risk of rogue AI data destruction.
2. **Stateful Graph Execution:** 
   Instead of a simple sequential chain, the system utilizes LangGraph's state machine. This allows for complex "ReAct" (Reasoning + Acting) loops, where the LLM can decide to call multiple tools sequentially or handle API errors autonomously before responding to the user.
3. **Model Agnosticism:** 
   The LLM instantiation is abstracted via LangChain. Swapping between Gemini, Anthropic (Claude), or OpenAI-compatible models (like MiniMax) requires modifying only a single line of code and the corresponding environment variable, ensuring zero vendor lock-in.

---

## 🛠 Developer Guide: How to Extend

This project is built as an **Extensible Integration Hub**. It is designed to be easily expanded with new enterprise systems (e.g., Jira, ERPs, custom internal APIs) using a Plug-and-Play architecture.

If you need to develop or extend this project, here are the key files and directories you should focus on:

### 1. The Plugin Directory (`agent/plugins/`)
This is where all external system integrations live. Each system gets its own dedicated Python file.
- `hubspot.py`: Contains the logic for fetching data from HubSpot CRM.
- `salesforce.py`: A mock implementation demonstrating how to connect to Salesforce.
**To add a new integration:** Create a new file here (e.g., `jira.py`), write your Python function using the `@tool` decorator, and implement your API logic with `try-except` enterprise error handling.

### 2. The Plugin Registry (`agent/plugins/registry.py`)
This file acts as the central switchboard.
Once you create a new plugin, you MUST import it here and add it to the `ALL_TOOLS` list. The LangGraph engine will automatically pick it up and expose it to the LLM.

### 3. The Orchestration Brain (`agent/engine.py`)
This is the core LangGraph state machine. 
If you add a new integration, you should update the `system_prompt` in this file to provide the LLM with **Semantic Routing Rules** (e.g., "If the user asks about tickets, use the Jira tool").

### 4. The Environment Template (`.env.example`)
Always document required API keys, client secrets, and base URLs for your new plugins here to maintain configuration standardization.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- A Google AI Studio API Key (`AQ...`)
- A HubSpot Legacy Private App Access Token (`pat-...`)

### Installation
1. Clone the repository and navigate to the root directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the environment template and configure your keys:
   ```bash
   cp .env.example .env
   # Edit .env to add:
   # - GOOGLE_API_KEY (supports multiple vertical keys for load balancing, e.g. GOOGLE_API_KEY_2, GOOGLE_API_KEY_3)
   # - HUBSPOT_ACCESS_TOKEN (for CRM integration)
   # - MINIMAX_API_KEY (for fallback failover routing)
   # - LANGCHAIN_API_KEY (for LangSmith observability dashboard)
   ```

### 🔍 Monitoring & Observability (LangSmith)
To enable real-time execution tracing, cost analysis, and prompt debugging, configure the LangSmith integration in your `.env` file:
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://eu.api.smith.langchain.com # Use 'https://api.smith.langchain.com' for US region
LANGCHAIN_API_KEY=lsv2_pt_xxxxxx
LANGCHAIN_PROJECT=E2E-Agent-Demo
```
*Once configured, every agent run will silently and asynchronously stream its execution graph steps directly to your LangSmith web console.*

### Execution
This architecture supports a dual-mode execution. You can run the interactive UI for demonstrations, and the headless API for external integrations simultaneously.

**1. Run the Enterprise UI (Streamlit):**
```bash
streamlit run streamlit_app.py
```
*The Enterprise Dashboard will be accessible at `http://localhost:8501`.*

**2. Run the Headless API Gateway (FastAPI):**
Open a second terminal and run:
```bash
uvicorn api.main:app --reload --port 8000
```
*The API Swagger Documentation will be accessible at [http://localhost:8000/docs](http://localhost:8000/docs).*

---

## 📡 Enterprise Agent Topologies & Invocation Paths

In commercial deployments, an Enterprise Integration Hub goes beyond a chat box. The core engine is decoupled to support multiple operational topologies:

```mermaid
graph TD
    A[Enterprise Integration Hub] --> B[1. Interactive Chat / ChatOps]
    A --> C[2. Headless API Gateway]
    A --> D[3. Scheduled Background Worker]
    A --> E[4. Event-Driven Reactive Agent]
    
    B --> B1[Slack/Teams Bot, Web Dashboard]
    C --> C1[REST API, Webhook endpoints for CRM/ERP]
    D --> D1[Cron jobs: Nightly sync, Daily reports]
    E --> E1[Triggered by CRM Webhook when lead status updates]
```

1. **Interactive Chat UI / ChatOps (Employee Assistance)**: Embedded widgets in corporate dashboards or Chat bots (Slack, Microsoft Teams) for manual, ad-hoc inquiry and updates.
2. **Headless API Gateway (System Ingestion)**: Accessing the agent programmatically via FastAPI REST API. Ideal for wrapping AI capabilities inside existing customer portals.
3. **Scheduled Background Worker (Autonomous Auditing)**: Chronologically triggered agents (Cron) that wake up at night to crunch data, compile summaries, and email insights without human intervention.
4. **Event-Driven Reactive Agent (Instant Action)**: Triggered by third-party system Webhooks (e.g., Salesforce lead creation) to instantly research the prospect, draft a proposal, and place it in the rep's draft folder.

---

## 🚀 Enterprise Roadmap & Scaling Strategy

This MVP serves as the foundational block. The roadmap scales the architecture from local prototyping to full-fledged production operation:

### 🏁 Phase 1: Local Single-Tenant MVP (Current State)
* **Topology**: Single-Agent structure, using `streamlit_app.py` for visual proof-of-concept.
* **Integrations**: HubSpot Live API and Salesforce Mock API.
* **Resilience**: Basic Key Rotation (Round Robin) and fallback routing (Gemini ➔ MiniMax).

### 🏃 Phase 2: Multi-Agent Crew & ChatOps Integration
* **Topology**: Multi-Agent supervisor network (e.g., separating CRM Specialists, Financial Analyst, and Communications Agent).
* **Integrations**: Replace Salesforce Mock with active API, add Sweden-specific ERP integration (e.g., **Fortnox**), and embed vector store RAG (e.g., **Confluence / SharePoint**).
* **Channel**: Slack and MS Teams Bot integration for true ChatOps workflow.

### 🏆 Phase 3: Production Scale & Event-Driven Automation
* **Topology**: Decoupled asynchronous workers using message queues (**RabbitMQ / Kafka**) for high-concurrency request scheduling.
* **Integrations**: Fully active Webhook and Cron scheduling for background automation.
* **Governance**: Setup **LangSmith / Langfuse** for LLM observability (trace monitoring, cost tracking) and integrate Enterprise Single Sign-On (SSO / SAML).
