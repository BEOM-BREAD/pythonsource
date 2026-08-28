"""
문제 4 (난이도 중) — Playwright로 동적 페이지 무한 스크롤 크롤링
quotes.toscrape.com/scroll (무한 스크롤 연습용 공식 사이트, 로그인 불필요)에서
스크롤을 끝까지 내려 명언(quote) 제목(=텍스트)을 30개 이상 수집,
titles.txt로 저장하는 정답 코드

+ 심화 옵션: 로그인이 필요한 사이트를 크롤링할 경우
  세션(쿠키)을 저장해두고 재사용하는 패턴 예시 코드 별도 포함
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com/scroll"


def crawl_infinite_scroll():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        page.goto(URL)
        page.wait_for_timeout(2000)

        scroll_pause_time = 1500
        last_height = page.evaluate("document.documentElement.scrollHeight")

        while True:
            page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
            page.wait_for_timeout(scroll_pause_time)

            new_height = page.evaluate("document.documentElement.scrollHeight")
            print(f"이전 높이: {last_height}, 현재 높이: {new_height}")

            if new_height == last_height:
                break

            last_height = new_height

        html_content = page.content()
        browser.close()

    return html_content


def extract_titles(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    quote_blocks = soup.select("div.quote span.text")
    titles = [q.text.strip() for q in quote_blocks]
    return titles


def save_titles(titles, filename="titles.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for title in titles:
            f.write(title + "\n")
    print(f"\n총 {len(titles)}개 수집 완료 → {filename} 저장")


if __name__ == "__main__":
    html = crawl_infinite_scroll()
    titles = extract_titles(html)

    print(f"\n=== 수집된 명언 {len(titles)}개 ===")
    for i, t in enumerate(titles, 1):
        print(f"{i}. {t}")

    save_titles(titles)


def save_login_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("로그인_페이지_URL")

        input("브라우저에서 직접 로그인 완료 후 여기서 엔터를 눌러주세요...")

        page.context.storage_state(path="session.json")
        print("세션 저장 완료: session.json")
        browser.close()


def crawl_with_saved_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="session.json")
        page = context.new_page()

        page.goto("크롤링할_로그인_후_페이지_URL")
        page.wait_for_timeout(3000)

        browser.close()
