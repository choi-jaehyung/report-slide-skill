#!/usr/bin/env python3
"""
크로스플랫폼 HTML → PDF 변환 (Windows / Linux / macOS 공통).

macOS 전용 `html2pdf_safari` 대신 어느 OS에서도 동작하는 폴백.
headless Chromium(Playwright)으로 슬라이드를 고해상도(2x) 래스터화한 뒤 PDF로 합친다.
각 슬라이드를 이미지로 구워 넣으므로 브라우저 렌더와 픽셀 단위로 동일하며,
chart-panel 소프트 섀도우도 이미지에 포함되어 어떤 PDF 뷰어에서도 깨지지 않는다
(Chrome의 벡터 print-to-pdf에서 발생하던 애플 PDFKit 섀도우 깨짐 이슈를 원천 회피).

설치(최초 1회):
    pip install playwright pillow
    python -m playwright install chromium

사용법:
    python html2pdf_playwright.py "<입력.html>" "<출력.pdf>" <슬라이드수> <슬라이드높이px>
예:
    python html2pdf_playwright.py "../output/실적보고 v2(디자인가이드 적용).html" "out.pdf" 13 720

주의:
- 슬라이드 폭은 1280px 고정(디자인 가이드 기준). 슬라이드는 세로로 정확히 <height>px씩
  쌓여 있다고 가정한다(.slide{height:<height>px}). 개수·높이만 인자로 넘긴다.
- 결과는 래스터 PDF(텍스트 선택 불가). 시각적 재현이 목적이므로 의도된 트레이드오프.
"""
import sys, io
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

WIDTH = 1280
SCALE = 2  # device_scale_factor: 2x 고해상도

def main():
    if len(sys.argv) != 5:
        print(__doc__); sys.exit(1)
    inp, out, slides, height = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": height},
                                device_scale_factor=SCALE)
        page.emulate_media(media="screen")  # print이 아닌 화면 렌더로(섀도우/그라데이션 그대로)
        page.goto(Path(inp).resolve().as_uri())
        page.wait_for_timeout(600)  # 폰트/레이아웃 안정화
        shot = page.screenshot(full_page=True)
        browser.close()

    full = Image.open(io.BytesIO(shot)).convert("RGB")
    pages = []
    for i in range(slides):
        top = i * height * SCALE
        pages.append(full.crop((0, top, WIDTH * SCALE, top + height * SCALE)))
    pages[0].save(out, save_all=True, append_images=pages[1:], resolution=144.0)
    print(f"wrote {out} ({len(pages)} pages, {WIDTH*SCALE}x{height*SCALE}px each)")

if __name__ == "__main__":
    main()
