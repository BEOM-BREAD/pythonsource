import sys
import io
import urllib.request
import urllib.parse
from urllib.parse import urlparse # url 파싱

API="https://www.mois.go.kr/gpms/view/jsp/rss/rss.jsp"

# ?ctxCd=1012

# 딕셔너리
values={
    'ctxCd':'1012'
}

print('before',values)
params=urllib.parse.urlencode(values) # html -> text
print('after',params)

# 요청
url=API+"?"+params # https://www.mois.go.kr/gpms/view/jsp/rss/rss.jsp?ctxCd=1012
print("요청 url=", url)

# 읽기
data=urllib.request.urlopen(url).read()
text=data.decode("utf-8")
print(text)

