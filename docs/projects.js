/*
 * ZeroMatrixTech 项目清单 —— 导航页的唯一数据来源。
 * 新增或更新项目只需修改这个文件，index.html 会自动渲染。
 *
 * 字段说明
 *   id        唯一标识（英文、小写）
 *   name      项目名称
 *   zh / en   一句话简介（中文 / 英文）
 *   category  protocol 协议与研究 | app 应用 | system 系统与环境 | creative 创意实验
 *   status    { label: 显示文字, tone: research | alpha | rc | stable | exp }
 *   tags      技术标签
 *   license   许可证
 *   repo      公开仓库地址；仓库未公开时填 null，并写 repoNote
 *   links     其他链接 { label, href, kind: "demo" | "doc" | "release", desc? }
 *             kind 为 demo 的链接会出现在导航页的“在线演示”区，desc 是演示说明
 *   image     卡片配图（相对 docs/ 的路径）；没有时用 art 指定的内置示意图
 *   art       terminal | curves —— 无配图时的内置示意
 *   note      卡片底部的补充说明（可选）
 */
window.ZMT_CATEGORIES = {
  protocol: "协议与研究",
  app: "应用",
  system: "系统与环境",
  creative: "创意实验",
};

window.ZMT_PROJECTS = [
  {
    id: "aclt",
    name: "ACLt Protocol",
    zh: "面向异构、无许可分布式计算的开放协议：任务先承诺后执行，结果靠抽样证据验证，风险有硬上限。",
    en: "An open, implementation-neutral protocol for heterogeneous, permissionless distributed computing.",
    category: "protocol",
    status: { label: "G0 · 协议规格化", tone: "research" },
    tags: ["协议规格", "Rust", "RIR", "验证模型"],
    license: "Apache-2.0",
    repo: null,
    repoNote: "仓库暂未公开",
    links: [{ label: "像素动画导览", href: "demos/aclt-theater.html", kind: "demo", desc: "跟着 Claude 跑一圈像素世界，看一个计算任务怎样从约定走到结算。约 2 分 30 秒，有配乐。" }],
    image: "assets/aclt-theater.png",
    imageAlt: "ACLt 像素动画开场画面",
  },
  {
    id: "reachterminal",
    name: "ReachTerminal",
    zh: "开源、自托管的投资研究终端：基本面研究、估值、风险与数据溯源放在同一个本地工作区，不含下单代码。",
    en: "Self-hosted investment research terminal. Browser UI, C++20 backend, PostgreSQL. No broker order submission.",
    category: "app",
    status: { label: "v0.1.0 alpha", tone: "alpha" },
    tags: ["C++20", "PostgreSQL", "Web 前端"],
    license: "MIT",
    repo: "https://github.com/ZeroMatrixTech/ReachTerminal",
    links: [
      { label: "在线演示", href: "demos/reachterminal/index.html", kind: "demo", desc: "真实前端 + 录制的 v0.1.0 后端响应，合成数据，只读。组合、研究、估值和压力测试都能点。" },
      { label: "架构", href: "https://github.com/ZeroMatrixTech/ReachTerminal/blob/main/docs/architecture.md", kind: "doc" },
      { label: "路线图", href: "https://github.com/ZeroMatrixTech/ReachTerminal/blob/main/docs/roadmap.md", kind: "doc" },
    ],
    image: "assets/reachterminal.png",
    imageAlt: "ReachTerminal 组合总览界面（合成演示数据）",
    note: "截图使用合成演示数据。",
  },
  {
    id: "ubuntu-zeromatrix",
    name: "ubuntu_ZeroMatrix",
    zh: "基于 Ubuntu 26.04.1 LTS 的开发系统镜像，提供虚拟机与实体机两条安装基线，预置 C++ / Python / Rust 工具链与 VS Code 工作区。",
    en: "Ubuntu 26.04.1 LTS development system with VM and physical install profiles and preconfigured toolchains.",
    category: "system",
    status: { label: "0.2.0-rc3 · 验收中", tone: "rc" },
    tags: ["Ubuntu", "ISO", "Make", "VS Code"],
    license: "Apache-2.0",
    repo: "https://github.com/ZeroMatrixTech/ubuntu_ZeroMatrix",
    links: [
      { label: "安装演示", href: "demos/ubuntu-zeromatrix/index.html", kind: "demo", desc: "模拟构建镜像、在启动菜单里改参数、安装和首次登录的完整流程。" },
      { label: "构建与安装", href: "https://github.com/ZeroMatrixTech/ubuntu_ZeroMatrix/blob/main/docs/build-and-install.md", kind: "doc" },
    ],
    art: "terminal",
    terminal: ["git lfs pull", "make iso-vm", "make iso-physical", "make verify-iso"],
  },
  {
    id: "mathpicasso",
    name: "MathPicasso",
    zh: "用数学函数画画：把图形作品转写为 MATLAB 数值曲线，保留颜色、定义域和隐藏状态。",
    en: "Drawing with mathematical functions, rendered as numeric curves in MATLAB.",
    category: "creative",
    status: { label: "示例作品", tone: "exp" },
    tags: ["MATLAB", "函数绘图"],
    license: "MIT（仅代码）",
    repo: "https://github.com/ZeroMatrixTech/MathPicasso",
    links: [
      { label: "函数画板", href: "demos/mathpicasso/index.html", kind: "demo", desc: "27 条公式画出一幅《灯塔与海》，可以逐条绘制、切换墨线，也能输入自己的公式。" },
      { label: "公式对照", href: "https://github.com/ZeroMatrixTech/MathPicasso/blob/main/docs/formulas.md", kind: "doc" },
    ],
    image: "assets/mathpicasso.png",
    imageAlt: "函数画板中的《灯塔与海》：由函数曲线组成的山、海、灯塔和帆船",
    note: "仓库里的 Osage 示例改编自第三方作品，授权尚未确认，这里不展示；配图是函数画板的原创示例。",
  },
];
