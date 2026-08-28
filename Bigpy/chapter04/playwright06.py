from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto('https://google.com')
    page.screenshot(path="C:\source\pythonsource\Bigpy\Py_Scrap\img\Web1.png")

    page.goto('https://daum.net')
    page.screenshot(path="C:\source\pythonsource\Bigpy\Py_Scrap\img\Web2.png")

    browser.close()

print('스크린샷 성공')