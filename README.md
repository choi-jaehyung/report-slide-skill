# 실적보고 슬라이드 디자인 스킬


월간 실적보고 슬라이드(1280×720, LINE Seed)를 **엑셀 데이터만 채우면** 디자인 가이드에 맞춰 자동 생성하는 Claude Code 스킬. 값(엑셀)과 표현(디자인)을 분리해, 어느 기기에서든 동일한 슬라이드를 재현한다.


## 설치 (팀원용)

Claude Code에서 아래를 실행:

```
/plugin marketplace add choi-jaehyung/report-slide-skill
/plugin install report-slide@report-slide
```

설치 후 스킬 호출: `/report-slide:report-slide`


## 사용법

1. 스킬을 실행하면 데이터 입력 템플릿(`data_template.xlsx`)을 안내한다.
2. 12개 시트(보고정보·Executive Summary·PL·NEXT Market·Balance Sheet·Cash Flow 등)에 이번 달 수치를 채운다. (현재 예시값이 들어 있으니 덮어쓰면 된다.)
3. 채운 엑셀을 넘기면 디자인 가이드에 맞춰 슬라이드 HTML을 생성하고, Safari 도구로 PDF까지 변환한다.


## 구성

```
plugins/report-slide/skills/report-slide/
├── SKILL.md            스킬 정의·워크플로우
├── DESIGN_GUIDE.md     디자인 시스템 전체 명세
├── template.html       폰트·토큰·컴포넌트 CSS·표지 임베드된 시작 골격
├── data_template.xlsx  데이터 입력 템플릿(12시트)
├── assets/             표지 이미지 + LINE Seed 서브셋 폰트
└── tools/              html2pdf_safari (PDF 변환 도구)
```


## 유지 규칙

- 슬라이드 디자인을 수정하면 `DESIGN_GUIDE.md`도 동시에 갱신해 스킬과 실제 산출물을 항상 일치시킨다.
- PDF 변환: **macOS**는 `tools/html2pdf_safari`, **Windows/Linux**는 `tools/html2pdf_playwright.py`(headless Chromium; `pip install playwright pillow` + `python -m playwright install chromium` 필요). Chrome 벡터 print-to-pdf 단독은 애플 PDFKit에서 섀도우가 깨지므로 지양.
