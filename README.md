# ZeroMatrixTech · 组织主页与官网

本仓库维护 ZeroMatrixTech 的 GitHub 组织介绍页和公司官网 <https://zeromatrix.tenneidp.com/>。ZeroMatrixTech 是北京凌矩阵科技有限责任公司的对外技术品牌。

主页内容位于 [profile/README.md](profile/README.md)。根目录 README 用于说明本仓库的用途。主页围绕品牌、公司简介、核心团队、业务与技术方向，以及交流合作组织内容。具体项目的介绍、成熟度和许可证由各自仓库维护。

## 目录

| 路径 | 用途 |
| --- | --- |
| `profile/README.md` | GitHub 组织主页（github.com/ZeroMatrixTech 上显示的内容） |
| `site/content.json` | 官网全部文字与项目数据，中英文成对存放 |
| `site/build.py` | 生成器：把 `content.json` 渲染成 `docs/` 下的中英文页面，只用 Python 标准库 |
| `docs/` | 官网成品，通过 GitHub Pages 发布；`docs/en/` 为英文版 |
| `docs/assets/site.css`、`site.js` | 全站共用的样式与脚本（手写，不由生成器覆盖） |
| `docs/demos/` | 可在浏览器中直接运行的演示页（每个项目一个子目录） |
| `docs/CNAME` | 自定义域名，由 GitHub 维护，不要删除 |

## 修改官网内容

1. 编辑 `site/content.json`。每段文字都写成 `{"zh": "…", "en": "…"}`，两种语言一起改；
2. 运行生成器，它会重写 `docs/` 与 `docs/en/` 下的 5 个页面，以及 `404.html`、`sitemap.xml`、`robots.txt`、`assets/favicon.svg`，最后检查所有站内链接和图片：

   ```sh
   python3 site/build.py
   ```

3. 本地预览：在 `docs/` 下运行 `python3 -m http.server`，打开 <http://127.0.0.1:8000/>；
4. 把 `site/` 和 `docs/` 的变化一起提交。

不要直接改 `docs/*.html`，下次生成会被覆盖。新增项目：在 `projects` 数组里加一项，配图放到 `docs/assets/`，演示放到 `docs/demos/` 并填 `demo` 字段；仓库未公开时 `repo` 填 `null` 并写 `repo_note`，不要放指向私有仓库的链接。同步更新 `profile/README.md` 的项目表。

## 发布

官网通过本仓库的 GitHub Pages 发布：Settings → Pages → Source 选 **Deploy from a branch**，分支 `main`，目录 `/docs`，自定义域名 <https://zeromatrix.tenneidp.com/>（Cloudflare 上的 CNAME 记录保持「仅 DNS」）。旧地址 `zeromatrixtech.github.io/.github/` 会自动跳转到自定义域名。

## 演示的数据来源

| 演示 | 来源 |
| --- | --- |
| `demos/aclt-theater.html` | ACLt 仓库 `docs/00-overview/aclt-theater.html` 的副本，更新时重新复制 |
| `demos/reachterminal/` | ReachTerminal v0.1.0 的真实前端；`data.js` 录制自本地后端加载 `examples/demo.json` 合成数据后的接口响应（分析日期 2026-10-09）；`shim.js` 按后端公式在浏览器中计算 DCF 与压力测试，写入类操作只读 |
| `demos/ubuntu-zeromatrix/` | 按仓库 README、`scripts/build-online.py` 与验收文档编写的流程模拟，不运行真实构建 |
| `demos/mathpicasso/` | 浏览器版函数绘图，示例《灯塔与海》为原创；不包含授权未确认的 Osage 示例 |
