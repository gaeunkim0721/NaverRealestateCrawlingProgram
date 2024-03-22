import requests
from bs4 import BeautifulSoup
import json
import math

#아래의 userAgent들 중 골라서 사용할것
userAgent1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
userAgent2 = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
userAgent3 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"


keyword = "서울"

url = "https://m.land.naver.com/search/result/{}".format(keyword)

res = requests.get(url,data={"isOnlyIsale":"false"},headers={
    "Accept-Encoding": "gzip",
    "Host": "m.land.naver.com",
    "Referer": "https://m.land.naver.com/map/37.482968:127.0634:14:1168010300/VL/A1",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": userAgent1
})

# res = requests.get(url) 네이버에서 접근을 막아서 위해 위와 같이 수정. userAgent3가 가장 잘됨

res.raise_for_status()

# print(url)

soup = (str)(BeautifulSoup(res.text, "lxml"))

# print(soup)s

#응답 메시지 속에서 원하는 데이터 얻기
#  filter: {
#             lat: '37.550985',
#             lon: '126.849534',
#             z: '12',
#             cortarNo: '1150000000',
#             cortarNm: '강서구',
#             rletTpCds: '*',
#             tradTpCds: 'A1:B1:B2'
#         },

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

# clusterList?view 를 통한 그룹(단지)의 데이터를 가져온다.
remaked_URL = "https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo={}&rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&btm={}&lft={}&top={}&rgt={}&pCortarNo={}_{}&addon=&bAddon=COMPLEX&isOnlyIsale=false".format(cortarNo, rletTpCd, tradTpCd, z, lat, lon,btm,lft,top,rgt,z,cortarNo)

# print(remaked_URL)

# res2 = requests.get(remaked_URL) 아래처럼 설정

res2 = requests.get(remaked_URL,data={"isOnlyIsale":"false"},headers={
    "Accept-Encoding": "gzip",
    "Host": "m.land.naver.com",
    "Referer": "https://m.land.naver.com/map/37.482968:127.0634:14:1168010300/VL/A1",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": userAgent1
})


json_str = json.loads(json.dumps(res2.json()))

# print(res2)


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

        res3 = requests.get(remaked_URL,data={"isOnlyIsale":"false"},headers={
            "Accept-Encoding": "gzip",
            "Host": "m.land.naver.com",
            "Referer": "https://m.land.naver.com/map/37.482968:127.0634:14:1168010300/VL/A1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": userAgent1
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


