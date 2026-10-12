# ZeroMatrixTech · GitHub 组织主页

本仓库维护 ZeroMatrixTech 的 GitHub 组织介绍页。ZeroMatrixTech 是北京凌矩阵科技有限责任公司的对外技术品牌。

主页内容位于 [profile/README.md](profile/README.md)。根目录 README 用于说明本仓库的用途。主页围绕品牌、公司简介、核心团队、业务与技术方向，以及交流合作组织内容。具体项目的介绍、成熟度和许可证由各自仓库维护。

## 目录

| 路径 | 用途 |
| --- | --- |
| `profile/README.md` | GitHub 组织主页（github.com/ZeroMatrixTech 上显示的内容） |
| `docs/` | 项目导航与演示站点，纯静态页面，通过 GitHub Pages 发布 |
| `docs/projects.js` | 项目清单，导航页的唯一数据来源 |
| `docs/demos/` | 可在浏览器中直接运行的演示页（每个项目一个子目录） |
| `docs/assets/` | 项目截图与配图 |

## 新增或更新项目

1. 编辑 `docs/projects.js`，按文件顶部的字段说明增加或修改一项；
2. 如有截图，放到 `docs/assets/`，在该项的 `image` 字段填相对路径；
3. 如有可在浏览器运行的演示，放到 `docs/demos/`，在 `links` 中加一条 `kind: "demo"`；
4. 同步更新 `profile/README.md` 的项目表；
5. 本地双击 `docs/index.html` 预览，确认后提交。

仓库未公开的项目，`repo` 填 `null` 并写 `repoNote`，不要放指向私有仓库的链接。

## 发布

导航站通过本仓库的 GitHub Pages 发布：Settings → Pages → Source 选 **Deploy from a branch**，分支 `main`，目录 `/docs`。站点地址为 <https://zeromatrixtech.github.io/.github/>。页面内全部使用相对路径，本地双击 `docs/index.html` 即可预览；ReachTerminal 演示使用 ES module，本地预览需在 `docs/` 下运行 `python3 -m http.server`。

## 演示的数据来源

| 演示 | 来源 |
| --- | --- |
| `demos/aclt-theater.html` | ACLt 仓库 `docs/00-overview/aclt-theater.html` 的副本，更新时重新复制 |
| `demos/reachterminal/` | ReachTerminal v0.1.0 的真实前端；`data.js` 录制自本地后端加载 `examples/demo.json` 合成数据后的接口响应（分析日期 2026-10-09）；`shim.js` 按后端公式在浏览器中计算 DCF 与压力测试，写入类操作只读 |
| `demos/ubuntu-zeromatrix/` | 按仓库 README、`scripts/build-online.py` 与验收文档编写的流程模拟，不运行真实构建 |
| `demos/mathpicasso/` | 浏览器版函数绘图，示例《灯塔与海》为原创；不包含授权未确认的 Osage 示例 |
