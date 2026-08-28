"""
문제 3 (난이도 중) — 인증키 필요한 API + 여러 도시 반복 조회
OpenWeatherMap API로 5개 도시의 현재 날씨를 조회하고,
최고/최저 기온 도시를 찾아 출력 + CSV 저장하는 정답 코드

사전 준비:
1. https://openweathermap.org/ 회원가입 → API 키 발급
   (발급 직후 바로 안 되면 활성화까지 몇 분~1시간 걸릴 수 있음)
2. 같은 폴더에 .env 파일 생성:
   OPENWEATHER_API_KEY=발급받은_키
3. 설치: uv pip install python-dotenv requests
"""

# 5개 도시 중 가장 더운 도시와 가장 시원한 도시를 찾아서 출력하세요.


import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

URL = "https://api.openweathermap.org/data/2.5/weather"

CITIES = ["Seoul", "Busan", "Incheon", "Daegu", "Gwangju"]


def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "kr"
    }

    res = requests.get(URL, params=params)

    if res.status_code == 404:
        return None

    res.raise_for_status()
    data = res.json()

    return {
        "도시": city,
        "기온": data["main"]["temp"],
        "날씨": data["weather"][0]["description"]
    }


def main():
    results = []

    print("=== 도시별 현재 날씨 ===")
    for city in CITIES:
        try:
            info = get_weather(city)
        except Exception as e:
            print(f"{city}: 조회 실패 ({e})")
            continue

        if info is None:
            print(f"{city}: 조회 실패 (도시를 찾을 수 없음)")
            continue

        print(f"{info['도시']}: {info['기온']}도, {info['날씨']}")
        results.append(info)

    if not results:
        print("\n조회에 성공한 도시가 없습니다.")
        return

    hottest = max(results, key=lambda x: x["기온"])
    coolest = min(results, key=lambda x: x["기온"])

    print(f"\n가장 더운 도시: {hottest['도시']} ({hottest['기온']}도)")
    print(f"가장 시원한 도시: {coolest['도시']} ({coolest['기온']}도)")

    csv_path = "weather_5cities.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["도시", "기온", "날씨"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nCSV 저장 완료: {csv_path}")


if __name__ == "__main__":
    main()


