# HubSpot Private App - 权限与能力追踪 (Scope & Capabilities Tracker)

> **💡 文档定位**
> 本文档用于记录当前 E2EAgentAI 项目中，HubSpot Private App (Access Token) 所拥有的实际权限（Scopes）。
> 只有在此文档中标记为 `[x]` 激活的权限，AI Agent 才能在 LangGraph 的 Tool 节点中被允许开发和调用。

## 1. 核心 CRM 基础对象权限

- [x] `crm.objects.contacts.read` (允许 Agent 读取客户/联系人信息)
- [ ] `crm.objects.contacts.write` (允许 Agent 创建或更新联系人)
- [x] `crm.objects.deals.read` (允许 Agent 读取销售机会/交易数据)
- [ ] `crm.objects.deals.write` (允许 Agent 创建或推进销售机会)
- [x] `crm.objects.companies.read` (允许 Agent 读取公司数据)

## 2. 其他可能的关联权限 (请根据你的实际勾选进行更新)

- [ ] `crm.objects.tickets.read` (读取客服工单)
- [x] `crm.objects.custom.read` (读取自定义字段和对象结构)
- [x] `crm.lists.read`
- [x] `crm.objects.appointments.read`
- [x] `crm.objects.contracts.read`
- [x] `crm.objects.courses.read`
- [x] `crm.schemas.contacts.read`

---

## 3. 🔑 如何获取 Access Token (Token Retrieval Guide)

为了让 Agent 能够使用上述权限，你需要将 Private App 的 Access Token 传递给代码环境。

**获取步骤（基于当前最新 UI）：**
1. 在创建完 Private App 后，你会进入该 App 的详情页面。
2. 在 `Overview` 旁边的标签页中，点击 **`Auth`** 标签。
3. 在 `Auth` 页面中，你会看到一行写着 **Access Token**。
4. 点击 **`Show Token`**（显示令牌），然后点击 **`Copy`**（复制）。
5. 将这串以 `pat-` 开头的代码粘贴到项目根目录的 `.env` 文件中：
   ```env
   HUBSPOT_ACCESS_TOKEN=pat-na1-xxxxxx...
   ```

**⚠️ 绝对安全警告：** 无论出于何种测试目的，**永远不要**把这个 Token 粘贴在截图中发给别人（包括我），也绝对不要把它直接写在 `.py` 等代码文件中提交到 Git！只能放在本地的 `.env` 里！
