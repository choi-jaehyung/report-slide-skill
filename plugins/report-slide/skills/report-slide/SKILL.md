---
name: report-slide
description: 엑셀 데이터 템플릿을 채우면 월간 실적보고 슬라이드(1280×720, LINE Seed 폰트)를 디자인 가이드에 맞춰 자동 생성한다. "실적보고 만들어줘/수정해줘", "보고 덱 생성", KPI·PL·Balance Sheet·Cash Flow·NEXT Market 등 재무 보고 슬라이드 작업 시 사용.
---


# 실적보고 슬라이드 디자인 스킬


**디자인 가이드 + 기본 이미지 + 엑셀 데이터**만으로 어느 기기에서든 동일한 실적보고 슬라이드를 재현한다. 값(엑셀)과 표현(디자인 가이드·템플릿)을 분리해, 매월 엑셀만 갈아끼우면 같은 룩의 보고서가 나온다.


## 구성 파일

- `data_template.xlsx` — **데이터 입력 템플릿.** 슬라이드별 시트 13개(00_보고정보 ~ 11_Cash&Crypto, 04b_Unifi KPI 포함). 현재 예시값이 채워져 있으니 매월 값만 덮어쓴다. 이 스킬의 시작점.
- `DESIGN_GUIDE.md` — **디자인 시스템 전체 명세.** 캔버스 규격·색상 토큰·타이포·컴포넌트 12종 스펙·값→픽셀 매핑·빌드 파이프라인·체크리스트. 슬라이드 생성 전 반드시 읽는다.
- `template.html` — **완성된 13페이지 참조 덱**(폰트·색상·전 컴포넌트 CSS·표지 + 실제 디자인이 반영된 모든 슬라이드, 샘플 데이터 포함). **새 보고서는 이 파일을 복제해 각 슬라이드의 데이터 값만 교체**한다(디자인/레이아웃/라벨 구조는 그대로). 처음부터 새로 그리지 말 것.
- `assets/cover.jpeg` — **필수 자산: 표지 배경 사진(텍스트 없는 깨끗한 사진).** template.html에 base64 인라인. 표지 제목·부제·보고월은 이미지에 굽지 않고 HTML 텍스트로 얹으므로 배경은 텍스트 없는 사진이어야 한다. 교체 시 이 파일을 대체하고 재인라인.
- `assets/logo.png` — 표지 로고. template.html에 base64 인라인(`.cover-logo`). 교체 시 이 파일을 대체하고 재인라인.
- `assets/fonts/*.woff` — LINE Seed 서브셋 폰트(400/700). 새 글리프 재서브셋용.
- `tools/html2pdf_safari` (+ `.swift`) — HTML→PDF 변환 도구(**macOS 전용**, WebKit/PDFKit). 
- `tools/html2pdf_playwright.py` — **크로스플랫폼(Windows/Linux/macOS) PDF 폴백**(headless Chromium 래스터화). Safari 없는 환경에서 사용.


## 워크플로우 — 이 스킬 실행 시


**A. 기본 흐름 (스킬 실행 시 이 순서로 사용자와 상호작용)**

1. **엑셀 템플릿 제공 + 업로드 요청.** `data_template.xlsx`를 사용자에게 전달하고 이번 달 수치로 채워 업로드해 달라고 요청한다.
   - 안내: `00_보고정보`엔 **보고 기준월(YYYY-MM)만** 입력(날짜 표기 자동 파생). 금액은 **원 단위로 입력**(엑셀은 백만원 표시, 0→`-`). 시트는 아래 "시트↔슬라이드" 표 참조.
   - 업로드되면 openpyxl로 전 시트 파싱. 빠진 값·형식 오류는 해당 시트·셀을 짚어 재요청.
2. **AUM·예치유저 데이터 요청.** 1이 완료되면, `Unifi_AUM_일자별.xlsx`(일자별 누적, **4/1~7/7 데이터가 입력된 상태로 제공**)를 전달하고 최신 일자까지 이어서 입력/갱신해 업로드해 달라고 요청한다. (이 파일에서 Unifi AUM 누적영역·예치유저 추이를 읽는다.)
3. **KRW 기준 슬라이드 생성 → PDF 전달.** **`template.html`(완성 참조 덱)을 복제한 뒤, 각 슬라이드의 데이터 값(숫자·라벨·날짜·차트 SVG)만 업로드된 데이터로 교체**한다. 디자인·레이아웃·라벨 텍스트 구조("MoM …", "예치 유저 추이", "Unifi 수익성 구조", "Apr 26/May 26", 최신값 pill, phead 단위 표기 등)는 참조 덱을 그대로 따른다(새로 그리거나 임의 변형 금지). 차트(막대/게이지/영역/도넛)는 새 데이터로 §5 규칙에 따라 크기·경로 재계산. 금액 변환: 백만원=원/1e6, 억원=원/1e8. **단, Executive Summary의 GMV는 억원으로 표기**(백만원값/100). **HTML은 내부 중간물이니 검토 요청 없이 곧바로 PDF로 변환(§PDF 변환)해 PDF만 전달한다.**
   - **결측치 처리(AUM·유저)**: 데이터에 빠진 날짜가 있으면 **앞뒤 실측 사이 선형보간 추정치로 채워 처음부터 그래프에 반영**한다(0으로 두고 나중에 후보정 금지). 단 토큰 도입 전 구간(IDRP 4/20·JPYC 5/26 이전 등 실제 값이 0인 구간)은 0을 유지.
4. **JPY 기준 슬라이드 여부 질문.** "일본 경영진 보고용 **JPY 기준·영어** 슬라이드도 만들까요? (예/아니오)"
   - **아니오** → 업무 종료.
   - **예** → 5로.
5. **환율 입력 요청.** "**100엔당 원화 환율**을 입력해 주세요(예: 900)." → rate 수령.
6. **JPY 변환.** 제출된 엑셀의 **KRW 금액만** 엔화로 환산: `JPY금액(엔) = KRW(원) × 100 / rate`. 표시 단위도 원→엔(**백만원→백만엔, 억원→억엔**). **변환 제외**: USD 금액(Unifi AUM), 카운트(명·MPU·예치유저), 비율(%)은 그대로.
7. **JPY·영어 슬라이드 생성.** 일본 경영진 보고용이므로 **덱 전체를 영어로** 작성한다.
   - 한글로 입력·표기된 모든 부분(제목·항목명·라벨·단위·주석·Key Insight 불릿 등)을 영어로 번역/치환. 표지 보고월·통화 단위도 영어(백만엔=JPY mn, 억엔=JPY 100M 등, 원화 KRW→JPY).
   - **원본이 한 줄이면 번역문도 한 줄**이 되도록 길이를 조정(요약).
   - 나머지 디자인/레이아웃/컴포넌트는 KRW 덱과 동일. **여기서도 HTML은 내부 중간물이며, 최종 산출물은 PDF로 변환해 전달한다.**

> **산출물 원칙: 이 스킬의 최종 산출물은 PDF다.** HTML은 슬라이드를 조립하기 위한 내부 빌드 파일일 뿐이므로 사용자에게 HTML을 검토시키지 않고 바로 PDF를 만들어 전달한다. (HTML을 직접 손봐야 하는 경우는 B의 디자인 수정 작업뿐.)

**PDF 변환 도구**(3·7 공통, 폭 1280·높이 720):
- **macOS**: `./tools/html2pdf_safari "<입력.html>" "<출력.pdf>" <슬라이드수> 720`
- **Windows/Linux**: `pip install playwright pillow ; python -m playwright install chromium` 후 `python tools/html2pdf_playwright.py "<입력.html>" "<출력.pdf>" <슬라이드수> 720`
- 결과는 실제 전달 채널로 한 번 열어 확인.

**B. 디자인 수정 지시를 받은 경우**

- 해당 HTML을 직접 편집하되, **수정 내용을 `DESIGN_GUIDE.md`에도 동시에 반영**해 스킬과 구현체를 항상 일치시킨다. 컴포넌트 스펙이 바뀌면 가이드 §4의 해당 항목을, 토큰이 바뀌면 §2를 갱신.


## 시트 ↔ 슬라이드 ↔ 컴포넌트 대응

| 엑셀 시트 | 슬라이드 | 주요 컴포넌트(가이드 §4) |
|---|---|---|
| 00_보고정보 | 표지 | cover-slide(텍스트 없는 배경사진 + 반투명 패널 + 로고) + 편집 텍스트 `.cover-title`·`.cover-sub`·`.cover-date`(보고월=표지 표기 영문값) |
| 01_Executive Summary | Executive Summary | 스탯카드 + es-label 3구획 + summary-panel |
| 02_Income Statement | Income Statement | 그룹막대(매출)·다이버징막대(손익) |
| 03_KPI by Product | KPI by Product | 게이지(% of Plan) + rpt 표 |
| 04_PL by Product | PL by Product | `table.rpt.pl` (Total 열 강조) |
| 04b_Unifi KPI | Unifi KPI | 수식박스(수익성 구조). AUM 영역차트·예치유저 선차트는 **별도 파일** `Unifi_AUM_일자별_*.xlsx` |
| 05_NEXT Market | NEXT Market Profitability | `table.rpt.nmp` (균일 44px 행) |
| 06_Personnel | Personnel Expenses | 가로 스택막대 / 표 |
| 07_Marketing | Marketing | 도넛 + 그룹막대(Plan vs Actual) |
| 08_Balance Sheet | Balance Sheet | `.bsx` + Current/Debt/Equity Ratio |
| 09_Key Elements BS | Key Elements of BS | 가로 그룹막대 + 콜아웃 |
| 10_Cash Flow | Cash Flow | 워터폴 + cf-cards |
| 11_Cash&Crypto Proj | Cash & Crypto Projection | 세로 스택막대 + 손익 추이 |


## 필수 준수 사항

- **표지 이미지는 필수 요소.** 모든 덱은 `assets/cover.jpeg`(또는 지정 표지, 텍스트 없는 배경사진)를 base64 인라인한 표지 슬라이드로 시작. 표지 제목·부제·보고월은 이미지가 아닌 HTML 텍스트로 얹는다(제목 편집 시 이미지 재렌더링 금지).
- 캔버스 1280×720 고정, `.slide` padding 63/81, 상단 블루바 7px(표지 제외).
- 색상은 가이드 §2 토큰만(계열 c1→c4, 음수 `#E5484D`). 폰트·이미지·스타일 전부 HTML 한 파일에 인라인(외부 링크 금지).
- chart-panel 소프트 섀도우(`0 20px 40px -18px rgba(20,23,31,.18)`) 제거 금지.
- PDF 변환: macOS는 `html2pdf_safari`, 그 외 OS는 `html2pdf_playwright.py`(크로스플랫폼). Chrome 벡터 print-to-pdf 단독 사용은 지양(애플 PDFKit 섀도우 깨짐).
- **슬라이드 디자인을 수정하면 `DESIGN_GUIDE.md`도 동시에 갱신**한다.
