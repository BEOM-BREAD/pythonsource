"""
문제 2 (난이도 하) — 공개 API 크롤링 (인증 없음)
Frankfurter API로 USD 기준 KRW/JPY/EUR 환율을 가져와서
콘솔 출력 + JSON(exchange_today.json) 저장까지 진행하는 정답 코드
"""

# https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW,JPY,EUR 를 이용해 달러 기준 원화, 엔화, 유로 환율을 가져오세요.

import requests
import json
from datetime import datetime

URL = "https://api.frankfurter.dev/v1/latest"


def get_exchange_rates():
    params = {
        "base": "USD",
        "symbols": "KRW,JPY,EUR"
    }

    res = requests.get(URL, params=params)
    res.raise_for_status()
    data = res.json()

    rates = data["rates"]
    rate_date = data["date"]

    return rates, rate_date


def main():
    rates, rate_date = get_exchange_rates()

    print(f"=== {rate_date} 기준 환율 (1 USD 기준) ===")
    for currency, value in rates.items():
        print(f"1 USD = {value:.2f} {currency}")

    result = {
        "조회일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "기준환율일자": rate_date,
        "환율": rates
    }

    with open("exchange_today.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\n저장 완료: exchange_today.json")


if __name__ == "__main__":
    main()
