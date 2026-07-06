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

编辑 [`publish.config.yaml`](publish.config.yaml) 添加或修改要公开的条目：

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
