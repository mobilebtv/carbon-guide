"""GitHub Issues → 작업본 '수정 제안 목록'(db suggestions/github) 동기화용 데이터 만들기.
사용: python3 sync_issues.py <현재 db 문서 json 또는 -> <출력 json>
"""
import json, re, sys, urllib.request
REPO = "mobilebtv/carbon-guide"
def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "carbon-guide-sync"})
    return json.load(urllib.request.urlopen(req))
issues = []
for page in range(1, 11):
    batch = get(f"https://api.github.com/repos/{REPO}/issues?state=all&per_page=100&page={page}")
    issues += [i for i in batch if "pull_request" not in i]
    if len(batch) < 100: break
cur = {}
if sys.argv[1] != "-":
    try: cur = {x["id"]: x for x in json.load(open(sys.argv[1])).get("items", [])}
    except Exception: cur = {}
items = []
for i in issues:
    t = i.get("title") or ""
    if not t.startswith("[수정 제안]"): continue
    body = i.get("body") or ""
    meta = {}
    m = re.search(r"<!-- meta (\{.*?\}) -->", body, re.S)
    if m:
        try: meta = json.loads(m.group(1))
        except Exception: meta = {}
    if not meta:
        mi = re.search(r"#([\w-]+)\)\)", body); who = re.search(r"\*\*제안자\*\*: (.+)", body)
        meta = {"item": mi.group(1) if mi else "", "team": who.group(1).strip() if who else "", "name": "",
                "kind": "add" if "**유형**: 추가할 내용" in body else "fix"}
        rf = re.search(r"\*\*참고\*\*: (.+)", body); meta["ref"] = rf.group(1).strip() if rf else ""
    lines = body.split("\n")
    try:
        start = next(k for k, l in enumerate(lines) if l.strip() == "" ) + 1
    except StopIteration: start = 0
    text = "\n".join(l for l in lines[start:] if not l.startswith("**참고**") and not l.startswith("<!-- meta")).strip()
    tm = re.match(r"\[수정 제안\] (.+?) — ", t)
    gid = f"gh-{i['number']}"
    st = "done" if i["state"] == "closed" else "new"
    old = cur.get(gid)
    if old and old.get("status") in ("done", "hold") and st == "new": st = old["status"]
    items.append({"id": gid, "at": i["created_at"], "item": meta.get("item", ""), "title": tm.group(1) if tm else t,
                  "kind": meta.get("kind", "fix"), "text": text[:3000], "ref": (meta.get("ref") or "")[:500],
                  "team": meta.get("team", ""), "name": meta.get("name", ""), "status": st,
                  "url": i["html_url"], "num": i["number"], "src": "github"})
json.dump({"items": items, "syncedAt": __import__("datetime").datetime.utcnow().isoformat() + "Z"}, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print(len(items), "items")
