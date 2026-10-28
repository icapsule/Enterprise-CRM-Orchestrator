# 🏗 PROJECT SPEC (Technical Architecture Specification) - Enterprise CRM Orchestrator

> **💡 Antigravity SPEC 定位声明**
> 这是项目运行期的工程“骨架”与技术“宪法”。它是最高级指令区，专门服务于 AI Agent (如下一代代码生成模型)。它必须极其精确、无废话、强约束，确保历经数百次自动迭代后，系统架构不产生丝毫的熵增。

---

## 1. 🛠 核心技术栈与选型论证 (Tech Stack & Tool Selection Matrix)

- **表现层 (Frontend / UI)**: Streamlit (基于 Python 生态，追求极致的一天内 Dashboard 开发效率)
- **Agent 框架 (Agentic Layer)**: LangGraph + 原生 LangChain Tools
- **数据层 (Data & Knowledge)**: HubSpot CRM (REST API) + Salesforce CRM (Mock / DX MCP)
- **数据集成协议**: 原生 REST API (基于 Private App Access Token) + MCP 标准协议适配

### 选型决策论证矩阵 (Evaluation & Rationale)

| 架构层级 | 选型结果 | 核心选型考量与替代方案对比 (Trade-offs) |
| :--- | :--- | :--- |
| **数据层 (CRM)** | **Salesforce Dev Edition** | 永久免费，自带官方 DX MCP 本地 stdio 支持，预置开箱即用的商机与线索数据。 |
| **数据层 (Marketing)** | **HubSpot Free CRM** | 公开 REST API 规范，轻量直接，通过 Private App 即可快速打通，作为多源对比最佳对照组。 |
| **知识库 (RAG)** | **Chroma (本地向量库)** | 本地轻量化向量数据库，搭配 3-5 份企业 PDF 即可在 1 小时内搭好验证，足够支撑演示场景。 |
| **Agent 状态机** | **LangGraph + MCP** | **为何不用 OpenManus？** 生态尚不成熟，缺乏严格企业级控制力，现场 Demo 极易失控翻车。<br/>**为何不用 Dify？** 低代码拖拽虽快，但缺乏对 Prompt 状态通道、异常重试与双模型级联容灾的代码级自由控制力。<br/>**最终选择 LangGraph**：状态可完全编程，文档与社区成熟，原生适配 ReAct 闭环与 MCP Client。 |
| **交互表现层** | **Streamlit** | Python 生态极速交付首选，单人单日内可构建出具备专业质感的企业级可视化控制台。 |

## 2. 🗺 架构拓扑树 (Architecture Topology)

```text
Enterprise-CRM-Orchestrator/
├── streamlit_app.py   # [表现层入口] Streamlit 渲染与交互主循环
├── agent/             # [Agent逻辑区] 
│   ├── engine.py      # LangGraph 状态图定义与节点编排
│   └── prompts.py     # 核心场景 Prompt 库（如销售报表场景）
├── mcp/               # [协议适配层]
│   └── client.py      # 连接本地 Salesforce DX MCP Server 的客户端封装
├── data/              # [可选数据/知识库] (P1 优先级储备)
│   └── docs/          # 存放用于 RAG 的演示 PDF 文件
└── requirements.txt   # Python 依赖清单 (streamlit, langgraph, mcp, etc.)
```

## 3. 🔌 接口协议与系统边界 (API Contracts & Boundaries)

- **数据通道契约**: 
  - 核心链路：`Streamlit <-> LangGraph <-> MCP Client <-> Salesforce CLI`
  - Agent 与 数据源之间的交互必须且只能通过 MCP Protocol 进行标准化调用（`CallTool` / `ReadResource`）。
- **工具调用规范**:
  - 针对 Salesforce，Agent 将主要调用 `describe_sobject` 或执行 SOQL 相关的 MCP Tools。

## 4. 🗃 系统状态与数据契约 (System States & Schema Types)

- **Agent State (LangGraph)**:
  - 必须维护严格的 `TypedDict`，包含当前用户的对话上下文、MCP 调用返回的原始 CRM 数据、以及供 Streamlit 消费的图表配置项（结构化 JSON）。

## 5. 🛡 架构级安全防御与风险红线 (Security Redlines & Risk Controls)

- **本地服务边界**: Salesforce DX MCP Server 必须通过安全的本地 stdio 通信，禁止随意在公网暴露 HTTP/WebSocket 的 MCP 服务端口。
- **凭证隔离**: 本地执行 Salesforce CLI 所需的 Session / Token 依赖操作系统级 Keychain 或环境变量，禁止在任何代码与 Markdown 文档中硬编码账号密码或静态 Token。
- **防止不可控的 Agent 死循环**: LangGraph 必须设定严格的 `recursion_limit`，防止由于 MCP 调用失败导致的无限重试。
- **托管版本差异预警**: Salesforce 官方托管 Hosted MCP（GA 版）通常要求 Enterprise Edition 及以上级别，开发测试阶段推荐使用本地 DX CLI MCP Server 确保平稳可控。
- **反贪多与范围裁剪原则**: 在企业级 MVP 阶段，坚决反对同时折腾多数据源 + 自建 RAG + 复杂多智能体体系，**砍范围比赶进度更重要**，先保证一条闭环链路 100% 稳定运行。

---

## 6. 🧠 决策轨迹挂载点 (Architecture Thought Log)

- **[2026-06-30] [Decision]**: 使用 Streamlit 替代 Next.js 作为表现层。
  - *Context*: 项目目标为 24 小时内交付可演示的 MVP。
  - *Trade-off*: 牺牲了极致的 Web UI 定制化能力与生产级可扩展性，换取了极速的 Python 全栈打通效率。
- **[2026-06-30] [Decision]**: 使用 LangGraph 替代 OpenManus。
  - *Context*: 需要一个稳定可控、原生支持 MCP 且生态成熟的 Agent 编排框架，以保证企业级 Demo 的现场稳定性。
  - *Trade-off*: 可能需要编写更多样板代码（相对于 Dify 等低代码平台），但获得了完全的代码级控制力。
- **[2026-06-30] [Decision]**: 优先单线突破 (Salesforce)，暂缓 RAG 与多数据源。
  - *Context*: 时间紧迫，砍掉范围比赶进度更重要，必须优先保证一条主流程跑通以用于视频/Live Demo。
