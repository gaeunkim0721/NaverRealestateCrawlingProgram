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

# 랜덤하게 1개의 User-Agent 선택
user_agent = random.choice(user_agents)

keyword = "서울"

url = "https://m.land.naver.com/search/result/{}".format(keyword)

try:
    res = requests.get(url ,data={"isOnlyIsale":"false"},headers={
        "Accept-Encoding": "gzip",
        "X-Requested-With": "XMLHttpRequest",
        "Host": "m.land.naver.com",
        "Referer": "https://m.land.naver.com/map/37.482968:127.0634:14:1168010300/VL/A1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": user_agent,
        "Accept": "application/json",
    })
    
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

    res2 = requests.get(remaked_URL,data={"isOnlyIsale":"false"},headers={
        "Accept-Encoding": "gzip",
        "X-Requested-With": "XMLHttpRequest",
        "Host": "m.land.naver.com",
        "Referer": "https://m.land.naver.com/map/37.482968:127.0634:14:1168010300/VL/A1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": user_agent,
        "Accept": "application/json",
    })

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

            time.sleep(0.1)

            res3 = requests.get(remaked_URL2,data={"isOnlyIsale":"false"},headers={
                "Accept-Encoding": "gzip",
                "X-Requested-With": "XMLHttpRequest",
                "Host": "m.land.naver.com",
                "Referer": "https://m.land.naver.com/map/37.482968:127.0634:14:1168010300/VL/A1",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": user_agent,
                "Accept": "application/json",
            })

            try:
                data = res3.json()
                articles = data.get('data', {}).get('list', [])
                for article in articles:
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

            # atclNo = v['atclNo']        # 물건번호
            # rletTpNm = v['rletTpNm']    # 상가구분
            # tradTpNm = v['tradTpNm']    # 매매/전세/월세 구분
            # prc = v['prc']              # 가격
            # spc1 = v['spc1']            # 계약면적(m2) -> 평으로 계산 : * 0.3025
            # spc2 = v['spc2']            # 전용면적(m2) -> 평으로 계산 : * 0.3025
            # hanPrc = v['hanPrc']        # 보증금                
            # rentPrc = v['rentPrc']      # 월세
            # flrInfo = v['flrInfo']      # 층수(물건층/전체층)
            # tagList = v['tagList']      # 기타 정보
            # rltrNm = v['rltrNm']        # 부동산
            # detaild_information = "https://m.land.naver.com/article/info/{}".format(atclNo)
                
    print("Request success with User-Agent:", user_agent)

except Exception as e:
    print("Request failed with User-Agent:", user_agent)
    print("Error:", e)