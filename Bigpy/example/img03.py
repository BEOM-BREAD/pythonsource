from playwright.sync_api import sync_playwright
import os
import requests

savePath = "C:/source/pythonsource/Bigpy/Py_Scrap/img/"
os.makedirs(savePath, exist_ok=True) # 폴더가 없으면 만들어 그리고 있으면 통과

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://search.naver.com/search.naver?where=image&sm=tab_jum&query=강아지")
    page.wait_for_timeout(2000)

    imgs = page.query_selector_all("img")
    print("찾은 img 개수: ", len(imgs))

    # 먼저 url만 뽑아서 리스트에 저장
    img_urls = []
    for img in imgs:
        src = img.get_attribute("src")
        if src and src.startswith("http"):
            img_urls.append(src)

    browser.close()
print(f"수집된 이미지 URL: {len(img_urls)}개")

# requests로 하나씩 실제 다운로드
count = 0
for url in img_urls[:20]:
    count += 1
    try:
        img_data = requests.get(url, timeout = 5).content
        fullfilename = os.path.join(savePath, f"{count}.jpg")
        with open(fullfilename,"w") as f:
            f.write(img_data)
        print(f"{count}.jpg 저장 완료")
    except Exception as e:
        print(f"{count}번 이미지 다운로드 실패")

print("다운로드 완료")