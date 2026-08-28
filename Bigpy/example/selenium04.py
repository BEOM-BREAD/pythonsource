from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import re

# Chrome WebDriver 경로 설정
chrome_driver_path = "C:/source/pythonsource/Bigpy/Py_Scrap/chromedriver/chromedriver.exe"

# Selenium WebDriver 설정
chrome_options = Options()
chrome_options.add_argument("--headless") # 브라우저 창을 띄우지 않음
chrome_options.add_argument("--disavle-gpu") # GPU 비활성화
chrome_options.add_argument("--no-sandbox") # 보안 비활성화

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 영화 검색 페이지 열기(예: "말할 수 없는 비밀")
    search_query = "말할 수 없는 비밀 영화 평점"
    search_url = f"https://search.naver.com/search.naver?query={search_query}"
    driver.get(search_url)

    time.sleep(3)

    # 영화 제목 가져오기
    try:
        title_element = driver.find_element(By.CLASS_NAME, "title_area")
        title = title_element.text.strip()
    except:
        title = "제목을 찾을 수 없음."

    # 영화 평점 가져오기
    try:
        score_element = driver.find_element(By.CLASS_NAME, "area_star_number")
        score = score_element.text.strip()
    except Exception as e:
        print("평점 추출 에러: ", e)
        score = "평점을 찾을 수 없음."

    # 결과 출력
    print(f"영화 제목: {title}")
    print(f"평점: {score}")

    # 특수문자 제거
    filename = re.sub(r'[^a-zA-Z0-9가-힣]','',title)

    file_path = os.path.join(os.getcwd(), f"{filename}.txt")
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(score)
    print(f"파일 저장 완료: {file_path}")

finally:
    driver.close()