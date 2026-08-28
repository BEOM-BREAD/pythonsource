from playwright.sync_api import sync_playwright
from datetime import datetime
import json

def crawl_wichket():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # 기본값이 headless=True 여서 안보임
        page = browser.new_page(viewport={"width" : 1920, "height": 1080}) # 화면크기

        page.goto('https://auth.wishket.com/login')
        page.wait_for_timeout(3000) # 대기 (밀리초 단위, 3초)

        page.fill('input[name="emailOrId"]','you7972')
        page.fill('input[name="password"]','Lilpa7972.')

        login_button_xpath = '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/form/div[3]/button'
        page.click(f'xpath = {login_button_xpath}')

        page.wait_for_timeout(3000)


        page.goto('https://www.wishket.com/mywishket/partners/')
        page.wait_for_timeout(3000)

        registered_projects = page.inner_text('xpath=/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[5]/div[1]/p')
        contracted_projects = page.inner_text('xpath=/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[5]/div[2]/p')
        completed_amount = page.inner_text('xpath=/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[5]/div[3]/p')

        browser.close()

        # 저장할 데이터 정리
        result = {
            "수집일시" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "등록된_프로젝트" : registered_projects,
            "계약한_프로젝트" : contracted_projects,
            "누적_완료_금액" : completed_amount
        }

        # 1) 날짜별로 새 JSON 파일 저장
        today = datetime.now().strftime("%Y-%m-%d")
        save_path = f"C:/source/pythonsource/Bigpy/Py_Scrap/data/wishket_{today}.json"
        with open(save_path, "w", encoding='utf-8') as f:
            json.dump(result,f,ensure_ascii=False, indent=2)

        # 2) 누적 기록용 CSV에도 한 줄 추가
        csv_path = "C:/source/pythonsource/Bigpy/Py_Scrap/data/wishket_history.csv"
        import os
        file_exists = os.path.isfile(csv_path)
        # a : append 추가 -> 기존의 것을 지우거나 덮어 쓰지 않고 누적
        with open(csv_path, "a", encoding='utf-8') as f:
            if not file_exists:
                f.write("수집일시, 등록된프로젝트,계약한프로젝트,누적완료금랙\n")
            f.write(f'{result["수집일시"]}, {registered_projects},{contracted_projects},{completed_amount}\n')

        print(f"저장 완료: {save_path}")
        return result

if __name__ == '__main__':
    crawl_wichket()

    # 배치파일 생성 메모장 사용
    '''
    @echo off
    cd /d C:\source\pythonsource\Bigpy\chapter04
    call C:\source\pythonsource\.venv\Scripts\activate.bat
    python playwright08.py
    '''