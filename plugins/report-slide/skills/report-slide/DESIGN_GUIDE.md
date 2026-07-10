# 실적보고 슬라이드 디자인 가이드

> 목적: **이 가이드 + 기본 이미지 자산 + 데이터**, 이 세 가지만 있으면 어느 기기·어느 도구에서도 동일한 슬라이드를 재현할 수 있도록 디자인 시스템 전체를 명세한다. 값(수치)과 표현(디자인)을 분리해, 매월 데이터만 갈아끼우면 같은 룩의 보고서가 나오게 하는 것이 최종 지향점이다.

> 기준 구현체: `output/실적보고 v2(디자인가이드 적용).html` (단일 HTML, 13페이지) = 스킬의 `template.html`. 이 문서와 구현체가 어긋나면 **구현체가 정답**. **스킬로 새 보고서를 만들 때는 이 완성 덱(template.html)을 복제해 데이터만 교체**하고 라벨·레이아웃은 그대로 둔다(처음부터 새로 그리면 미세 디자인이 어긋난다).


## 0. 재현에 필요한 3가지 입력


슬라이드 1장을 재현하는 것은 아래 세 입력을 조립하는 일이다.

1. **디자인 가이드(이 문서)** — 캔버스 규격, 색상 토큰, 타이포, 컴포넌트별 CSS 스펙과 값→픽셀 매핑 규칙. 기기·도구가 바뀌어도 불변.
2. **기본 이미지 자산** — 슬라이드에 들어가는 비-CSS 그래픽. 현재 덱에서는 **표지 배경 사진 1장(텍스트 없는 깨끗한 사진)**과 **로고 1개**(`assets/logo.png`)가 있으며, 모두 HTML 안에 base64로 인라인되어 외부 파일 의존이 없다. **표지의 제목·부제·보고월 텍스트("LINE NEXT" / "Financial Report" / 예 "May 2026")는 이미지에 굽지 않고 모두 HTML 텍스트(`.cover-title`·`.cover-sub`·`.cover-date`)로 얹는다** — 제목을 바꿔도 이미지 재렌더링이 필요 없어 배경 왜곡이 없다. 보고월은 데이터(입력)로 취급해 매월 바꾼다.
3. **데이터** — 각 페이지에 들어갈 수치·항목명·기간. 표현과 분리해 관리하며, 컴포넌트의 "데이터 매핑" 항목이 값이 어디에 꽂히는지 규정한다.

핵심 원칙: **폰트·이미지·스타일을 전부 HTML 한 파일에 인라인**한다. 외부 폰트 링크나 이미지 파일 참조가 없어야 인터넷·설치 환경과 무관하게 어느 기기에서든 픽셀 단위로 동일하게 렌더된다.


### 데이터 템플릿 입력 규칙(값 최소화)


- **날짜는 보고 기준월 하나로 파생**: `00_보고정보`에 **보고 기준월(YYYY-MM)만** 입력하면, 표지 영문월(예 "May 2026")·NEXT Market 당월(YYYY.MM)·Income Statement 6개월 시계열(최근 6개월, 마지막은 (F))·Cash&Crypto 축 등 날짜 표기를 스킬이 자동 생성한다. 개별 시트의 날짜 헤더를 수정하면 그 값이 우선한다.
- **금액 입력·표시 규칙**: 금액은 **원 단위(full)로 입력**한다. 엑셀 표시형식은 `#,##0,,;-#,##0,,;-`(원→백만원, 0은 `-`), 숫자는 우측정렬. 슬라이드 렌더 시 원값을 항목 단위로 변환한다 — **백만원 = 원/1,000,000**, **억원 = 원/100,000,000**, 명·비율은 그대로. (엑셀은 항상 백만원 표시, 슬라이드만 억원 등으로 변환.) **예외: Executive Summary의 GMV는 슬라이드에서 억원으로 표기**(백만원값/100). Unifi AUM(exec)도 억원.
- **AUM·예치유저는 별도 파일**: Unifi AUM(USDT/IDRP/JPYC 일자별 달러)·예치유저 추이는 `Unifi_AUM_일자별_*.xlsx`(일자별 누적)에서 읽는다. `04b_Unifi KPI` 시트는 수익성 구조만 담는다. AUM은 k USD, 예치유저는 명.
- **결측치 보간**: AUM·예치유저에 빠진 날짜가 있으면 앞뒤 실측 사이 **선형보간 추정치로 채워 처음부터 그래프에 반영**한다(0으로 두고 후보정 금지). 단 토큰 도입 전 실제 0 구간(IDRP 4/20·JPYC 5/26 이전)은 0 유지.


## 1. 캔버스 & 슬라이드 골격


- **슬라이드 규격: 1280 × 720px 고정** (16:9). `@page{size:1280px 720px;margin:0;}`. 폭 1280은 PDF 변환 도구에도 하드코딩되어 있으므로 바꾸지 않는다.
- 각 슬라이드는 `<div class="slide">` 하나. 세로 flex 컬럼, `padding:63px 81px 63px`, `overflow:hidden`, `page-break-after:always`.
- **상단 블루 바**: 모든 슬라이드 최상단에 높이 7px 풀폭 바(`--blue`). `.slide::before`로 구현. 표지(`.cover-slide`)만 예외로 숨김.
- **페이지 헤더 `.phead`**: 제목(`h2`, 40px/700)과 우측 하단 단위 표기(`.unit`, 14px, 예 "(백만원)")를 양끝 배치. 하단에 `2px solid var(--ink)` 구분선, `padding-bottom:16px`. 제목·단위 모두 baseline(`align-items:flex-end`).
- **본문 `.body`**: `flex:1; margin-top:26px;` 세로 flex. 남는 공간을 컴포넌트가 채운다.
- **페이지 번호 `.pagenum`**: 우하단(`right:24px; bottom:18px`), 13px, `#9AA1AD`. 표지 제외 `01`부터 2자리.
- **범례 `.legend`** / **주석 `.note`**: 범례는 상단 좌측(14px/700, `--muted`), 단위는 `margin-left:auto`로 우측. 주석은 하단(12.5px, `--muted`, line-height 1.5), 계산식·전제는 여기에 `*` 접두로.


## 2. 색상 토큰


```
--ink:#14171F     기본 텍스트·강한 구분선
--muted:#6B7280   보조 텍스트·라벨
--line:#E6E9EF    옅은 구분선·트랙 배경
--blue:#1A56DB    브랜드 블루(상단바·제목 강조·불릿)
--blued:#103A96   진한 블루
--panel:#F5F7FB   패널·카드·스탯 배경
--chip:#E9F0FF    칩 배경

차트 계열색(범주 구분, 이 순서로 사용):
--c1:#4A7FF7  (실적·주계열)
--c2:#AE8DF5
--c3:#ECB565
--c4:#F9DE59
--grey-series:#C7CCD6  (계획/기준선 등 대조계열)

--emerald:#10B981  긍정 강조
--pink:#F472B6
음수/적자 전용: #E5484D (red)
```

규칙: 계열 구분은 **c1→c2→c3→c4 순서**로 배정한다. "계획 vs 실적" 같은 대조는 계획=`--grey-series`, 실적=`--c1`. 음수·적자·감소는 오직 `#E5484D`.


### 제품 표기 순서 (전 페이지 공통)


여러 제품이 나열되는 모든 표·차트·범례는 **다음 순서를 고정**한다:

**Unifi · NEXT Market · Hyze · Game · Alive · MOLTS · AI Friends · Xenesis · etc**

- 목록에 없는 항목(예 Personnel의 Service Supply)은 목록 제품들 뒤·`etc` 앞에 둔다.
- Total 행/열은 표에서 맨 앞(또는 관례상 위치) 유지. 도넛·범례도 이 순서로 세그먼트/행을 배열하고 색은 c1→c4 순.
- KPI by Product 페이지는 **AI Friends 행을 두지 않는다**(해당 페이지 한정 제외). Unifi AUM 미니차트 단위는 **k USD**.


## 3. 타이포그래피 & 폰트 임베드


- **서체: LINE Seed Sans KR.** `font-family:'LSKR','LINE Seed Sans KR','Apple SD Gothic Neo',sans-serif`. 웨이트는 400·700 두 가지만 사용.
- **임베드 방식(재현성의 핵심):** 폰트를 외부 링크로 부르지 않고, 필요한 글리프만 **서브셋한 woff를 base64로 `@font-face`에 인라인**한다. 400/700 각각 `'LSKR'`와 `'LINE Seed Sans KR'` 두 이름으로 등록(별칭). `font-display:swap`.
  - 서브셋은 문서에 실제로 쓰인 문자만 포함해 용량을 줄인다(각 ~24KB 수준). 새 텍스트에 기존 서브셋에 없는 글리프가 들어가면 재서브셋이 필요하다 — 렌더 시 해당 글자가 fallback 폰트로 나오면 이 신호다.
  - 도구: `fonttools`의 subset. 원본 woff/ttf에서 `pyftsubset original.ttf --text-file=used_chars.txt --flavor=woff --output-file=sub.woff` 후 base64로 `url(data:font/woff;base64,…) format('woff')`에 삽입.
- **크기 체계(주요값):** 페이지 제목 40/700 · 패널 제목(h3) 18/700 · 스탯값 25/700 · 도넛 중앙값 36/700 · 게이지값 26/700 · 표 본문 14.5(nmp 12.5, pl 14) · 라벨/축 12.5~14/700 · 주석 12.5.


## 4. 컴포넌트 카탈로그


각 컴포넌트는 **용도 → 핵심 스펙 → 데이터 매핑** 순. 클래스명은 구현체와 1:1 대응한다.


### 4.0 표지 (`.cover-slide` — 텍스트 편집형)


- **원칙: 표지의 모든 텍스트(로고 제외)는 이미지에 굽지 않고 HTML 텍스트로 얹는다.** 배경 사진은 **텍스트가 전혀 없는 깨끗한 사진**이며, 로고·제목·부제·보고월은 각각 편집 가능한 요소로 분리한다. 제목을 바꿔도 이미지를 재렌더링할 필요가 없어 배경 왜곡이 발생하지 않는다.
- 구조: `<div class="slide cover-slide" style="padding:0;">` 안에
  1. 배경 사진 `<img class="cover-bg">`(base64, `object-fit:cover`로 슬라이드 전체를 채움),
  2. 반투명 패널 `<div class="cover-overlay">`, 그 안에
     - 로고 `<img class="cover-logo">`(base64, `assets/logo.png`),
     - 제목 `<div class="cover-title">LINE NEXT</div>`,
     - 부제 `<div class="cover-sub">Financial Report</div>`,
     - 보고월 `<div class="cover-date">Apr 2026</div>`.
- 컴포넌트 스펙(모든 좌표는 `.cover-overlay` 기준):
  - `.cover-bg`: `position:absolute;inset:0;width:100%;height:100%;object-fit:cover`.
  - `.cover-overlay`: `position:absolute;inset:72px;background:rgba(0,0,0,.749)` — 슬라이드 4변에서 72px 안쪽에 놓인 반투명 검정 패널.
  - `.cover-logo`: `position:absolute;top:34px;left:50%;transform:translateX(-50%);width:152px;height:152px;opacity:.9`.
  - `.cover-title`: `top:214px`, 중앙정렬, 흰색, LINE Seed **Bold(700)**, `font-size:80px;line-height:1.0;letter-spacing:0.5px`.
  - `.cover-sub`: `top:306px`, 중앙정렬, 흰색, LINE Seed **Regular(400)**, `font-size:68px;line-height:1.0`.
  - `.cover-date`: `top:472px`, 중앙정렬, 흰색, LINE Seed **Regular(400)**, `font-size:20px;letter-spacing:0.5px`.
- 데이터 매핑: 엑셀 `00_보고정보` 시트의 **표지 표기(영문)** 값(예 "May 2026")을 `.cover-date` 텍스트로. 제목·부제(`LINE NEXT` / `Financial Report`)는 고정 텍스트이며 JPY·영어 덱에서도 그대로(단위·통화 표기는 각 덱 규칙을 따른다).
- 배경/로고 교체 시: 새 이미지를 `assets/cover.jpeg`·`assets/logo.png`에 넣고 base64로 재인라인. 배경은 반드시 텍스트가 없는 깨끗한 사진을 쓴다.


### 4.1 스탯카드 · 요약 (Executive Summary)


- **`.stat-row` / `.statcard`**: 가로 flex, `gap:24px`, 각 카드 `flex:1`. 카드 배경 `--panel`, radius 14, padding `15px 22px`.
- 카드 내부: 라벨 `.l`(14/700, muted) → 값 `.v`(25/700) → 진행 트랙 `.bar-track`(높이 8, 배경 `--line`, radius 4) + `.bar-fill`(`--blue`, 음수는 `.neg` → 우측정렬·`#E5484D`) → `.pct`(13, muted, 우측정렬).
- **`.es-label`**: 섹션 구분 소제목. 13/700, `letter-spacing:.04em`, `--blue`, 대문자. Finance / Business / Key Insight 3구획 구분에 사용.
- **`.summary-panel`**: 불릿 리스트 패널(`--panel`, radius 14). `li` 15px/line 1.55, 좌측 불릿은 `::before` 6px 원 `--blue`.
- 데이터 매핑: 카드당 (라벨, 값, 계획대비%, 진행률 막대폭%). 막대폭은 값/계획 비율을 %로. **Business 구획 지표는 모두 "계획비"(달성율) 기준**으로 표기(전월비 사용하지 않음).


### 4.2 표 (`table.rpt`)


기본 표. 공통 규칙:

- `width:100%; border-collapse:collapse; font-size:14.5px`.
- thead th: 하단 `2px solid var(--ink)`, 가운데정렬(첫 열 좌측), 13px/700 muted.
- td: 하단 `1px solid var(--line)`, 우측정렬(첫 열 좌측·700).
- `td.hl`: 블루 강조. `tr.total td`: 700 + 배경 `--panel`. `tr.indent td:first-child`: `padding-left:26px`, 400, muted (하위 항목).

**변형 A — `table.rpt.pl` (PL by Product):** 폰트 14, th/td 상하 padding 6(균일 행높이), 첫 열 `nowrap`. **첫 헤더셀은 비움**(구분 등 텍스트 없이 빈 셀). **마지막 열(Total) 강조**: 배경 `#F1F6FF`, `border-left:2px solid #D7E4FB`, 700, thead는 블루 글자.

**변형 B — `table.rpt.nmp` (NEXT Market Profitability):** 폰트 12.5. **모든 th·td `height:44px`, 상하 padding 0**으로 헤더 포함 전 행 높이 완전 균일. thead th는 `vertical-align:bottom; padding-bottom:9px`로 2줄 헤더(그룹행+열헤더행)에서 라벨 baseline을 일치시킨다. 둘째 헤더행 첫 셀(GMV)은 `text-align:center` 오버라이드. 첫 열 `nowrap`(제목 줄바꿈 방지, colgroup 첫 열 160px). 그룹 헤더 `th.grp`: 가운데정렬·`--panel` 배경. **누적 그룹은 "누적 (Cumulative)", 당월 그룹은 엑셀 `00_보고정보`의 당월(YYYY.MM) 값을 받아 "당월 2026.06" 형식**(영문 This Month 표기 없음). 한계이익 열 `td.mgn/th.mgn`: 배경 `#EAF3FF`·700. 누적/당월 그룹 경계 `.gsep`: `border-left:2px solid #C4D6F8`. 온보딩 열(2번째) 가운데정렬·muted.


### 4.3 세로 그룹 막대 — 계획 vs 실적 (`.gbar-*`)


- 컨테이너 `.gbar-chart`: 가로 flex, `align-items:flex-end`, 하단 `2px solid --line` 축선.
- 그룹 `.gbar-group`(카테고리 1개) 안에 막대 2개(`.bar.plan` grey / `.bar.actual` c1), 폭 26px, radius `4px 4px 0 0`. 값 라벨 `.val`은 막대 위 `top:-20px`.
- 축 라벨 `.gbar-axis`: 그룹과 같은 flex 배분, 12.5/700 가운데.
- 데이터 매핑: 카테고리별 (계획값, 실적값). 높이는 §5 매핑 규칙.


### 4.4 다이버징 막대 — 손익 +/- (`.dbar-*`)


- `.dbar-chart` 안에 `.zero`(50% 위치 0선). 그룹 `.dbar-group` 높이 100%, 내부 `.dbar-pair`(폭 60px 중앙정렬).
- 막대 계획/실적 각 폭 26(계획 left:0, 실적 left:29). 양수 `.up`(위로, radius 상단), 음수 `.down`(아래로, radius 하단). 0선 기준 위/아래 배치.
- 데이터 매핑: 값의 부호로 up/down, 절대값으로 0선 대비 높이%.


### 4.5 가로 스택 막대 (`.hstack-*`)


- 행 `.hstack-row`: 라벨 `.lbl`(폭 110, 우측정렬 14/700) + 트랙 `.track`(높이 26, 배경 --panel, radius 6) + 합계 `.total`(폭 56).
- 트랙 안 `.fill` 내부에 세그먼트 `.seg.a`(c1)·`.seg.b`(c3), 흰 글자 11.5/700 중앙. **범례 스와치 색은 세그먼트 색과 반드시 일치**시킨다(Personnel: Employee c1 / Outsourcing c3).
- **값 레이블 오버플로 처리**: 막대가 짧아 값이 막대 안에 다 안 들어가면(대략 막대폭 < 텍스트폭), 세그 안 값을 비우고 막대 오른쪽 바깥에 `.segout`(11.5/700, **어두운색 `--ink`** — 밝은 트랙 배경 위이므로)로 표시한다. 이때 `.track`은 `display:flex;align-items:center`, `.fill`은 `flex:0 0 auto`.
- 데이터 매핑: 행별 (세그먼트 값 배열, 합계). 세그폭% = 세그값/행최대.


### 4.6 가로 그룹 막대 + 콜아웃 (`.hgroup-*`, `.callout`)


- `.hgroup-row`: 라벨 `.lbl`(폭 82, 우측 13/700) + `.bars`(세로 2줄, 우측 margin 62 — 값 라벨 공간). 막대 높이 17, radius 우측만. `.bar.apr` grey / `.bar.may` c1. 값 `.v`는 막대 오른쪽 바깥(`left:100%`, margin-left 6).
- `.callout`(예 Market Value Gap): --panel 카드, `.cap`(블루) + `.val`. **폭은 `width:fit-content`(텍스트+여백), 내부 텍스트 가운데정렬(`align-items:center;text-align:center`)**, 관련 데이터 레이블 **바로 옆(적당한 여백)**에 절대배치. 페이지 단위는 제목이 아니라 **범례 우측 `.unit`(그래프 영역)**에 둔다.


### 4.7 도넛 (`.donut-*`)


- `.donut-box` 260×260. 원형 차트는 **conic-gradient** 배경 또는 SVG 아크로 구현하되 계열색 c1→c2→c3→c4 순.
- 중앙 `.donut-center`: 값 `.v`(36/700, 1.3배), 라벨 `.l`(13 muted)에 단위(한글 "백만원").
- 범례 `.donut-legend`: 세로, 행마다 스와치 + 라벨(15/700) + 값(13.5 muted/400).


### 4.8 게이지 (반원+ 270° 아크)


- 구조: `.gauge-box`(폭 190, 가운데정렬). 내부 SVG `viewBox="0 0 220 180"`, `<g transform="rotate(-225 110 100)">` 안에 원 2개(r=80, stroke-width 20, linecap round):
  - 트랙(배경): `stroke="#E6E9EF" stroke-dasharray="376.8 502.4"` — 270° 아크.
  - 값(채움): `stroke="#4A7FF7" stroke-dasharray="<dash> 502.4"`.
- **핵심 공식:** 원주 = 2π×80 ≈ 502.4. 270° 아크 길이 = 502.4 × 3/4 ≈ **376.8**. 값 채움 `dash = 백분율/100 × 376.8`.
  - 예: 42% → 158.2 · 58% → 218.5 · 71% → 267.5.
- 중앙 값 `.gauge-center .v`(26/700), 하단 `.gauge-label`(15/700). 여러 게이지는 라벨(예 "to Asset"/"to Equity")로 구분.


### 4.9 워터폴 (`.wf-*`)


- `.wf-chart`: position relative, 상하 여백(top 30/bottom 38 — 값·라벨 공간). 좌측이 축과 겹치지 않도록 `margin-left:35px`(축선 `.wf-axis-line`은 `left/right:-35px`).
- `.wf-bar`: 절대배치, 폭 81, radius 상단. 값 `.val`(위 -24, 14/400), 라벨 `.lbl`(아래 -30, 13.5/700).
- **감소(음수) 막대는 하단 라운딩**: `.wf-bar.neg{border-radius:0 0 5px 5px}` (증가/총계 막대는 상단 라운딩). 워터폴에서 아래로 내려가는 변화이므로 끝(아래)을 둥글게.
- 데이터 매핑: 시작→증감→종료 누적. 각 막대의 bottom/height를 누적값으로 계산.


### 4.10 세로 스택 막대 — 다기간 (`.vstack-*`)


- `.vstack-chart`: 가로 flex align-end, 하단 축선. 컬럼 `.vstack-col` 높이 100%, 세그 폭 58%.
- `.seg.top`(c2, radius 상단) / `.seg.bot`(c1). 흰 글자 9.5/700. 컬럼 위 합계 `.total-lbl`(12.1/700 — 강조 확대).
- 축 `.vstack-axis`(12.6/700 — 날짜 확대). (증감 보조행 `.vstack-pl`은 제거됨 — 차트가 콘텐츠 영역을 꽉 채우도록 `.vstack-chart` flex:1이 여백을 흡수.)


### 4.11 Balance Sheet 레이아웃 (`.bsx` 상단 + `.bs-ratios` 하단)


`.body`는 세로 2단(`flex-direction:column`): **상단 막대(자산/부채/자본) · 하단 비율 3종 좌우 배치.**

- **상단 `.bsx`**: 세로 flex. 각 행 `.r`은 `[라벨 .nm | 막대 .barwrap]` 가로 배치 — **라벨이 막대 왼쪽 옆**(위가 아님). 전폭을 써서 막대를 길게 뽑는다.
  - `.nm` 폭 172 고정, 항목명 폰트 top행 20px·sub행 15.5px(콤팩트), muted, sub는 `padding-left:34`. 행간 `gap:6`, `.bsx`는 `flex:0 0 auto`(자연높이)로 상단 영역을 낮춰 하단 박스를 위로 올린다.
  - **하위행 막대는 출발점도 들여쓴다**: `.bsx .r.sub .barwrap{margin-left:46px}` (라벨뿐 아니라 막대 시작점도 우측 이동).
  - 막대 `.bar` 높이 29(sub 22), radius 우측만. **상위·하위행 모두 값+MoM을 막대 안 양끝**(`.mom`, `justify-content:space-between`, 흰색). 막대가 너무 짧아 값·MoM이 겹칠 때만 예외적으로 MoM을 막대 밖 `.smom`(muted)로 뺀다. 계열색: 자산 c1, 부채 c2, 자본 c3.
  - 적자 행 `.r.def`: 값 `.dv`는 12px·`#E5484D`(하위 값과 동일 출발점 `padding-left:12`, 마이너스는 `text-indent:-0.42em`로 숫자 좌측끝 정렬), 옆에 MoM(`.smom` muted). barwrap `justify-content:space-between`로 오른쪽 끝에 **단위 `.bsunit`(백만원)**을 둔다 — 즉 단위를 Deficit 행과 같은 높이 우측에 표기(별도 줄 두지 않음).
- **단위 표기**: Balance Sheet는 예외적으로 단위 "(백만원)"를 제목이 아니라 **막대 그래프 영역의 우측 하단**(bsx와 ratios 박스 사이 오른쪽)에 둔다.
- **하단 `.bs-ratios`**: **흰 배경 패널로 감싸고 소프트 섀도우**(border 1px --line, radius 16, `box-shadow:0 20px 40px -18px rgba(20,23,31,.18)`, padding `20px 26px 24px`). 내부는 가로 flex 3열(`align-items:flex-start`로 **세 타이틀을 같은 높이**에 정렬), `.bs-rcol`(flex:1, 세로·가운데). 각 열 상단에 `.bs-secttl`(16/700 가운데).
  1. **Current Ratio**: `.cr-wrap` 안에 `.crrow` 얇은 가로막대(높이 12, radius 6). 전월(Apr 286%)·당월(May 262%) 2행, 사이 간격 벌림. **두 막대를 열 안에서 수직 중앙 정렬**(`position:absolute;top:50%;translateY(-50%)`)해 게이지 중앙 숫자 높이와 맞춘다.
  2. **Debt Ratio**: `.gwrap`에 게이지 2개(42% to Asset, 71% to Equity).
  3. **Equity Ratio**: `.gwrap`에 게이지 1개(58%, 하단 라벨 "Equity / Assets").


### 4.12 Cash Flow 카드 (`.cf-*`)


- 불릿은 텍스트 세로 중앙에 오도록 `li::before{top:0.95em;transform:translateY(-50%)}`(line-height 1.9 기준).
- `.cf-cards` 세로 flex. `.cf-card`(**흰 배경 + border 1px --line + 소프트 섀도우** `0 20px 40px -18px rgba(20,23,31,.18)`, radius 12, padding `18px 20px`): 헤더 `.h`(19/700, 값 `.v` 블루) + 불릿 리스트(14.5, muted 불릿). 다른 페이지 패널과 동일한 영역구분 스타일.
- 차트와 우측 텍스트 박스 병치 시 박스 폭·행간 여유를 둔다.


### 4.13 영역·선 차트, 수식 박스 (Unifi KPI)


- **누적 영역 차트(스택)**: `.area-wrap` 안에 인라인 SVG. 계열 3개(USDT c1 / IDRP c2 / JPYC c3)를 아래에서 위로 스택. 각 밴드는 `<path>`(상단선 L→R + 하단선 R→L + Z)로 채움, `opacity:0.92`. `preserveAspectRatio="none"`로 패널을 채운다. 하단 `.area-axis`(날짜 라벨 12/700 muted, space-between).
  - 데이터 매핑: 데일리 시계열 3계열. Y = `H − 누적값/ymax×H`, X = `i×(W/(N−1))`. **Unifi AUM 단위는 k USD**, 패널 제목은 "Unifi AUM"(누적 등 부기 없음).
  - **X축 날짜는 보고 기간에 맞춰 매번 바뀐다** — 스킬/템플릿에 특정 날짜를 고정하지 않고, 해당 월 범위로 라벨만 채운다.
  - 상단 두 차트 패널(`.ukpi-top`)과 하단 수익성 패널(`.ukpi-formula`)의 높이 비율은 flex로 조절(현행 약 2.1 : 0.9 — 차트를 크게, 수식 박스는 낮게).
- **선 차트**: 같은 `.area-wrap`/SVG. 단일 계열 `<path>` 스트로크(c1, width 3) + 옅은 영역채움(c1 opacity 0.10). 합계 추이 등 단일 값.
- **면적 채움 규칙(★PDF 호환)**: 영역/면적 채움은 **SVG linearGradient의 stop-opacity를 쓰지 말 것** — Safari/WebKit PDF 변환이 그라데이션 투명도를 무시해 불투명하게 깨진다(HTML은 정상, PDF만 solid로). 대신 **단색 fill + `fill-opacity`(또는 element `opacity`) 0.10~0.12**로 옅은 음영을 낸다. (KPI AUM·예치유저·Unifi AUM 모두 이 방식.)
- **최신값 라벨**: 각 차트의 최신 데이터 지점 **위쪽 빈 공간**에 `.chart-last`(절대배치 우측, 흰 반투명 pill, `--ink`)로 표시 — 채워진 영역/선과 겹치지 않게 그 위로 올린다. `.area-wrap`은 `position:relative`.
- **단위·범례 규칙**: 단위는 제목이 아니라 **그래프 영역 안**(범례 우측 `.unit`)에 둔다. **범례 항목이 하나뿐이면 범례를 생략**하고 단위만 우측에 표시(예 예치 유저 "(명)").
- **수식 박스 `.frow`**: 가로 flex(`flex:1;align-items:stretch`로 **박스가 패널 높이를 채워** 여백 최소화). `.fbox`(--panel, radius 12, 세로 flex 가운데정렬) = 라벨 `.fl`(13/700 muted) + 값 `.fv`(26/700). 연산자 `.fop`(24/700 muted, ×/−/=). 결과 박스 `.fbox.res`(배경 --chip, `.fv` 블루). 단계식: [A] × [B] − [C] = [결과]. 예시 주석 없이 박스만 배치.


## 5. 값 → 픽셀 매핑 규칙 (차트 공통)


막대·게이지는 "데이터만 바꿔도 재현" 되려면 값→크기 변환이 결정적이어야 한다.

- **세로 막대(gbar/dbar/vstack)**: 축 영역 높이를 100%로 두고, `막대높이% = 값 / 축최대값 × 100`. 축최대값은 해당 차트의 (계획·실적 포함) 최대치를 올림한 눈금값으로 고정. 다이버징은 0선 위/아래로 분리해 각각 절대값 기준.
- **가로 막대(hstack/hgroup/crrow)**: `채움폭% = 값 / 행(또는 차트) 최대값 × 100`.
- **게이지**: §4.8 공식(`dash = 퍼센트/100 × 376.8`).
- **워터폴**: 각 스텝 bottom = 직전 누적/축최대, height = 증감/축최대.

값 라벨은 항상 실제 수치를 표기(막대 길이는 시각화, 숫자는 라벨이 담당).


## 6. 슬라이드 구성 (현재 덱, 12페이지)


표지 + 본문 12(총 13슬라이드). 각 페이지가 쓰는 주요 컴포넌트:

| # | 페이지 | 주요 컴포넌트 |
|---|--------|--------------|
| 표지 | Cover | 배경 사진(base64, 텍스트 없음, 상단바 숨김) + 반투명 패널 + 로고 + 편집 텍스트 `.cover-title`·`.cover-sub`·`.cover-date`(보고월=변수) |
| 02 | Executive Summary | 스탯카드 + es-label 3구획 + summary-panel |
| 03 | Income Statement | 그룹막대(매출)·다이버징막대(손익) |
| 04 | KPI by Product | 게이지(% of Plan) + rpt 표 |
| 05 | PL by Product | `table.rpt.pl` (Total 열 강조) |
| 06 | **Unifi KPI** | 누적 영역차트(USDT/IDRP/JPYC) + 선차트(예치유저) + 수식박스(`.frow`) |
| 07 | NEXT Market Profitability | `table.rpt.nmp` (누적/당월, 균일 44px 행; 둘째 헤더행 GMV도 가운데정렬) |
| 08 | Personnel Expenses | 가로 스택막대(Employee c1 / Outsourcing c3) |
| 09 | Marketing | 도넛 + 그룹막대 |
| 10 | Balance Sheet | `.bsx` 상단 + `.bs-ratios` 하단 3열 |
| 11 | Key Elements of BS | 가로 그룹막대 + 콜아웃 |
| 12 | Cash Flow | 워터폴 + `.cf-cards`(흰 패널+섀도우) |
| 13 | Cash & Crypto Projection | 세로 스택막대 + 손익 추이 |

> 페이지 순서·개수는 데이터에 따라 바뀔 수 있다. 정확한 현행 목록은 구현체 HTML의 `.slide` 순서를 따른다.


## 7. 빌드 · 검증 · 내보내기 파이프라인


- **작업 원본**: `output/실적보고 v2(디자인가이드 적용).html` 단일 파일을 직접 편집.
- **claude.ai 배포(검토용)**: `<style>`부터 취해 `</head>·<body>·</body>·</html>` 래퍼를 제거한 뒤 Artifact로 게시. 같은 파일경로 = 같은 URL로 갱신.
- **PDF 변환 — Chrome 금지, Safari 도구 사용(★ 확정 규칙):**
  ```
  cd scripts
  ./html2pdf_safari "<입력.html>" "<출력.pdf>" <슬라이드수> <슬라이드높이px>
  # 예: ./html2pdf_safari "../output/실적보고 v2(디자인가이드 적용).html" "../output/실적보고 v2 미리보기.pdf" 13 720
  ```
  - 이유: chart-panel의 소프트 섀도우(`0 20px 40px -18px rgba(20,23,31,.18)`)가 Chrome headless PDF에서는 애플 PDFKit 뷰어(Preview·iOS Files·텔레그램)에서 불투명 회색 박스로 깨진다. Safari/WebKit(WKWebView+PDFKit) 도구는 애플 엔진이라 실제 열람 환경과 렌더가 일치한다. WeasyPrint는 box-shadow 미지원+flex 차트 깨짐으로 폐기.
  - 폭 1280 하드코딩. 슬라이드 수·높이만 인자로.
- **크로스플랫폼 PDF(Windows/Linux)**: Safari가 없는 환경에서는 `tools/html2pdf_playwright.py`(headless Chromium)로 각 슬라이드를 2x 래스터화해 PDF로 합친다. `pip install playwright pillow ; python -m playwright install chromium` 후 `python tools/html2pdf_playwright.py <입력> <출력> <슬라이드수> 720`. 섀도우·그라데이션이 이미지에 구워져 모든 뷰어에서 동일하게 나온다(래스터 PDF, 텍스트 선택 불가). Chrome 벡터 `--print-to-pdf` 단독은 애플 PDFKit에서 섀도우가 깨지므로 지양.
- **검증**: 브라우저 렌더가 깨끗해도 PDF 변환 단계 버그가 있을 수 있다. 정렬·오버플로는 페이지별 PDF를 PNG로 래스터화(Quartz, scale 1.5)해 육안 확인하고, 섀도우·그라데이션류는 실제 전달 채널(텔레그램 파일)로 한 번 열어 확정.
- **pptx**: 모든 HTML 수정 확정 후 마지막 단계에 변환(미착수).


## 8. 재현 체크리스트


새 기기·새 달 데이터로 슬라이드를 다시 만들 때:

- [ ] 캔버스 1280×720, `.slide` padding 63/81, 상단 블루바 7px(표지 제외).
- [ ] 색상은 §2 토큰만 사용. 계열 c1→c4 순, 음수는 `#E5484D`.
- [ ] LINE Seed 서브셋 woff를 base64 `@font-face`로 인라인(외부 링크 금지). 새 글리프 추가 시 재서브셋.
- [ ] 이미지(표지 등)는 base64 인라인, 외부 파일 참조 없음.
- [ ] 차트 크기는 §5 값→픽셀 규칙으로 계산, 숫자 라벨은 실제값 표기.
- [ ] chart-panel 소프트 섀도우 유지.
- [ ] PDF는 Safari 도구로만 변환, 텔레그램에서 실물 확인.
