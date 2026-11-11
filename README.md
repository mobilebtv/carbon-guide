# 모바일 B tv 편성 가이드 (배포 버전)

이 저장소는 claude.ai의 작업용 가이드에서 **Publish** 버튼으로 자동 갱신돼요. 파일을 직접 고치지 마세요(다음 Publish 때 덮어써져요).

- `index.html` — 배포 페이지 (전체 Publish 때 갱신)
- `content/*.js` — 탭별 내용 (탭 Publish 때 해당 탭만 갱신)
- `api/suggest.js` — 수정 제안을 이 저장소의 Issue로 등록하는 Vercel 함수
- 이미지 폴더 — 가이드에 쓰인 이미지

## Vercel 환경변수
- `GITHUB_TOKEN` — 이 저장소의 Issues 읽기·쓰기 권한이 있는 fine-grained 토큰
- `GITHUB_REPO` — `계정명/저장소명`

수정 제안은 이 저장소의 **Issues**에 `[수정 제안]`으로 쌓여요.
