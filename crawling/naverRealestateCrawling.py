import requests
from bs4 import BeautifulSoup
import json


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
    "User-Agent": userAgent3
})

# res = requests.get(url) 네이버에서 접근을 막아서 위해 위와 같이 수정. userAgent3가 가장 잘됨

res.raise_for_status()


soup = (str)(BeautifulSoup(res.text, "lxml"))


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
rletTpCds = value.split("rletTpCds:")[1].split(",")[0]
tradTpCds = value.split("tradTpCds:")[1].split()[0]

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
rletTpCds="VL" #상가
tradTpCds="A1:B1:B2" #매매/전세/월세 매물 확인

# clusterList?view 를 통한 그룹(단지)의 데이터를 가져온다.
remaked_URL = "https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo={}&rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&btm={}&lft={}&top={}&rgt={}\
    &pCortarNo=14_4182025000&addon=COMPLEX&bAddon=COMPLEX&isOnlyIsale=false".format(cortarNo, rletTpCds, tradTpCds, z, lat, lon,btm,lft,top,rgt)

res2 = requests.get(remaked_URL)
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
            .format(lgeo, lgeo, rletTpCds, tradTpCds, z2, lat2, lon2, count,cortarNo, idx)



atclNo = v['atclNo']        # 물건번호
rletTpNm = v['rletTpNm']    # 상가구분
tradTpNm = v['tradTpNm']    # 매매/전세/월세 구분
prc = v['prc']              # 가격
spc1 = v['spc1']            # 계약면적(m2) -> 평으로 계산 : * 0.3025
spc2 = v['spc2']            # 전용면적(m2) -> 평으로 계산 : * 0.3025
hanPrc = v['hanPrc']        # 보증금                
rentPrc = v['rentPrc']      # 월세
flrInfo = v['flrInfo']      # 층수(물건층/전체층)
tagList = v['tagList']      # 기타 정보
rltrNm = v['rltrNm']        # 부동산
detaild_information = "https://m.land.naver.com/article/info/{}".format(atclNo)


print(v)