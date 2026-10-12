/*
 * ReachTerminal 静态演示适配层（只用于 GitHub Pages 演示）
 *
 * - 读取类接口：返回 data.js 中录制的真实后端响应。录制方式：v0.1.0 后端 +
 *   独立临时 PostgreSQL + examples/demo.json 合成数据，分析日期 2026-10-09。
 * - /api/dcf 与 /api/stress：按 backend/core.hpp 中 dcf()、stress() 的公式在浏览器里计算，
 *   校验条件与后端一致。
 * - 写入类接口（导入、笔记、估值保存、SEC 获取、导出）：返回只读提示。
 */
(() => {
  const REC = window.RT_DEMO || {};
  const READ_ONLY = "在线演示为只读：导入、保存和联网获取请在本地运行完整版本（./scripts/dev.sh）。";
  const json = (status, body) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
  const fail = msg => json(400, { error: msg });
  const CUR = /^[A-Z]{3}$/;

  function dcf(v) {
    const num = k => { if (typeof v[k] !== "number") throw new Error("Required number: " + k); if (!Number.isFinite(v[k])) throw new Error("Nonfinite input"); return v[k]; };
    let f = num("fcff"); const growth = num("growth"), wacc = num("wacc"), terminal = num("terminal_growth"), debt = num("net_debt"), shares = num("shares");
    if (!Number.isInteger(v.years)) throw new Error("Integer years required");
    const years = v.years;
    if (!(f > 0 && f <= 1e15 && shares > 0 && shares <= 1e15 && Math.abs(debt) <= 1e15 && years >= 1 && years <= 20 && growth > -.95 && growth <= 1 && wacc > 0 && wacc <= 1 && terminal > -.5 && terminal < wacc))
      throw new Error("Invalid DCF assumptions; require positive FCFF/shares and WACC > terminal growth");
    if ((v.sector || "") === "Financials") throw new Error("Industrial FCFF DCF not applicable to Financials");
    if (typeof v.currency !== "string" || !CUR.test(v.currency)) throw new Error("Invalid currency");
    let pv = 0; const projections = [];
    for (let n = 1; n <= years; n++) { f *= 1 + growth; const p = f / Math.pow(1 + wacc, n); pv += p; projections.push({ year: n, fcff: f, present_value: p }); }
    const tv = f * (1 + terminal) / (wacc - terminal) / Math.pow(1 + wacc, years), equity = pv + tv - debt;
    if (!Number.isFinite(equity / shares) || !Number.isFinite(tv) || !Number.isFinite(pv)) throw new Error("DCF numerical overflow");
    return { enterprise_value: pv + tv, equity_value: equity, per_share: equity / shares, terminal_share: tv / (pv + tv), currency: v.currency, projections,
      model: "User-supplied unlevered FCFF; operating cash flow minus capex is not automatically FCFF", assumptions: v };
  }
  function stress(p, input) {
    if (p.complete !== true) throw new Error("Cannot stress incomplete portfolio");
    const shock = input.equity_shock ?? -.1, fxshock = input.fx_shock ?? -.05;
    if (!(Number.isFinite(shock) && Number.isFinite(fxshock) && shock >= -1 && shock <= 1 && fxshock >= -1 && fxshock <= 1)) throw new Error("Shock out of range");
    let loss = 0; const rows = [];
    for (const r of p.positions) { if (r.quantity === 0) continue; const f = r.currency === "USD" ? 0 : fxshock, delta = r.market_value_base * ((1 + shock) * (1 + f) - 1); loss += delta; rows.push({ instrument: r.instrument, strategy: r.strategy, change: delta }); }
    for (const c of p.cash) if (c.currency !== "USD") loss += c.base_value * fxshock;
    return { pnl: loss, nav_after: p.nav + loss, positions: rows, equity_shock: shock, fx_shock: fxshock, margin_estimate: null, model: p.scenario_model };
  }

  const realFetch = window.fetch.bind(window);
  window.fetch = async (input, opts = {}) => {
    const url = new URL(typeof input === "string" ? input : input.url, location.href);
    if (!url.pathname.includes("/api/")) return realFetch(input, opts);
    const path = "/api/" + url.pathname.split("/api/")[1], method = (opts.method || "GET").toUpperCase();
    await new Promise(r => setTimeout(r, 60));
    try {
      if (method === "GET") {
        if (path === "/api/research") { const key = "/api/research?instrument=" + url.searchParams.get("instrument"); return REC[key] ? json(200, REC[key]) : fail("Unknown instrument"); }
        if (path === "/api/export") return fail(READ_ONLY);
        if (path === "/api/health") return json(200, { ok: true, database: "Recorded demo", trading_enabled: false });
        return REC[path] ? json(200, REC[path]) : json(404, { error: "Not found" });
      }
      const body = opts.body ? JSON.parse(opts.body) : {};
      if (path === "/api/dcf") return json(200, dcf(body));
      if (path === "/api/stress") return json(200, stress(REC["/api/portfolio"], body));
      return fail(READ_ONLY);
    } catch (e) { return fail(e.message || String(e)); }
  };
})();
