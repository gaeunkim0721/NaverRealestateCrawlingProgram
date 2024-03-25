import requests
from bs4 import BeautifulSoup
import json
import math
import random
import time

# User-Agent 리스트
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)land AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36',
]
# 프록시 서버 목록
proxies_list = [
    {"http": "http://35.185.196.38:3128", "https": "http://35.185.196.38:3128"},
    {"http": "http://208.196.136.141:3128", "https": "http://208.196.136.141:3128"},
    {"http": "http://8.219.97.248:80", "https": "http://8.219.97.248:80"},
    {"http": "http://5.252.23.220:3128", "https": "http://5.252.23.220:3128"},
    {"http": "http://41.216.183.18:8080", "https": "http://41.216.183.18:8080"},
    {"http": "http://72.10.160.171:29855", "https": "http://72.10.160.171:29855"},
    {"http": "http://2.58.56.39:80", "https": "http://2.58.56.39:80"},
    {"http": "http://109.108.40.238:8090", "https": "http://109.108.40.238:8090"},
    {"http": "http://112.78.188.42:8080", "https": "http://112.78.188.42:8080"},
    {"http": "http://188.93.237.29:3128", "https": "http://188.93.237.29:3128"},
    {"http": "http://4.180.165.171:8080", "https": "http://4.180.165.171:8080"},
    {"http": "http://112.78.188.46:8080", "https": "http://112.78.188.46:8080"},
    {"http": "http://66.70.238.78:8888", "https": "http://66.70.238.78:8888"},
    {"http": "http://134.209.105.209:3128", "https": "http://134.209.105.209:3128"},
    {"http": "http://20.247.228.80:80", "https": "http://20.247.228.80:80"},
    {"http": "http://8.222.152.158:55555", "https": "http://8.222.152.158:55555"},
    # 추가 프록시는 이와 같은 방식으로 리스트에 추가하면 됩니다.
]



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


selected_proxy = random.choice(working_proxies)


# 랜덤하게 1개의 User-Agent 선택
user_agent = random.choice(user_agents)


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


keyword = "서울"

url = "https://m.land.naver.com/search/result/{}".format(keyword)

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
        lgeo = v['lgeo']
        count = v['count']
        z2 = v['z']
        lat2 = v['lat']
        lon2 = v['lon']

        len_pages = count / 20 + 1
        for idx in range(1, math.ceil(len_pages)):
            
            remaked_URL2 = "https://m.land.naver.com/cluster/ajax/articleList?""itemId={}&mapKey=&lgeo={}&showR0=&" \
                "rletTpCd={}&tradTpCd={}&z={}&lat={}&""lon={}&totCnt={}&cortarNo={}&page={}"\
                .format(lgeo, lgeo, rletTpCd, tradTpCd, z2, lat2, lon2, count,cortarNo, idx)

            # time.sleep(random.uniform(0.5, 2.0))

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

                    # 여기에서 매물 정보를 출력하거나 다른 처리를 할 수 있습니다.
                    print(f"매물 번호: {atclNo}, 유형: {rletTpNm}, 거래 유형: {tradTpNm}, 가격: {prc}, 면적: {spc1}/{spc2}, 층: {flrInfo}, 중개사: {rltrNm}, 상세 페이지: {detailUrl}")

            except ValueError as e:
                print(f"JSON 파싱 오류: {e}")

            except Exception as ex:
                print(f"에러 발생: {ex}")
                
    print("Request success with User-Agent:", user_agent)

except Exception as e:
    print("Request failed with User-Agent:", user_agent)
    print("Error:", e)