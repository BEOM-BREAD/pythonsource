import sys
import io
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import urllib.request as req
from io import BytesIO
import xlsxwriter

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

workbook = xlsxwriter.Workbook('C:/source/pythonsource/Bigpy/Py_Scrap/data/you_crawl_result.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', '작성자')
worksheet.write('B1', '댓글내용')
worksheet.write('C1', '좋아요')
worksheet.write('D1', '프로필이미지')


def main():
    with sync_playwright() as p:
        # headless=False — 브라우저 창이 화면에 뜸
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--mute-audio",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ]
        )
        page = browser.new_page(viewport={"width": 1920, "height": 1280})

        page.goto('https://www.youtube.com/watch?v=8CHp4j6bbaQ')
        page.wait_for_timeout(5000)

        page.keyboard.press("PageDown")
        page.wait_for_timeout(2000)

        scroll_pause_time = 4000
        last_height = page.evaluate("document.documentElement.scrollHeight")

        while True:
            page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
            page.wait_for_timeout(scroll_pause_time)

            new_height = page.evaluate("document.documentElement.scrollHeight")
            print(f"Last Height: {last_height}, Current Height: {new_height}")

            if new_height == last_height:
                break

            last_height = new_height

        html_content = page.content()
        browser.close()

    soup = BeautifulSoup(html_content, "html.parser")

    comment = soup.select('ytd-comment-view-model#comment')
    print(f"\n총 댓글 수: {len(comment)}개\n")

    ins_cnt = 2

    for dom in comment:
        try:
            img_tag = dom.select_one("#img")
            img_src = img_tag.get('src') if img_tag else None

            author_tag = dom.select_one('#author-text > span')
            author = author_tag.text.strip() if author_tag else '작성자없음'

            content_tag = dom.select_one('#content-text')
            content = content_tag.text.strip() if content_tag else '내용없음'

            posi_tag = dom.select_one('#vote-count-middle')
            posi_cnt = posi_tag.text.strip() if posi_tag else '0'

            print(f"작성자: {author}")
            print(f"댓글: {content}")
            print(f"좋아요: {posi_cnt}")
            print(f"이미지: {img_src if img_src else 'None'}")
            print()

            worksheet.write(f'A{ins_cnt}', author)
            worksheet.write(f'B{ins_cnt}', content)
            worksheet.write(f'C{ins_cnt}', posi_cnt)

            if img_src and img_src.startswith('http'):
                try:
                    request = req.Request(img_src, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                    })
                    img_data = BytesIO(req.urlopen(request, timeout=10).read())

                    worksheet.insert_image(
                        f'D{ins_cnt}', author,
                        {'image_data': img_data, 'x_scale': 0.5, 'y_scale': 0.5}
                    )
                except Exception as e:
                    print(f"이미지 다운로드 실패: {e}")
                    worksheet.write(f'D{ins_cnt}', img_src)
            else:
                worksheet.write(f'D{ins_cnt}', 'None')

            ins_cnt += 1

        except Exception as e:
            print(f"댓글 파싱 오류: {e}")
            continue

    print(f"\n총 {ins_cnt - 2}개 댓글 저장 완료!")

    workbook.close()
    print("엑셀 저장 완료!")


if __name__ == '__main__':
    main()