# 🎯 PRD (Product Requirements Document) - [Project Name]

> **💡 Antigravity PRD 定位声明**
> 这是一个基于 AI 驱动开发 (Agentic Coding) 的动态 PRD。它的核心任务是确立“人机分工框架”，清晰定义业务状态与用户故事，作为所有代码生成的最初代“单一事实来源 (Single Source of Truth)”。

---

## 1. 🌌 项目愿景 (Project Vibe & Vision)

- **核心目标**: 在 24 小时内打造一个真正的企业级 E2E (End-to-End) Agent 演示 MVP。核心打通 "HubSpot 数据层 -> LangGraph Agent -> Streamlit 可视化" 的完整链路。
- **情绪基调 (Vibe)**: 务实、极速交付、企业级、数据驱动 (Data-driven)、技术硬核。
- **核心用户画像**: 需要快速验证 AI Agent 在企业真实数据环境（如 CRM 销售流水线）中流转能力的架构师及 B 端产品经理。

## 2. 🎭 人机分工与协作边界 (Human-AI Division of Labor)

- **人类强制主导 (Human Override)**:
  - HubSpot CRM 的注册、Private App 创建以及 Access Token 凭证的管理。
  - 业务场景范围的硬性裁剪（坚守“先打通单链路，再做加分项”的原则）。
- **AI 自主飞地 (AI Autonomous Zone)**:
  - LangGraph 框架与 HubSpot REST API Tool 的代码骨架生成及节点编排。
  - Streamlit Dashboard 的图表渲染及交互设计。
  - 销售场景预设 Prompt（如“帮我查一下最近新增的客户”）的撰写与调优。

## 3. 📖 核心用户故事 (User Stories)

### P0 (Must Have - 核心通路)
- [ ] **US-01**: 作为系统演示者，我希望 Agent 能够通过 MCP 协议自动查询 Salesforce Dev Org 中的销售数据，以便证明 Agent 具备真实的企服数据接驳能力。
- [ ] **US-02**: 作为终端销售主管，我希望在 Streamlit Dashboard 上通过自然语言交互（如“生成本周Pipeline健康报表”），以便直接查看基于实时 CRM 数据生成的图表。

### P1 (Should Have - 体验提升 / 加分项)
- [ ] **US-03**: 作为市场人员，我希望 Agent 能够通过 REST API 获取 HubSpot Free CRM 的数据，以便进行跨系统的销售/市场数据对比。
- [ ] **US-04**: 作为企业员工，我希望能够查询基于 Chroma 构建的简易 PDF 知识库，以便快速获取企业内部政策或产品文档。

## 4. ⚙️ 功能细节与业务状态 (Core Requirements & States)

- **系统链路状态机**:
  - `MCP_Connecting` -> `Data_Fetched` -> `Agent_Reasoning` -> `Dashboard_Rendered`
- **边缘用例控制 (Edge Cases)**:
  - 当 Salesforce DX MCP Server 未启动或连接超时时，Streamlit 界面需优雅降级，提示用户检查本地 CLI 服务状态。
  - 复杂查询导致 Agent 思考超时，需提供明确的 loading 状态与思考日志透出。

## 5. 验收准则 (Acceptance Criteria / DoD)

- [ ] 成功在本地跑通 `describe_sobject` 或自定义 SOQL 查询的 MCP 链路。
- [ ] LangGraph 成功通过 MCP 适配器获取数据并给出合乎逻辑的 JSON/结构化报表数据。
- [ ] Streamlit 成功接收 Agent 输出并渲染为直观的业务图表（如 Pipeline 漏斗图或柱状图）。
- [ ] 整体主链路（Salesforce -> Agent -> Streamlit）联调通过，可录制完整的 Live Demo 视频。

## 6. 🚀 延展规划库 (Roadmap & Backlog)

- [ ] [Idea]: 接入 HubSpot CRM (REST API) 作为多数据源演示。
- [ ] [Idea]: 接入本地 Chroma 向量库，提供 PDF 企业知识库的 RAG 能力。
- [ ] [Tech Debt]: 将 Streamlit 表现层替换为 Next.js 生产级 Dashboard。
