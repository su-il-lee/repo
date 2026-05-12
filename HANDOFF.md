# HANDOFF.md — D:\claude 프로젝트 인수인계

> 작성일: 2026-05-12  
> 이 파일만 읽으면 다음 에이전트가 현재 상태를 파악하고 이어갈 수 있도록 작성됨.

---

## 프로젝트 개요

`D:\claude`는 빌드 도구 없이 운용되는 Python + 정적 HTML 워크스페이스.  
주요 용도: Azure Synapse Analytics 쿼리 → CSV 추출 → 자동 대시보드 HTML 생성.

---

## 디렉토리 구조 (주요 항목)

```
D:\claude\
├── Totalagent.py          # 메인 3단계 파이프라인 실행기
├── PBconnect.py           # Azure Synapse 연결 테스트
├── 2ndStep.py             # SQL 쿼리 → CSV 저장
├── dashboard_agent.py     # 최신 CSV → 대시보드 HTML 생성
├── gen_dashboard.py       # 대시보드 생성 보조 스크립트
├── infoU.ini              # ⚠️ Azure AD 자격증명 (절대 커밋 금지)
├── CLAUDE.md              # Claude Code 지시 파일
├── .gitignore             # 생성 완료 (아래 참고)
├── ai-sync-club/
│   └── index.html         # ✅ AI싱크클럽 랜딩페이지 (완성)
├── calculator/            # 정적 HTML 계산기
├── todo/                  # 정적 HTML 투두
├── todo-next/             # Next.js 투두앱
├── news_clipping/         # 뉴스 클리핑 관련
└── code/                  # 기타 코드
```

---

## 이번 세션에서 한 작업

### ✅ 성공한 것

1. **AI싱크클럽 랜딩페이지 생성** (`ai-sync-club/index.html`)
   - 단일 HTML 파일, 인라인 CSS/JS, 외부 의존성 없음 (Google Fonts CDN만 사용)
   - 섹션: 고정 NAV → Hero (풀스크린) → About (3카드) → Activities (3카드) → 가입 방법 (3단계 타임라인) → CTA 배너 → Footer
   - 디자인: 다크 네이비 (`#0d1117`) + 인디고/바이올렛/시안 그라디언트
   - 폰트: `Noto Sans KR` (Google Fonts)
   - 애니메이션: `IntersectionObserver` 기반 scroll-reveal (바닐라 JS)
   - 반응형: CSS Grid + Flexbox, 모바일 대응
   - 통계 수치: 회원 120+, 세션 48+, 프로젝트 30+ (placeholder)

2. **git 저장소 초기화** (`git init`)
   - `D:\claude`를 git 저장소로 초기화
   - 현재 `master` 브랜치, 아직 커밋 없음

3. **.gitignore 생성**
   - 제외 항목: `infoU.ini`, `*.csv`, `dashboard_*.html`, `node_modules/`, `.next/`, `.claude/`, OS 파일 등

### ❌ 실패 / 미완성

- 없음. 요청한 모든 작업 완료.

### ⚠️ 시도 안 한 것 (다음 단계 후보)

- 첫 번째 git commit 미수행 (사용자가 요청하지 않음)
- 랜딩페이지 콘텐츠 커스터마이징 (실제 연락처, SNS 링크, 실제 가입 URL)
- Vercel 배포 (todo-next 또는 ai-sync-club)
- `aa.csv`, `analysis.json` 등 정체불명 파일 정리

---

## 다음 에이전트를 위한 다음 단계 (우선순위 순)

1. **첫 커밋** — `.gitignore` 검토 후 `git add` + `git commit`  
   - 주의: `infoU.ini`가 스테이징되지 않도록 반드시 확인
   - 커밋 대상에서 제외해야 할 추가 파일 여부 사용자에게 확인 권장

2. **랜딩페이지 내용 확정** — `ai-sync-club/index.html`의 placeholder 값 교체  
   - 연락처 이메일, 오픈 카톡 링크, 실제 SNS URL
   - 통계 수치 (120+명, 48+회, 30+건) 실제 값으로 교체

3. **Vercel 배포 (선택)** — `ai-sync-club/` 단독 또는 전체 레포 배포  
   - 단일 HTML 파일이므로 Vercel Static 배포 즉시 가능

4. **todo-next 상태 확인** — Next.js 앱 현황 파악 및 필요 시 의존성 설치

---

## 환경 정보

| 항목 | 값 |
|---|---|
| OS | Windows 11 Enterprise |
| Shell | bash (Git Bash) |
| 작업 디렉토리 | `D:\claude` |
| Python 파이프라인 DB | Azure Synapse (`synapse-workspace-si.sql.azuresynapse.net` / `sibidb`) |
| 인증 방식 | ActiveDirectoryPassword (ODBC Driver 18) |
| 자격증명 파일 | `infoU.ini` (절대 커밋 금지) |

---

## 주요 파일 빠른 참조

- 파이프라인 실행: `python Totalagent.py`
- DB 연결 테스트: `python PBconnect.py`  
- 랜딩페이지: `D:\claude\ai-sync-club\index.html` (브라우저에서 직접 열기)
- Claude 지시 파일: `D:\claude\CLAUDE.md`
