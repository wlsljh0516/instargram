from logging import error
from selenium import webdriver
from selenium.webdriver.common.by import By
import re, time, random, sqlite3, clipboard
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pprint import pprint 
 
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
# 필요한 정보 입력 요청 (인스타 ID / PW / 태크 / 파일 위치 및 파일명 지장)
# 파일 저장 위치는 D:\\ 권장     # C: 는 용량 부족

# DM을 보내는 프로그램입니다. DM아이디.txt와 DM메시지.txt를 수정해주세요.

instaID = '' #아이디입니다.
instaPW = '' #비번입니다.
DB_name = 'you1125'    # 수정

# webdriver 객체 생성       # 크롬 버전과 동일한 chromedriver설치
driver = webdriver.Chrome(executable_path='C:\workspace/chromedriver.exe')
driver.implicitly_wait(5)

# 웹 사이트 접속 (인스타그램 로그인)
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

# DM보낼 아이디 열기
f = open("C:/workspace/DM아이디.txt", 'r')
string = f.read()

# DM메시지 열기
fcontent = open("C:/workspace/DM게시글.txt", 'r', encoding='UTF8')
strcontent = fcontent.read()

# 데이터베이스 연결
conn = sqlite3.connect('C:\workspace/'+DB_name+'.db', isolation_level=None)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS ' + DB_name + ' ( ID text, content text);')
conn.commit()
print("DB connection successful")



# a = string.split(',') # split함수를 사용해 ',' 기준으로 나눕니다.
a = string.split('\n') # split함수를 사용해 '\n' 기준으로 나눕니다.

# print(a)
i = 0
b = len(a)
print(b)

# DM보낼 아이디 수 만큼 반복
string = str(string)
while i < b:
    try:
        wID = a[i]
        iint = i + 1
        iint = str(iint)
        print(iint)
        wID = str(wID)
        print(wID)
        d = re.search((wID), string)

        # 웹 사이트 접속 (해시태그 검색)
        time.sleep(random.uniform(2,3))
        driver.get('https://www.instagram.com/' + wID + '/')
        time.sleep(1)
        i += 1
    except Exception as e:
        d = 'error'
        i = 'error'
        print('반복 error > ', e)
        break

    # 팔로우&메시지 보내기 버튼 클릭
    try:
        driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div/button').click()
        time.sleep(1)
        print('팔로우&메시지 보내기 버튼을 클릭했습니다.')
    except Exception as e:
        print('클릭 error > ', e)
        break

    # 팔로우가 되어 있지 않으면 메시지 보내기 클릭
    try:
        driver.find_element_by_css_selector('#react-root > section > main > div > header > section > div.nZSzR > div.qF0y9.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm.bPdm3 > div > div > button').click()
        time.sleep(1)
        print('메시지 보내기를 클릭했습니다.')
    except:
        print('메시지 보내기 버튼이 이미 클릭이 되었습니다.')
    
    #팝업창 닫기
    try:
        driver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm').click()
        time.sleep(1)
        print('다음에하기 누르기')
    except:
        print('다음에하기 누르기가 없습니다. ')
    
    #DM메시지 넣기
    try:
        clipboard.copy(strcontent) # 복사하기
        strcontent = clipboard.paste() #send_key()메소드 매개변수는 이모티콘이 포함된 문장있으면 에러
        dm = driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea').send_keys(strcontent)
        dm.send_keys(Keys.CONTROL,'v') #붙여넣기
        print('DM 내용넣기')

    except Exception as e:
        print('DM메시지 넣기 error > ', e)
        break

    #DM메시지 보네기
    try: 
        driver.find_element_by_css_selector('#react-root > section > div > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm > div > div > div.DPiy6.qF0y9.Igw0E.IwRSH.eGOV_.vwCYk > div.uueGX > div > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm > div > div > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.JI_ht > button').click()
        print('DM 내용보내기')

    except Exception as e:
        print('DM메시지 보네기 error > ', e)
        break



    #db 저장
    try:
        cur.execute(
            'INSERT INTO ' + DB_name + ' ( ID, content) VALUES (?,?);',
            ( wID, strcontent ))
        conn.commit()
        print('INSERT SUCCESS')
    except Exception as e:
        print('INSERT error > ', e)
        break
print("DM 보내기가 끝났습니다.")
f.close()
fcontent.close()
conn.close()