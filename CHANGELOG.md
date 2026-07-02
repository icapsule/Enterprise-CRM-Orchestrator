# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-07-02

### Added
- **Developer Console**: Integrated API Playground (FastAPI Swagger) link directly into the Streamlit UI to prove true headless backend capabilities.
- **LangSmith Tracing UI**: Integrated LangSmith Trace Dashboard one-click access in the Streamlit Sidebar for real-time cognitive observability.
- **IM Integrations Sandbox**: Added UX placeholders for MS Teams, Slack, and Telegram bot delivery pipelines.
- **Agentic Documentation**: Added "Deep Agents" topology to the architectural roadmap for handling extremely long-running asynchronous workflows.

### Changed
- **LangChain Brand UI Redesign**: Fully redesigned the Streamlit dashboard layout using custom injected CSS (Inter font, mint green accents, high-contrast dark slate headers) to perfectly align with LangChain's Enterprise design aesthetic.

## [1.0.0] - 2026-07-01

### Added
- **Agent Core Engine**: Deployed LangGraph-based action-oriented agent (`create_react_agent`) capable of reasoning and multi-step tool execution.
- **Cascading LLM Failover**: Built a zero-downtime router that iterates through `GEMINI_API_KEY_1`, `GEMINI_API_KEY_2`, etc., and automatically drops to `MINIMAX_API_KEY` upon encountering `ResourceExhausted` errors.
- **Plugin Architecture**: Added mock stubs for HubSpot CRM and Salesforce integrations to demonstrate external system mutations.
- **Dual-Interface Delivery**: Bootstrapped both a FastAPI REST backend (`api/main.py`) and a Streamlit frontend (`streamlit_app.py`).

### Fixed
- Stabilized `load_dotenv()` import path to prevent `ValidationError` on cold boots.
- Hardened exception catching across the LLM Fallback chain to ensure non-deterministic API failures do not crash the Agent runtime.
