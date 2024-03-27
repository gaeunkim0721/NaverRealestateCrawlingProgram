import requests
from bs4 import BeautifulSoup
import json
import math
import random
import time

# User-Agent 리스트
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36 Edge/88.0.705.50"
]
proxies_list = [
    {"http": "http://72.10.160.91:13403", "https": "http://72.10.160.91:13403"},
    {"http": "http://72.10.164.178:23241", "https": "http://72.10.164.178:23241"},
    {"http": "http://117.74.65.207:54466", "https": "http://117.74.65.207:54466"},
    {"http": "http://8.213.128.6:8889", "https": "http://8.213.128.6:8889"},
    {"http": "http://72.10.160.90:15727", "https": "http://72.10.160.90:15727"},
    {"http": "http://43.156.0.125:8888", "https": "http://43.156.0.125:8888"},
    {"http": "http://162.223.94.164:80", "https": "http://162.223.94.164:80"},
    {"http": "http://142.93.49.65:8000", "https": "http://142.93.49.65:8000"},
    {"http": "http://103.231.78.36:80", "https": "http://103.231.78.36:80"},
    {"http": "http://8.213.128.6:20002", "https": "http://8.213.128.6:20002"},
    {"http": "http://8.213.128.6:8118", "https": "http://8.213.128.6:8118"},
    {"http": "http://8.213.129.20:2001", "https": "http://8.213.129.20:2001"},
    {"http": "http://103.49.202.250:80", "https": "http://103.49.202.250:80"},
    {"http": "http://8.213.137.155:503", "https": "http://8.213.137.155:503"},
    {"http": "http://8.213.137.155:8024", "https": "http://8.213.137.155:8024"},
    {"http": "http://138.91.159.185:80", "https": "http://138.91.159.185:80"},
    {"http": "http://191.252.196.14:8889", "https": "http://191.252.196.14:8889"},
    {"http": "http://103.83.232.122:80", "https": "http://103.83.232.122:80"},
    {"http": "http://201.174.38.160:999", "https": "http://201.174.38.160:999"},
    {"http": "http://8.213.137.155:447", "https": "http://8.213.137.155:447"},
    {"http": "http://8.213.129.15:5000", "https": "http://8.213.129.15:5000"},
    {"http": "http://64.56.150.102:3128", "https": "http://64.56.150.102:3128"},
    {"http": "http://41.33.203.234:1975", "https": "http://41.33.203.234:1975"},
    {"http": "http://119.39.68.79:2323", "https": "http://119.39.68.79:2323"},
    {"http": "http://220.178.135.112:8089", "https": "http://220.178.135.112:8089"},
    {"http": "http://3.125.124.192:50664", "https": "http://3.125.124.192:50664"},
]


counttimes = 0

countprints = 0


keyword = "서울"

url = "https://m.land.naver.com/search/result/{}".format(keyword)


selected_proxy = random.choice(proxies_list)

working_proxies = []

for proxy in proxies_list:
    try:
        print(f"프록시 테스트 중: {proxy}")
        # Google 홈페이지에 접근을 시도하여 프록시 작동 여부를 확인합니다.
        response = requests.get("http://www.google.com", proxies=proxy, timeout=5)
        
        # 응답 코드가 200이면 프록시가 작동하는 것으로 간주하고 목록에 추가합니다.
        if response.status_code == 200:
            print(f"작동하는 프록시: {proxy}")
            working_proxies.append(proxy)
    except Exception as e:
        # 요청 실패 시 출력
        print(f"프록시 작동 실패: {proxy}, 오류: {e}")

# 작동하는 프록시 목록 출력
print(f"\n작동하는 프록시 목록: {working_proxies}")



working_user_agents = []

for user_agent in user_agents:
    headers = {
        "User-Agent": user_agent
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"작동하는 User-Agent: {user_agent}")
            working_user_agents.append(user_agent)
        else:
            print(f"차단된 User-Agent: {user_agent}, 상태 코드: {response.status_code}")
    except Exception as e:
        print(f"오류 발생: {user_agent}, 오류 메시지: {str(e)}")

# 작동하는 User-Agent 출력
print("\n작동하는 User-Agent 목록:")
for agent in working_user_agents:
    print(agent)



selected_proxy = random.choice(working_proxies)


# 랜덤하게 1개의 User-Agent 선택
user_agent = random.choice(working_user_agents)


headers={
                "Accept-Encoding": "gzip",
                "X-Requested-With": "XMLHttpRequest",
                "Host": "m.land.naver.com",
                "Referer": "https://m.land.naver.com/map/37.482968:127.0634:14:1168010300/VL/A1",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": user_agent,
                "Accept": "application/json",
            }


try:
    res = requests.get(url ,data={"isOnlyIsale":"false"},proxies=selected_proxy, headers=headers)

    # print(res.text)

    soup = (str)(BeautifulSoup(res.text, "lxml"))

    value = soup.split("filter: {")[1].split("}")[0].replace(" ","").replace("'","")

    lat = value.split("lat:")[1].split(",")[0]
    lon = value.split("lon:")[1].split(",")[0]
    z = value.split("z:")[1].split(",")[0]
    cortarNo = value.split("cortarNo:")[1].split(",")[0]
    #빌라,매매 매물만 선택하기 위해 주석 처리
    # rletTpCds = value.split("rletTpCds:")[1].split(",")[0]
    # tradTpCds = value.split("tradTpCds:")[1].split()[0]

    # lat - btm : 37.550985 - 37.4331698 = 0.1178152
    # top - lat : 37.6686142 - 37.550985 = 0.1176292
    lat_margin = 0.118

    # lon - lft : 126.849534 - 126.7389841 = 0.1105499
    # rgt - lon : 126.9600839 - 126.849534 = 0.1105499
    lon_margin = 0.111
    btm=float(lat)-lat_margin
    lft=float(lon)-lon_margin
    top=float(lat)+lat_margin
    rgt=float(lon)+lon_margin

    # 최초 요청 시 디폴트 값으로 설정되어 있으나, 원하는 값으로 구성
    rletTpCd="VL" #상가
    tradTpCd="A1"
    # :B1:B2" #매매/전세/월세 매물 확인

    # clusterList?view 를 통한 그룹의 데이터를 가져온다.
    remaked_URL = "https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo={}&rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&btm={}&lft={}&top={}&rgt={}&pCortarNo={}_{}&addon=&bAddon=COMPLEX&isOnlyIsale=false".format(cortarNo, rletTpCd, tradTpCd, z, lat, lon,btm,lft,top,rgt,z,cortarNo)

    res2 = requests.get(remaked_URL,data={"isOnlyIsale":"false"},proxies=selected_proxy, headers=headers)

    json_str = json.loads(json.dumps(res2.json()))

    values = json_str['data']['ARTICLE']

    # 큰 원으로 구성되어 있는 전체 매물그룹(values)을 load 하여 한 그룹씩 세부 쿼리 진행
    for v in values:
        if countprints % 150 == 0:
            selected_proxy = random.choice(proxies_list)
            user_agent = random.choice(working_user_agents)
        # user_agent = random.choice(working_user_agents)

        # selected_proxy = random.choice(working_proxies)

        lgeo = v['lgeo']
        count = v['count']
        z2 = v['z']
        lat2 = v['lat']
        lon2 = v['lon']
        if countprints % 5 == 0:
            time.sleep(random.uniform(5, 10))
        len_pages = count / 20 + 1
        for idx in range(1, math.ceil(len_pages)):
            

            remaked_URL2 = "https://m.land.naver.com/cluster/ajax/articleList?""itemId={}&mapKey=&lgeo={}&showR0=&" \
                "rletTpCd={}&tradTpCd={}&z={}&lat={}&""lon={}&totCnt={}&cortarNo={}&page={}"\
                .format(lgeo, lgeo, rletTpCd, tradTpCd, z2, lat2, lon2, count,cortarNo, idx)

            
            res3 = requests.get(remaked_URL2,data={"isOnlyIsale":"false"},proxies=selected_proxy, headers=headers)
            json_str2 = json.loads(json.dumps(res3.json()))

            try:
                data = json_str2['body']
                for article in data:
                    atclNo = article.get('atclNo')        # 물건번호
                    rletTpNm = article.get('rletTpNm')    # 부동산 유형 (예: 아파트, 빌라 등)
                    tradTpNm = article.get('tradTpNm')    # 거래 유형 (예: 매매, 전세, 월세)
                    prc = article.get('prc')              # 가격
                    spc1 = article.get('spc1')            # 계약면적
                    spc2 = article.get('spc2')            # 실사용 면적
                    hanPrc = article.get('hanPrc')        # 보증금
                    rentPrc = article.get('rentPrc')      # 월세
                    flrInfo = article.get('flrInfo')      # 층 정보
                    rltrNm = article.get('rltrNm')        # 부동산 중개사
                    detailUrl = f"https://m.land.naver.com/article/info/{atclNo}"  # 상세 페이지 URL
                    counttimes += 1

                    # 여기에서 매물 정보를 출력하거나 다른 처리를 할 수 있습니다.
                    print(f"매물 번호: {atclNo}, 유형: {rletTpNm}, 거래 유형: {tradTpNm}, 가격: {prc}, 면적: {spc1}/{spc2}, 층: {flrInfo}, 중개사: {rltrNm}, 상세 페이지: {detailUrl}")
                countprints += 1
                print(countprints)
                print(counttimes)

                
            except ValueError as e:
                print(f"JSON 파싱 오류: {e}")

            except Exception as ex:

                print(f"에러 발생: {ex}")
                
    print("Request success with User-Agent:", user_agent)

except Exception as e:
    print("Request failed with User-Agent:", user_agent)
    print("Error:", e)