# AI 组件指纹库索引（A.I.G / 腾讯朱雀实验室）

> 数据来源：[tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard) `data/fingerprints/`（MIT License，作者：腾讯朱雀实验室）
> 条目数：168 个组件指纹 ｜ 用途：识别暴露在外的 AI 基础设施组件与版本

## 何时使用

对已发现的服务端口做指纹识别时，若响应特征涉及 LLM/AI 组件（见下方清单），
或目标资产清单里出现 AI 平台/推理框架/向量库/MCP 网关，加载本目录。

**这是规则数据，不是可执行引擎。** Agent 读规则后自行用 `curl`（Kali 原生）按规则里的
`method` + `path` 发请求，用 `matchers` 判断命中，再按 `version.extractor` 的正则提取版本。
不要引入任何外部扫描器。

## 数据格式

```yaml
info:
  name: ollama                 # 组件标识
  severity: info
  desc: 组件说明
http:
  - method: GET
    path: '/'                  # 探测路径
    matchers:                  # 匹配表达式（DSL：&& || !，body=/header=/icon=）
      - body="Ollama is running"
version:
  - method: GET
    path: '/api/version'       # 版本提取路径
    extractor:
      part: body               # body | header
      regex: '{"version":"(\d+\.\d+\.?\d+?)"}'
```

## 工作流

1. 按端口/路径特征从下方清单定位候选组件，读对应 `<name>.yaml`。
2. 用 `curl -s -i <target><path>` 请求，对响应体/头做 `matchers` 判定。
3. 命中后按 `version` 规则提取版本号。
4. 把 `组件 + 版本` 交给 `cve-triage`（其 `data/aig-vuln/` 为同源 CVE 库）。

## 组件清单（按类别）

**本地推理 / 模型服务**：ollama、vllm、llama-cpp、sglang、triton-inference-server、tensorrt-llm、lmdeploy、xinference、localai、text-generation-webui、koboldcpp、tabbyapi、powerinfer、mlc-llm、deepspeed-mii、huggingface-tgi、aphrodite-engine、gpt4all、lollms、lightllm、llmstudio、bentoml、baseten-truss、fireworks-ai、nvidia-nim、modal、replicate、together-ai、databricks-model-serving、vertex-ai、aws-bedrock、azure-openai、groq、dynamo

**LLM 应用 / 平台**：dify、fastgpt、flowise、langflow、ragflow、anythingllm、openwebui、lobechat、nextchat、librechat、chatgpt-web、h2ogpt、privategpt、quivr、kotaemon 类、maxkb、weknora、blinko、onyx、lollms-webui、chuanhugpt、betterchatgpt、huggingface-chat-ui、ai-chatbot、marimo、sillytavern

**Agent / 编排框架**：autogen-studio、AutoGPT、crewai、superagi、devika、praisonai、langchain、langserve、langroid、langfuse、graphiti、cognee、mem0、memos、LightRAG、Suna、Omnigent、agentic-flow、upsonic、OpenClaw、junoclaw、Flyto2 Core

**网关 / 代理**：LiteLLM、new-api、portkey-ai-gateway、envoy-ai-gateway、cloudflare-ai-gateway、helicone、bifrost、9router、sub2api、omniroute、kong-proxy

**向量库 / 数据层**：chroma、qdrant、milvus、weaviate、feast、clickhouse、dask、ray、hatchet、trigger.dev、tensorzero

**MCP 相关**：mcp、mcp sse、MCPHub、mcp-atlassian、mcp-documentation-server、mcp-searxng、meta-ads-mcp、n8n-mcp、netlicensing-mcp、NotebookLM MCP、mcp-server-kubernetes（见 cve-triage 库）

**训练 / 微调 / 标注**：axolotl、llamafactory、ms-swift、instructlab、feast、kubeflow、kubeai、Eclipse Theia、openhoudini

**Notebook / 开发环境**：jupyterlab、jupyter-notebook、jupyter-server、ray、kubeflow、mlflow

**语音 / 多模态**：f5-tts、gpt-sovits、ChatRTX、comfyui（含 ComfyUI-* 节点包）、ComfyUI-Manager、ComfyUI-Impact-Pack、ComfyUI-Custom-Scripts、comfy_mtb、ComfyUI-Prompt-Preview、ComfyUI-Ace-Nodes、ComfyUI-Bmad-Nodes、pipecat

**工作流 / 自动化**：n8n、clickhouse、nocobase、DBHub、Crawl4AI、Context7、netlicensing、Open GenAI Stack、KubePi

> 完整逐条清单直接 `ls` 本目录；文件名即 `<组件>.yaml`。子目录 `comfyui/` 下为其节点包指纹。

## 注意事项

- **指纹命中只证明“组件暴露”，不等于存在漏洞。** 版本提取失败时不得推断 CVE 适用性。
- 未认证即可访问的管理端点/模型接口，若可由非可信网络访问，风险显著更高——结合 RoE 判定是否在 scope。
- 对 localhost / 个人开发目标，除证据显示公网可达外，不要表述为“公网暴露”。
