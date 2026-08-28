# https://books.toscrape.com/ 에서 첫 페이지에 있는 책 20권의 제목, 가격, 별점을 크롤링하세요

"""
문제 1 (난이도 하) — 정적 페이지 크롤링 & CSV 저장
books.toscrape.com에서 첫 페이지 책 20권의 제목/가격/별점을 크롤링해서
콘솔 출력 + CSV(books_top20.csv) 저장까지 진행하는 정답 코드
"""

import requests
from bs4 import BeautifulSoup
import csv

URL = "https://books.toscrape.com/"


def crawl_books():
    res = requests.get(URL)
    res.raise_for_status()
    res.encoding = res.apparent_encoding

    soup = BeautifulSoup(res.text, "html.parser")
    books = soup.select("article.product_pod")

    results = []

    for i, book in enumerate(books, 1):
        title = book.select_one("h3 a")["title"]
        price = book.select_one("p.price_color").text.strip()
        star_classes = book.select_one("p.star-rating")["class"]
        rating = star_classes[1]

        print(f"{i}. {title} | {price} | 별점: {rating}")

        results.append({
            "순번": i,
            "제목": title,
            "가격": price,
            "별점": rating
        })

    return results


def save_to_csv(results, filename="books_top20.csv"):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["순번", "제목", "가격", "별점"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nCSV 저장 완료: {filename}")


if __name__ == "__main__":
    book_list = crawl_books()
    save_to_csv(book_list)
