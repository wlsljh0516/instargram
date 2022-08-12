from selenium import webdriver
from selenium.webdriver.common.by import By
import re, time, random, sqlite3, clipboard
from selenium.webdriver.common.keys import Keys
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
# 필요한 정보 입력 요청 (인스타 ID / PW / 태크 / 파일 위치 및 파일명 지장)
# 파일 저장 위치는 D:\\ 권장     # C: 는 용량 부족

#참가자의 리그램만 찾습니다.

instaID = ''
instaPW = ''
DB_name = 'you1105'    # 수정
query_txt = 'ai튜터'
tag1 = '#ai학습'
tag2 = '#ai튜터'
tag3 = '#메타버스'
dday = '2021-10-20'                  # 수정
dd = '1103'                         # 수정
cnt = 200                            # 수정

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
f = open("C:/workspace/통합문서1.txt", 'r')
string = f.read()

# 데이터베이스 연결
conn = sqlite3.connect('C:\workspace/'+DB_name+'.db', isolation_level=None)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS ' + DB_name + ' (ID text, wluckname text, content, url text, tag1 text, tag2 text, tag3 text, hashtag text, follower text, likes text, wdate text, tags text);')
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

    # 인스타 이름 추출
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

    #참가자 명단으로 참가자 유무 검사
    try:
        #명단을 불러와 아이디 검색
        wlist = re.search(str(nickname), string)
        if wlist == None:
            wluckname = "미참가자"
            print(wluckname)
        else:
            wluckname = "참가자"
            print(wluckname)
    except Exception as e:
        wID = 'error'
        wurl = 'error'
        print('참가자 이름 error > ', e)
        break

    # 참가자가 아니면 데이터베이스에 저장하지 않음
    if wlist != None:

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


            if wwdate >= dday:        
            # if wwdate == wwdate:

                # 단순 리그램 - 못잡음
                regram = 'X'

                # 인스타 게시글 추출
                try:
                    content = driver.find_element(By.CLASS_NAME, 'C4VMK').text
                except Exception as e:
                    content = []
                    print('인스타 게시글 error > ', e)
                    break


                # '#'해시태그 추출
                try:
                    hashtag = re.findall('#[A-Za-z0-9가-힣]+', content)
                    # hashtag = driver.find_elements(By.CLASS_NAME, 'xil3i')
                    for i in range(len(hashtag)):
                        # wtags = wtags + hashtag[i].text
                        wtags = re.sub('#', '', ', '.join(hashtag))
                    if tag1 in wtags:
                        wtag1 = '○'
                    else:
                        wtag1 = 'X'
                    if tag2 in wtags:
                        wtag2 = '○'
                    else:
                        wtag2 = 'X'
                    if tag3 in wtags:
                        wtag3 = '○'
                    else:
                        wtag3 = 'X'
                    # if '#kyowonedu_official' in hashtag:
                    #     whashtag = '△'
                    print(wtag1 + " " + wtag2 + " " + wtag3)
                except Exception as e:
                    wtag1 = 'error'
                    wtag2 = 'error'
                    whashtag = 'error'
                    print("'#'해시태그 error > ", e)
                    break

                # '@'태그 추출
                try:
                    hashtag = driver.find_elements(By.CLASS_NAME, 'notranslate')
                    for i in range(len(hashtag)):
                        wtags = wtags + hashtag[i].text
                    if '@kyowonedu_official' in wtags:
                        whashtag = '○'
                    elif '#kyowonedu_official' in wtags:
                        whashtag = '△'
                    # elif ((re.search('#kyowonedu_official', content)).group()) == None or ((re.search('@kyowonedu_official', content)).group()) == None:
                    else:
                        whashtag = 'X'
                    print("@kyowonedu_official : " + whashtag)
                except Exception as e:
                    whashtag = 'error'
                    print("'@'태그 error > ", e)
                    break

                time.sleep(random.uniform(2,4))

                # if wtag2 == wtag2:
                if wtag2 == '○':

                    # 좋아요 클릭
                    # try:
                    #     driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button').click()
                    #     print('좋아요 클릭')
                    # except Exception as e:
                    #     print('좋아요 클릭 error > ', e)
            
            
                    # 좋아요 수 추출
                    try:
                        # if driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div'):
                        #     like_part = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/span').text
                        #     if like_part.endswith == '회':     # '조회@회'가 뜨는 좋아요 수..에러
                        #         driver.find_element(By.CLASS_NAME, 'vcOH2').click()
                        #         like = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/div[4]/span').text
                        #         like = int(''.join(like.split(',')))
                        #         wlike = like
                        #     else:
                        #         like = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div[2]/a/span').text
                        #         like = int(''.join(like.split(','))) + 1
                        #         wlike = like
                        # if driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a'):
                        #     like_part = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a').text
                        #     if like_part.startswith == '좋아요':
                        #         like = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a/span').text
                        #         like = int(''.join(like.split(',')))
                        #         wlike = like
                        # wlike = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/article/div/div[2]/div/div[2]/section[2]/div/div/a/span//*[@attribute="title"]').value
                        try:
                            wlike = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/a/span').text
                        except Exception as e:
                            wlike = "0"
                        print("좋아요 수: " + wlike)
                    except Exception as e:
                        wlike = 'error'
                        print('좋아요 수 error > ', e)
                        break
            
            
                    # 사용자 홈 접속
                    driver.execute_script('window.open("https://www.instagram.com/' + nickname + '")')
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(random.uniform(3,5))
            
                    # 팔로워 수 저장      # print(follower.get_attribute('title'))
                    try:
                        # follower = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
                        # follower = int(''.join(follower.get_attribute('title').split(',')))
                        follower = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/section/main/div/header/section/ul/li[2]/a/span').get_attribute("title")
                        wfollower = follower
                        print("팔로워 수 : " + wfollower)
                    except Exception as e:
                        wfollower = 'error'
                        print('팔로워 수 error > ', e)
            
                    # 열었던 창 닫기
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(random.uniform(2,4))

                try:
                    cur.execute(
                        'INSERT INTO ' + DB_name + ' (ID, wluckname, content, url, tag1, tag2, tag3, hashtag, follower, likes, wdate, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                        (wID, wluckname, content, wurl, wtag1, wtag2, wtag3, whashtag, wfollower, wlike, wwdate, wtags))
                    conn.commit()
                    print('INSERT SUCCESS')
                except Exception as e:
                    print('INSERT error > ', e)
                    break
            else:
                print('skip')
        else:
            print("value already exists in DB")
    # 다음 게시물로 이동    #bool(next_btn) 이 false면 반복문 stop
    else:
        print("skip2")
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
conn.close()