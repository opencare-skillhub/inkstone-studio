# MCP 集成指南

## 1. 选题调研 (Ideation)
当需要寻找热点或调研竞品时，优先使用以下 MCP 工具：
- **Exa Search**: `mcporter call 'exa.web_search_exa(query: "...", numResults: 5)'`
  - 适用场景：寻找特定领域的深度文章、学术资料或近期热点。
- **Jina Reader**: `curl -s "https://r.jina.ai/URL"`
  - 适用场景：已知竞品文章 URL，需要提取纯文本进行分析。
- **Firecrawl**: 若已配置 Firecrawl MCP，可用于批量抓取或结构化提取。

## 2. 发布 (Publishing)
目前 Inkstone 不强制绑定发布渠道，推荐工作流：
1. **格式化**：使用 `rewrite.md` 将长文转为各平台格式。
2. **导出**：定稿存入 `published/` 目录。
3. **微信生态**：若配置了 `youmind-wechat-article` 或 `wechat-studio` 技能，可直接调用其发布/排版指令。
4. **降级方案**：生成 HTML 版本，提示用户手动复制到平台编辑器。

## 3. 优雅降级
如果用户环境未配置相关 MCP，Agent 应：
- 提示用户："当前未检测到 Exa MCP，请提供几个你想分析的竞品 URL，或告诉我你关注的关键词，我用内置搜索尝试。"
- 不要编造搜索结果。
