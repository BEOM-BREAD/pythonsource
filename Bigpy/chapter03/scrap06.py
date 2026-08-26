import sys
import io
import urllib.request
import urllib.parse
from urllib.parse import urlparse

# 내 공인 IP주소를 알려주는 API
API="https://api.ipify.org"

# 딕셔너리
values={
    'format':'json'
}

print('before',values)
params=urllib.parse.urlencode(values) # html -> text
print('after',params)

# 요청
url=API+"?"+params # https://api.ipify.org?format=json
print("요청 url=", url)

# 읽기
data=urllib.request.urlopen(url).read()
text=data.decode("utf-8")
print(text)