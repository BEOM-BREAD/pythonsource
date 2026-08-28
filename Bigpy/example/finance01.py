from bs4 import BeautifulSoup
import urllib.request as req
import requests

# 주식 요청 url
url = "http://finance.naver.com/sise/"

# 요청
print(requests.get(url).encoding) #euc-kr
res = req.urlopen(url).read().decode('euc-kr')
print('res',res)

soup = BeautifulSoup(res, 'html.parser')
popular_list = soup.select("#popularItemList > li")

print("인기 검색 종목")
for item in popular_list:
    rank = item.find('em').text.strip()
    title = item.find('a').text.strip()
    print(f"{rank} {title}")