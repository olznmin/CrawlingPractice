# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time 
from selenium.webdriver.common.by import By
import json
# 크롬 드라이버 자동 업데이트을 위한 모듈
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json 
import codecs

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# 불필요한 에러 메시지 삭제
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 드라이버 최신 버전 설정
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

# 터미널에서 URL 입력 받기
url = input("웹 페이지 URL을 입력하세요: ")
# https://smartstore.naver.com/nande/products/477282453

# 웹페이지 해당 주소 이동
browser.get(url)

#페이지 로딩을 위한 대기 시간 설정
time.sleep(5)

# 페이지 소스코드 가져오기
html = browser.page_source

# JSON 데이터 추출을 위한 JavaScript 실행
json_data = browser.execute_script("return JSON.stringify(window.__PRELOADED_STATE__)")

# JSON 데이터가 있는지 확인
if json_data:
    # JSON 데이터 파싱
    parsed_json = json.loads(json_data)

    with codecs.open('output.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_json, file, indent=4, ensure_ascii=False)

    print("JSON 파일이 성공적으로 저장되었습니다.")

with open('output.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 상품정보 데이터
name_extracted_data=""

name_data = data['product']['A']
name_target_key='name'
if name_target_key in name_data:
    name_extracted_data = name_data[name_target_key]
    print(name_extracted_data)
    

# 가격 데이터 
price_extracted_data=""                                

price_data= data['product']['A']['benefitsView']
target_key ='discountedSalePrice'
if target_key in price_data:
    price_extracted_data = price_data[target_key]
    print(price_extracted_data)

#이미지 데이터
image_extracted_data=""
image_data= data['product']['A']['productImages'][0]
image_target_key= 'url'
if image_target_key in image_data:
    image_extracted_data= image_data[image_target_key]
    print(image_extracted_data)

#상품 옵션 데이터
optionCombinations_data = data['product']['A']['optionCombinations']
print(optionCombinations_data)

#추가상품 데이터 
supplementProducts_data = data['product']['A'].get('supplementProducts', "null")
print(supplementProducts_data)


# 추출된 데이터 저장
extracted_data = [
    {
        "product_title": name_extracted_data,
        "price": price_extracted_data,
        "image": image_extracted_data,
        "option": supplementProducts_data,
        "optionCombinataions": optionCombinations_data
    }
]

# JSON 파일로 저장
with codecs.open('extracted_data.json', 'w', encoding='utf-8') as file:
    json.dump(extracted_data, file, indent=4, ensure_ascii=False)

print("추출된 데이터가 성공적으로 저장되었습니다.")


browser.close()

