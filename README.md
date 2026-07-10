# 실적보고 슬라이드 디자인 스킬


월간 실적보고 슬라이드(1280×720, LINE Seed)를 **엑셀 데이터만 채우면** 디자인 가이드에 맞춰 자동 생성하는 Claude Code 스킬. 값(엑셀)과 표현(디자인)을 분리해, 어느 기기에서든 동일한 슬라이드를 재현한다.

> **⚠️ 안내: 이 저장소에 포함된 모든 수치는 더미(가상) 샘플 데이터입니다.**
> `data_template.xlsx`·`Unifi_AUM_일자별.xlsx`·`template.html`에 들어 있는 매출·손익·KPI·AUM·재무상태표·현금흐름 등의 값과 제품/타이틀명은 실제 데이터가 아니며, 디자인·레이아웃을 시연하기 위한 임의의 예시값입니다. 실제 보고 시에는 본인의 데이터로 덮어쓰세요.


## 설치 (팀원용)

Claude Code에서 아래를 실행:

```
/plugin marketplace add choi-jaehyung/report-slide-skill
/plugin install report-slide@report-slide
```

설치 후 스킬 호출: `/report-slide:report-slide`


## 사용법

1. 스킬을 실행하면 데이터 입력 템플릿(`data_template.xlsx`)을 안내한다.
2. 13개 시트(보고정보·Executive Summary·PL·NEXT Market·Balance Sheet·Cash Flow 등)에 이번 달 수치를 채운다. (현재 **더미 샘플 데이터**가 들어 있으니 본인의 실제 수치로 덮어쓰면 된다.)
3. 이어서 Unifi AUM·예치유저 데이터 템플릿(`Unifi_AUM_일자별.xlsx`)을 안내한다. 일자별 누적 AUM·예치유저 수를 최신 일자까지 입력/갱신한다. (Unifi KPI 슬라이드의 AUM 영역차트·예치유저 추이가 이 파일에서 생성된다.)
4. 채운 두 엑셀을 넘기면 디자인 가이드에 맞춰 슬라이드 HTML을 생성하고, Safari 도구로 PDF까지 변환한다.


## 구성

```
plugins/report-slide/skills/report-slide/
├── SKILL.md            스킬 정의·워크플로우
├── DESIGN_GUIDE.md     디자인 시스템 전체 명세
├── template.html       폰트·토큰·컴포넌트 CSS·표지 임베드된 시작 골격
├── data_template.xlsx  데이터 입력 템플릿(13시트)
├── Unifi_AUM_일자별.xlsx  Unifi AUM·예치유저 일자별 누적 데이터
├── assets/             표지 배경·로고 + LINE Seed 서브셋 폰트
└── tools/              html2pdf_safari (PDF 변환 도구)
```


## 유지 규칙

- 슬라이드 디자인을 수정하면 `DESIGN_GUIDE.md`도 동시에 갱신해 스킬과 실제 산출물을 항상 일치시킨다.
- PDF 변환: **macOS**는 `tools/html2pdf_safari`, **Windows/Linux**는 `tools/html2pdf_playwright.py`(headless Chromium; `pip install playwright pillow` + `python -m playwright install chromium` 필요). Chrome 벡터 print-to-pdf 단독은 애플 PDFKit에서 섀도우가 깨지므로 지양.
