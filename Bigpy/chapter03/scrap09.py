import urllib.request
from bs4 import BeautifulSoup

url = "http://www.encar.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36"
}

req = urllib.request.Request(url, headers=headers)
mem = urllib.request.urlopen(req)

encoding = mem.info().get_content_charset() or 'utf-8'
html = mem.read().decode(encoding, errors='ignore')

soup = BeautifulSoup(html, "html.parser")
print(soup)

# 1. title 태그에서 텍스트 가져오기
title = soup.select_one("title")
#print("title :", title)
print("title :", title.text) # 자식 텍스트가 여러개일 경우 합침
#print("title :", title.string) # 자식 텍스트 하나일경우 사용 -> 내차팔기·내차사기 | None

# 2. 속성값을 활용하여 텍스트 가져오기 (meta name="description")
description=soup.select_one('meta[name="description"]')
print("description : ",description.get("content") if description else "없음")

keywords = soup.select_one('meta[name="keywords"]')
print("keywords :", keywords.get("content") if keywords else "없음")

naver_verify = soup.select_one('meta[name="naver-site-verification"]')
print("naver-site-verification :", naver_verify.get("content") if naver_verify else "없음")