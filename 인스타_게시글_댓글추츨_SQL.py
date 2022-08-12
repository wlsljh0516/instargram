from selenium import webdriver
import re, time, random, sqlite3, clipboard
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pprint import pprint

# 게시글을 모든 댓글을 가지고와 SQL에 저장합니다. 순서는 랜덤입니다.

DB_name = 'you1129_댓글추출'
url = 'CWsgY9VswAY' #인스타 주소
instaID = ''
instaPW = ''

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
# buttons = driver.find_elements_by_css_selector('li > ul > li > div > button')

# for button in buttons:
#     button.send_keys(Keys.ENTER)

try:
    # html source 추출
    html_source = driver.page_source
    # BS로 html parsing
    soup = BeautifulSoup(html_source, 'html.parser')
    # 원하는 항목의 데이터만 추출
    #아이디 
    
    products = soup.select('._6lAjh > .qF0y9 > .Jv7Aj > .sqdOP')
    #댓글
    products2 = soup.select('div.C4VMK > span')
    #리스트로 만들기
    listproduct = []
    listproduct2 = []
    #결과 확인
    for product, product2 in zip(products,products2): 
        #products에 있는 아이디만 추출하여 listproduct에 넣음
        listproduct.append(product.get_text()) # .append로 리스트에 추가

        #products2에 있는 게시글 내용만 추출하여 listproduct2에 넣음 .get_text로 내용가지고 옴
        listproduct2.append(product2.get_text()) # .append로 리스트에 추가 .get_text로 내용가지고 옴
    
    #아이디리스트
    pprint(listproduct)
    #게시글리스트
    pprint(listproduct2)

except Exception as e:
    print('리스트 error > ', e)

try:
    #아이디와 게시글을 순서대로 SQLite에 넣음
    i = 0
    while True:
            cur.execute(
            'INSERT INTO ' + DB_name + ' (ID, content) VALUES (?, ?);',
            (listproduct[i], listproduct2[i]))
            i += 1
            conn.commit()
            print('INSERT SUCCESS')
#데이터가 없으면 빠져나감
except:
    print("데이터없음")
driver.quit()
conn.close()