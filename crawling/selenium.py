from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# Selenium WebDriver 설정
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# 대상 URL로 이동
url = 'https://new.land.naver.com/houses?ms=37.3595704,127.105399,16&a=VL&e=RETAIL'
driver.get(url)

# 웹 페이지가 로드될 때까지 잠시 대기
time.sleep(5)  # 로딩 시간에 따라 조절

# BeautifulSoup 객체 생성
soup = BeautifulSoup(driver.page_source, 'html.parser')

soup.findAll

# 필요한 데이터 추출
# 예: soup.find_all(...) 등을 사용

# WebDriver 종료
driver.quit()
