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
| 相对路径 | `AI Agent相关/AI基础认知/solution.html` | 相对 `source_root`（默认 `..` 即主仓库根目录） |
| glob（批量） | `**/solution.html`（省略 target） | 匹配多个文件，target 自动取源文件所在目录 |
| 绝对路径 | `D:/yld/projects/learning-warehouse/...` | 可用但不推荐，换机器会失效 |

```yaml
source_root: ..

entries:
  - source: "AI Agent相关/AI基础认知/solution.html"
    target: "AI Agent相关/AI基础认知/AI 基础认知"
    mode: html

  - source: "**/solution.html"
    mode: html
```

| mode | 行为 |
|------|------|
| `html` | 源 HTML → `target/index.html` |
| `image` | 原样复制到 target 路径 |
| `markdown` | 复制 `.md` 并生成 Markdown 预览页 |
| `copy` | 原样复制任意静态文件 |

## 在线访问

推送 **learningWarehouse-public 子仓库** 的 `master` 后，GitHub Actions 自动部署 GitHub Pages（推主仓库 Gitee/GitHub **不会**触发此 workflow）。

首次使用前请在 GitHub 仓库 **Settings → Pages → Build and deployment → Source** 设为 **GitHub Actions**。

https://carrieryu.github.io/learningWarehouse-public/
