---
name: capture-web
description: Capture one public web page as clean Markdown in the Obsidian Inbox with source metadata, then hand it to digest. Use when the user provides a webpage URL and asks to clip, capture, save, import, or digest it into the vault.
---

# Capture Web

将一个公开网页可靠地转换为 Inbox 剪藏。本技能只负责“捕获”，不替代 `digest` 的价值判断和知识提炼。

## 边界

- 一次只处理一个 `http` / `https` URL。
- URL 以 `.md` 结尾时不使用 Defuddle；直接读取原始 Markdown，并另行确认保存方式。
- 不绕过登录、付费墙、验证码或访问控制。
- 不接受带账号密码的 URL、localhost 或私有网络地址。
- 不下载网页图片，不伪造作者、发布日期或缺失元数据。
- 默认只预览；写入前必须得到用户确认，脚本也必须显式传入 `--write`。
- 不覆盖同名文件。公开仓库不保存未经授权的完整受版权保护文章。

## 工作流

1. 确认 URL 和用户确实希望保存到当前 Vault。
2. 检查 `defuddle` 命令是否可用；不可用时报告安装缺口，不假装已经抓取。
3. 运行预览：

   ```text
   python .agents/skills/capture-web/scripts/capture_web.py --vault . --url "https://example.com/article"
   ```

4. 展示提取到的标题、目标路径和正文预览，说明只保存来源元数据与清理后的 Markdown。
5. 用户确认后执行写入：

   ```text
   python .agents/skills/capture-web/scripts/capture_web.py --vault . --url "https://example.com/article" --write
   ```

6. 报告生成的精确路径，并建议对该文件运行 `digest`。

## 输出契约

目标目录固定为 `04_References/01_Inbox/`。Frontmatter 至少包含：

```yaml
type: reference
source_kind: web
source: "https://example.com/article"
clipped: "YYYY-MM-DD"
extraction_tool: defuddle
tags: []
```

处理状态由文件所在目录表达，不额外写 `status`。正文保留提取标题、原始链接和 Defuddle 返回的干净 Markdown。捕获完成不代表内容已经可信、值得保留或适合建卡；这些判断交给 `digest`。
