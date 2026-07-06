# learningWarehouse-public

从 [learning-warehouse](../) 主仓库按白名单同步可公开内容，并通过 GitHub Pages 在线预览。

## 快速开始

```bash
cd learningWarehouse-public
python tools/sync.py
git add site/ publish.config.yaml
git commit -m "sync: update public content"
git push origin master
```

Windows 也可双击 `tools/sync.bat`。

## 配置

编辑 [`publish.config.yaml`](publish.config.yaml) 添加或修改要公开的条目。

### source 写法

| 写法 | 示例 | 说明 |
|------|------|------|
| `@别名` | `@ai_basics_html` | **推荐**。别名定义在主仓库 [`publish.aliases.yaml`](../publish.aliases.yaml)，父项目改路径时只改别名文件 |
| 相对路径 | `问题积累/xxx.md` | 相对 `source_root`（默认 `..` 即主仓库根目录） |
| glob（批量） | `**/solution.html`（省略 target） | 匹配多个文件，target 自动取源文件所在目录 |
| 绝对路径 | `D:/yld/projects/learning-warehouse/...` | 可用但不推荐，换机器会失效 |

`publish.config.yaml` 示例：

```yaml
source_root: ..
aliases_file: publish.aliases.yaml

entries:
  - source: "@ai_basics_html"
    target: "AI Agent相关/AI基础认知/AI 基础认知"
    mode: html
```

主仓库 [`publish.aliases.yaml`](../publish.aliases.yaml) 示例：

```yaml
ai_basics_html: "AI Agent相关/AI基础认知/solution.html"
```

| mode | 行为 |
|------|------|
| `html` | 源 HTML → `target/index.html` |
| `image` | 原样复制到 target 路径 |
| `markdown` | 复制 `.md` 并生成 Markdown 预览页 |
| `copy` | 原样复制任意静态文件 |

## 在线访问

推送 `master` 后，GitHub Actions 自动部署 GitHub Pages：

https://carrieryu.github.io/learningWarehouse-public/

首次使用前请在 GitHub 仓库 Settings → Pages 中将 Source 设为 **GitHub Actions**。
