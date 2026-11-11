// 배포 버전의 '수정 제안'을 GitHub Issue로 등록해요.
// Vercel 환경변수: GITHUB_TOKEN (Issues 읽기·쓰기), GITHUB_REPO (계정명/저장소명)
module.exports = async (req, res) => {
  if (req.method !== "POST") { res.status(405).json({ error: "method_not_allowed" }); return; }
  let b = req.body || {};
  if (typeof b === "string") { try { b = JSON.parse(b); } catch (e) { b = {}; } }
  const s = (v, n) => String(v == null ? "" : v).replace(/\r/g, "").trim().slice(0, n);
  if (s(b.website, 10)) { res.status(200).json({ ok: true }); return; } // 스팸 방지용 숨은 칸
  const team = s(b.team, 60), name = s(b.name, 40), text = s(b.text, 3000), ref = s(b.ref, 500);
  const item = s(b.item, 80), title = s(b.title, 120), path = s(b.path, 200), url = s(b.url, 300);
  const kind = b.kind === "add" ? "추가할 내용" : "잘못된 내용";
  if (!team || !name || !text) { res.status(400).json({ error: "required" }); return; }
  const repo = process.env.GITHUB_REPO, token = process.env.GITHUB_TOKEN;
  if (!repo || !token) { res.status(500).json({ error: "not_configured" }); return; }
  const body = [
    `**항목**: ${path || item}${url ? ` ([바로가기](${url}))` : ""}`,
    `**유형**: ${kind}`,
    `**제안자**: ${team} ${name}`,
    "",
    text,
    ref ? `\n**참고**: ${ref}` : ""
  ].join("\n");
  try {
    const r = await fetch(`https://api.github.com/repos/${repo}/issues`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "btv-pyeonseong-guide", "Content-Type": "application/json" },
      body: JSON.stringify({ title: `[수정 제안] ${title || item} — ${kind} (${team} ${name})`, body })
    });
    if (!r.ok) { res.status(502).json({ error: "github", status: r.status }); return; }
    const j = await r.json();
    res.status(200).json({ ok: true, number: j.number });
  } catch (e) { res.status(502).json({ error: "network" }); }
};
