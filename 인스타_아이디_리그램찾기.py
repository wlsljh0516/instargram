from logging import error
from selenium import webdriver
from selenium.webdriver.common.by import By
import re, time, random, sqlite3
from bs4 import BeautifulSoup
from pprint import pprint 
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
# 필요한 정보 입력 요청 (인스타 ID / PW / 태크 / 파일 위치 및 파일명 지장)
# 파일 저장 위치는 D:\\ 권장     # C: 는 용량 부족
instaID = ''
instaPW = ''
DB_name = 'you1110'    # 수정
query_txt = 'ai튜터'
tag1 = '#ai학습'
tag2 = '#ai튜터'
tag3 = '#메타버스'
dday = '2021-10-20'                  # 수정
dd = '1108'                         # 수정
cnt = 200                            # 수정

# webdriver 객체 생성       # 크롬 버전과 동일한 chromedriver설치
driver = webdriver.Chrome(executable_path='C:\workspace/chromedriver.exe')
driver.implicitly_wait(5)

# 웹 사이트 접속 (인스타그램 로그인)
driver.get('https://www.instagram.com/accounts/login/')

# 로그인 정보 입력
driver.find_element_by_name('username').send_keys(instaID)
driver.find_element_by_name('password').send_keys(instaPW)

driver.find_element_by_xpath(
    '//*[@id="loginForm"]/div/div[3]/button').submit()
time.sleep(random.uniform(3,6))

# 당첨자명단 열기
f = open("C:/workspace/아이디.txt", 'r')
string = f.read()
fcontent = open("C:/workspace/게시글.txt", 'r', encoding='UTF8')
strcontent = fcontent.read()
fcontent2 = open("C:/workspace/게시글2.txt", 'r', encoding='UTF8')
strcontent2 = fcontent2.read()
fcontent3 = open("C:/workspace/게시글3.txt", 'r', encoding='UTF8')
strcontent3 = fcontent3.read()
fcontent4= open("C:/workspace/게시글4.txt", 'r', encoding='UTF8')
strcontent4 = fcontent4.read()
# 데이터베이스 연결
conn = sqlite3.connect('C:\workspace/'+DB_name+'.db', isolation_level=None)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS ' + DB_name + ' (iint text,ID text);')
conn.commit()
print("DB connection successful")

a = string.split(',')
# print(a)
i = 0
b = len(a)
print(b)

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
        time.sleep(random.uniform(3,5))
        i += 1
    except Exception as e:
        d = 'error'
        i = 'error'
        print('반복 error > ', e)
        break

    try:
        # 스크롤 높이 가져옴
        last_height = driver.execute_script("return document.body.scrollHeight")
        heightno = 0
        while True:
            # 끝까지 스크롤 다운
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # 2~4초 대기
            time.sleep(random.uniform(3,6))

            # 스크롤 다운 후 스크롤 높이 다시 가져옴
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            heightno += 1
            heightno2 = heightno % 8
            
            if heightno2 == 0:
                try:
                    # html source 추출
                    html_source = driver.page_source
                    # BS로 html parsing
                    soup = BeautifulSoup(html_source, 'html.parser')
                    # 원하는 항목의 데이터만 추출
                    products = soup.select('.KL4Bh')
                    # 제품 이름, 코드 추출
                    content = [product.find('img')['alt'] for product in products]
                    # 게시글 보기
                    # pprint(content)
                except Exception as e:
                    content = 'error'
                    print('인스타 게시글 error > ', e)
                    break
                try:
                    wcontent = re.search(str(strcontent), str(content))
                    print(wcontent)
                    if wcontent == None:
                        wcontent = "게시글 미참가자"
                        print(wcontent)
                    else:
                        wcontent = "게시글 참가자"
                        print(wcontent)
                              
                except Exception as e:
                    print('게시글 구분 error > ', e)
                    break

                try:
                    wcontent2 = re.search(str(strcontent2), str(content))
                    print(wcontent2)
                    if wcontent2 == None:
                        wcontent2 = "게시글 미참가자"
                        print(wcontent2)
                    else:
                        wcontent2 = "게시글 참가자"
                        print(wcontent2)
                              
                except Exception as e:
                    print('게시글 구분2 error > ', e)
                    break

                try:
                    wcontent3 = re.search(str(strcontent3), str(content))
                    print(wcontent3)
                    if wcontent3 == None:
                        wcontent3 = "게시글 미참가자"
                        print(wcontent3)
                    else:
                        wcontent3 = "게시글 참가자"
                        print(wcontent3)
                           
                except Exception as e:
                    print('게시글 구분3 error > ', e)
                    break

                try:
                    wcontent4 = re.search(str(strcontent4), str(content))
                    print(wcontent4)
                    if wcontent4 == None:
                        wcontent4 = "게시글 미참가자"
                        print(wcontent4)
                    else:
                        wcontent4 = "게시글 참가자"
                        print(wcontent4)      
                except Exception as e:
                    print('게시글 구분4 error > ', e)
                    break
                try:
                    if wcontent == "게시글 참가자" or wcontent2 == "게시글 참가자" or wcontent3 == "게시글 참가자" or wcontent4 == "게시글 참가자":
                        print("스크롤 멈춤")
                        break
                except Exception as e:
                    print('스크롤 멈춤 error > ', e)
                    break
                try:
                    if heightno == 16:
                        print("스크롤 16번내림")
                        break
                
                except Exception as e:
                    print('스크롤 멈춤 error > ', e)
                    break



            else:
                print("스크롤 내리기")
            
            
    except Exception as e:
        print('last_height error > ', e)
        break

    

    #db 저장
    try:
        cur.execute(
            'INSERT INTO ' + DB_name + ' (iint, ID) VALUES (?,?);',
            (iint, wID))
        conn.commit()
        print('INSERT SUCCESS')
    except Exception as e:
        print('INSERT error > ', e)
        break
f.close()
fcontent.close()
conn.close()