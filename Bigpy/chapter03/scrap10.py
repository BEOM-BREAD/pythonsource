import requests
from bs4 import BeautifulSoup

url = "https://www.melon.com/chart/index.htm"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36"
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# id="tb_list" 테이블 안의 곡 목록 전체 가져오기
songs = soup.select("#tb_list tr")

count = 0
for song in songs:
    rank = song.select_one(".rank")
    title = song.select_one(".ellipsis.rank01 a")  # 곡 제목
    artist = song.select_one(".ellipsis.rank02 a")  # 가수

    if title and artist:
        print(f"{rank.text.strip()}위 | {title.text.strip()} - {artist.text.strip()}")
        count += 1

    if count >= 10:
        break