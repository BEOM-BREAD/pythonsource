import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"


res=requests.get(url)
soup=BeautifulSoup(res.text, "html.parser")

#첫 번째 책 하나만 찾기
book = soup.find("article", class_="product_pod")
#book = soup.select("article.product_pod")
#book = soup.find("article.product_pod") #(X) 첫번째 인자값을 태그로 인지

title = book.find("h3").find("a")["title"]   # 속성값 가져오기
price = book.find("p", class_="price_color").text

print("제목:", title)
print("가격:", price)