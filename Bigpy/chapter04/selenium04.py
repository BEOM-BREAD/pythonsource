from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

chrome_options = Options()

s = Service(r"C:\source\pythonsource\Bigpy\Py_Scrap\chromedriver\chromedriver.exe")

driver = webdriver.Chrome(service=s, options=chrome_options)

driver.get('https://google.com')
driver.save_screenshot(r"C:\source\pythonsource\Bigpy\Py_Scrap\img\website3.png")

driver.get('https://daum.net')
driver.save_screenshot(r"C:\source\pythonsource\Bigpy\Py_Scrap\img\website4.png")

driver.quit()

print("스크린샷 성공")