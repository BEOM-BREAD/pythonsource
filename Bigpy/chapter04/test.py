from selenium import webdriver
from selenium.webdriver.chrome.service import Service # 경로 설정
from selenium.webdriver.chrome.options import Options # head 설정 (예: headless)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re
# pip install selenium


# Chrome WebDriver 경로 설정
chrome_driver_path = "C:/source/pythonsource/Bigpy/Py_Scrap/chromedriver/chromedriver.exe"


# Selenium WebDriver 설정
chrome_options = Options()
chrome_options.add_argument("--headless") # 브라우저 창을 띄우지 않음(백그라운드에서 실행)
chrome_options.add_argument("--disable-gpu") # GPU 가속 끔
chrome_options.add_argument("--no-sandbox") # 보안 샌드박스 끔
chrome_options.add_argument("--disable-dev-shm-usage") # 메모리 문제 방지

# 버젼 147부터 직접적인 드라이버 실행
chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"

# WebDriver 실행
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 영화 검색 페이지 열기
    search_query = "말할 수 없는 비밀 영화"
    search_url = f"https://search.naver.com/search.naver?query={search_query}"
    driver.get(search_url)

    # 페이지 로딩 대기
    wait = WebDriverWait(driver, 10) # 최대 10초 동안 기다림
    time.sleep(3) # 페이지가 모두 load 될때까지 3초기다림

    # 영화 정보를 담을 딕셔너리
    movie_info = {}

    
    title = "제목을 찾을 수 없음"
    # 전체 텍스트 가져오기 <body> </body>
    body_text = driver.find_element(By.TAG_NAME, "body").text 
    lines = body_text.split('\n') # 엔터를 기준으로 쪼개기 

    for line in lines:
        line = line.strip()
        # 검색어 키워드가 포함된 짧은 라인 = 제목
        if "말할 수 없는 비밀" in line and len(line) < 20: # 길이가 20자 미만
            title = line
            break

    print(f"영화 제목: {title}")

    # 영화 세부 정보 가져오기
    info_data = {}
    
    # 개봉일, 등급, 장르, 국가, 러닝타임 등의 정보를 찾기
    info_selectors = [
        ".info_group",
        ".movie_info",
        ".detail_info",
        ".sub_info",
        ".cs_common_module .detail_info"
    ]
    
    for selector in info_selectors:
        try:
            info_elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in info_elements:
                text = element.text.strip() # 앞뒤 공백/줄바꿈 제거 
                if text:
                    # 개봉일 추출
                    if "개봉" in text or "2025" in text:
                        lines = text.split('\n')
                        for i, line in enumerate(lines):
                            if "개봉" in line and i + 1 < len(lines):
                                info_data["개봉"] = lines[i + 1]
                    
                    # 등급 추출
                    if "등급" in text or "전체" in text or "12세" in text or "15세" in text:
                        lines = text.split('\n')
                        for i, line in enumerate(lines):
                            if "등급" in line and i + 1 < len(lines):
                                info_data["등급"] = lines[i + 1]
                    
                    # 장르 추출
                    if "장르" in text or "판타지" in text or "멜로" in text:
                        lines = text.split('\n')
                        for i, line in enumerate(lines):
                            if "장르" in line and i + 1 < len(lines):
                                info_data["장르"] = lines[i + 1]
                    
                    # 국가 추출
                    if "국가" in text or "대한민국" in text:
                        lines = text.split('\n')
                        for i, line in enumerate(lines):
                            if "국가" in line and i + 1 < len(lines):
                                info_data["국가"] = lines[i + 1]
                    
                    # 러닝타임 추출
                    if "러닝타임" in text or "분" in text:
                        lines = text.split('\n')
                        for i, line in enumerate(lines):
                            if "러닝타임" in line and i + 1 < len(lines):
                                info_data["러닝타임"] = lines[i + 1]
        except:
            continue

    # 소개/줄거리 가져오기
    story_selectors = [
        ".story",
        ".movie_story",
        ".desc",
        ".summary",
        ".cs_common_module .desc"
    ]
    
    story = ""
    for selector in story_selectors:
        try:
            story_element = driver.find_element(By.CSS_SELECTOR, selector)
            story = story_element.text.strip()
            if story:
                break
        except:
            continue

    # 결과 출력
    print(f"영화 제목: {title}")
    
    # 수집된 정보 출력
    for key, value in info_data.items():
        print(f"{key}: {value}")
    
    if story:
        print(f"\n**소개**\n{story}")

    # 정규표현식으로 한글/영문/숫자 외 특수문자 공백 제거하여 파일명 생성
    filename = re.sub(r'[^a-zA-Z0-9가-힣]', '', title)

    # 영화 정보를 파일로 저장
    file_path = os.path.join(os.getcwd(), f"{filename}.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"영화 제목: {title}\n\n")
        
        # 영화 정보 작성
        for key, value in info_data.items():
            file.write(f"{key}\n{value}\n")
        
        # 소개 작성
        if story:
            file.write(f"\n**소개**\n{story}\n")

    print(f"\n파일 저장 완료: {file_path}")

    # 디버깅용: 페이지 소스의 일부를 확인해보기
    print("\n--- 디버깅 정보 ---")
    try:
        # 페이지에서 찾을 수 있는 모든 텍스트 중 영화 관련 정보 출력
        all_text = driver.find_element(By.TAG_NAME, "body").text
        lines = all_text.split('\n')
        
        relevant_lines = []
        keywords = ['개봉', '등급', '장르', '국가', '러닝타임', '배급', '감독', '출연']
        
        for line in lines:
            line = line.strip()
            if any(keyword in line for keyword in keywords) and line:
                relevant_lines.append(line)
        
        print("페이지에서 찾은 관련 정보:")
        for line in relevant_lines[:20]:  # 처음 20개만 출력
            print(f"- {line}")
            
    except Exception as e:
        print(f"디버깅 정보 수집 중 오류: {e}")

finally:
    # WebDriver 종료
    driver.quit()