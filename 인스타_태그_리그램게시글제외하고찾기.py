from selenium import webdriver
from selenium.webdriver.common.by import By
import re, time, random, sqlite3, clipboard
# pip install webdriver-manager
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
# 필요한 정보 입력 요청 (인스타 ID / PW / 태크 / 파일 위치 및 파일명 지장)
# 파일 저장 위치는 D:\\ 권장     # C: 는 용량 부족
instaID = ''
instaPW = ''
DB_name = 'you1203'    # 수정
query_txt = '엔칸토아이캔두'
tag1 = '#ai학습'
tag2 = '#ai튜터'
tag3 = '#메타버스'
dday = '2021-11-10'                  # 수정
dd = '1108'                         # 수정
cnt = 56                            # 수정

# 태그를 통해 지정된 리그램을 제외하고 찾습니다.

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

# 태그 입력 
driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input""").send_keys(query_txt)

# 웹 사이트 접속 (해시태그 검색)
driver.get('https://www.instagram.com/explore/tags/' + query_txt + '/')
time.sleep(random.uniform(7,10))

# 당첨자명단 열기
f = open("C:/workspace/아이디.txt", 'r')
string = f.read()
fcontent = open("C:/workspace/엔칸토아이캔두.txt", 'r', encoding='UTF8')
strcontent = fcontent.read()
# 데이터베이스 연결
conn = sqlite3.connect('C:\workspace/'+DB_name+'.db', isolation_level=None)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS ' + DB_name + ' (ID text, content text, url text, wcontent text, follower text, likes text, wdate text);')
conn.commit()
print("DB connection successful")

# 해당 태그의 게시물 수 얻어오기
# search_cnt = int(''.join((driver.find_element(By.CLASS_NAME, 'g47SY').text).split(',')))

# 게시물 열기
# url = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/section/main/article/div[1]/div/div/div[1]/div[1]/a')
url = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]')

url.click()
time.sleep(random.uniform(4,8))

# 페이지 이동하면서 데이터 추출

no = 1

next_con = True

while next_con == True and no <= cnt:

    wID = ''
    wContent = ''
    wfollower = ''
    wlike = ''

    print('\n' + '-' * 10 + str(no) + '-' * 10)

    # 인스타 이름 추출 sqdOP yWX7d     _8A5w5   ZIAjV 
    try:
        nickname = driver.find_element(By.CSS_SELECTOR, 'a.sqdOP.yWX7d._8A5w5.ZIAjV').text
        wID = nickname
        print(wID)
        url = str(driver.current_url)
        wurl = url
        
    except Exception as e:
        wID = 'error'
        wurl = 'error'
        print('인스타 이름 error > ', e)
        break
    # # 참가자와 미 참가자 구분
    # try:
    #     wlist = re.search(str(nickname), string)
    #     if wlist == None:
    #         wluckname = "미참가자"
    #         print(wluckname)
    #     else:
    #         wluckname = "참가자"
    #         print(wluckname)
    # except Exception as e:
    #     wID = 'error'
    #     wurl = 'error'
    #     print('참가자 이름 error > ', e)
    #     break
    
    #참가자이면 저장하고 미 참가자이면 스킵
    # if wlist != None:
    uu = cur.execute("select url from " + DB_name + " where url = '" + wurl + "';").fetchone()
    
    if uu == None:

        # 작성일 추출
        try:
            wdate = driver.find_element(By.CSS_SELECTOR, 'time')
            wdate = '-'.join(re.findall('\d+', wdate.get_attribute('title')))
            wwdate = wdate
            print(wwdate)
        except Exception as e:
            wwdate = 'error'
            print('작성일 error > ', e)
            break


        # if wwdate == dday:        
        if wwdate == wwdate:

            # 단순 리그램 - 못잡음
            regram = 'X'

            # 인스타 게시글 추출 및 게시글 참가자와 미 참가자 구분
            try:
                content = driver.find_element(By.CLASS_NAME, 'C4VMK').text
            except Exception as e:
                content = []
                print('인스타 게시글 error > ', e)
                break

            try:
                wcontent = re.search(str(strcontent), str(content))
                print(wcontent)
                if wcontent == None:
                    print("미참가자")
                else:
                    wcontent = "게시글 참가자"
                    print(wcontent)      
            except Exception as e:
                print('게시글 구분 error > ', e)
                break
            


            if wcontent == None:
                try: #데이터 베이스 저장
                    cur.execute(
                        'INSERT INTO ' + DB_name + ' (ID, content, url, wcontent, follower, likes, wdate) VALUES (?, ?, ?, ?, ?, ?, ?);',
                        (wID, content, wurl, wcontent, wfollower, wlike, wwdate))
                    conn.commit()
                    print('INSERT SUCCESS')
                except Exception as e:
                    print('INSERT error > ', e)
                    break
            else:
                print('스킵')
        else:
            print('skip')
    else:
        print("value already exists in DB")
    
    # else:
    #     print("skip2")

    # 다음 게시물로 이동    #bool(next_btn) 이 false면 반복문 stop
    try:
        if no == 1:           
            next_btn = driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div/div/button')
            next_btn.click()
        else:
            next_btn = driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div/div[2]/button')
            next_btn.click()
            time.sleep(random.uniform(2,5))
        no += 1
    except Exception as e:
        print('다음 게시물 이동 error > ', e)
        conn.close()
        break
f.close()
fcontent.close()
conn.close()