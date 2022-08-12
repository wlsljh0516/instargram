from selenium import webdriver
import time, random, sqlite3, clipboard
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pprint import pprint
from openpyxl import Workbook
import pandas as pd

# 게시글을 모든 댓글을 가지고와 엑셀에 저장합니다. 순서는 랜덤입니다. 

DB_name = 'you1129_댓글추츨'
url = 'CWsgY9VswAY'
instaID = ''
instaPW = ''

# webdriver 객체 생성       # 크롬 버전과 동일한 chromedriver설치
driver = webdriver.Chrome()
driver.get("https://www.instagram.com/")
driver.implicitly_wait(3)

# 웹 사이트 접속 (인스타그램 로그인)
time.sleep(random.uniform(3,6))
driver.get('https://www.instagram.com/accounts/login/')

# 로그인 정보 입력
clipboard.copy(instaID) # 복사하기
instaID = clipboard.paste()
id_dr = driver.find_element_by_name('username')
id_dr.send_keys(Keys.CONTROL,'v') #붙여넣기

clipboard.copy(instaPW) # 복사하기
instaPW = clipboard.paste()
ps_dr = driver.find_element_by_name('password')
ps_dr.send_keys(Keys.CONTROL,'v')#붙여넣기
clipboard.copy('.')# 비번없에기

driver.find_element_by_xpath(
    '//*[@id="loginForm"]/div/div[3]/button').submit()
time.sleep(random.uniform(3,6))

# 웹 사이트 접속 (해시태그 검색) 
driver.get('https://www.instagram.com/p/' + url + '/')
time.sleep(random.uniform(7,10))

# 데이터베이스 연결
conn = sqlite3.connect('C:\workspace/'+DB_name+'.db', isolation_level=None)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS ' + DB_name + ' (ID text, content text);')
conn.commit()
print("DB connection successful")

# 댓글 플러스 버튼 누르기
while True:
    try:
        # 댓글 플러스 버튼 주소
        button = driver.find_element_by_css_selector('#react-root > div > div > section > main > div > div.ltEKP > article > div > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm > div > div.eo2As > div.EtaWk > ul > li > div > button > div > svg')
    except:
        pass
    
    # None이 아니면 계속 수행
    if button is not None:
        try: # 댓글 플러스 버튼 클릭
            driver.find_element_by_css_selector('#react-root > div > div > section > main > div > div.ltEKP > article > div > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm > div > div.eo2As > div.EtaWk > ul > li > div > button > div > svg').click()
            time.sleep(random.uniform(1,2))
            print('댓글 추가하기')
        except:
            # 댓글이 없으면 while문 빠져나감
            break

# 대댓글 버튼 누르기
# buttons = driver.find_elements_by_css_selector('li > ul > li > div > button')()

# for button in buttons:
#     button.send_keys(Keys.ENTER)

# 댓글 내용 추출
id_f = []
rp_f = []
#아이디 추출
ids  = driver.find_elements_by_css_selector('._6lAjh > .qF0y9 > .Jv7Aj > .sqdOP')
#댓글 추츨
replies = driver.find_elements_by_css_selector('div.C4VMK > span')

# 아이디와 댓글을 data에 넣음
for id, reply in zip(ids, replies): # zip을 통해 ids리스트는 id를 통해 추출되고 replies는 reply를 통해 추출된다.
    id_a = id.text.strip() # 띄어쓰기를 없엠
    id_f.append(id_a) # id 데이터를 넣음

    rp_a = reply.text.strip()
    rp_f.append(rp_a)


    data = {"아이디": id_f,
            "코멘트": rp_f}

df = pd.DataFrame(data)
df.to_excel('result.xlsx')

driver.quit()
conn.close()