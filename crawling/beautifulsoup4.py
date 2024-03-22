import requests
import json
import pandas as pd

userAgent1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
userAgent2 = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
userAgent3 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"


down_url = 'https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo=1168010800&rletTpCd=VL&tradTpCd=A1&z=14&lat=37.513583&lon=127.031375&btm=37.4932238&lft=127.0121918&top=37.5339366&rgt=127.0505582&pCortarNo=14_1168010800&addon=COMPLEX&bAddon=COMPLEX'
r = requests.get(down_url,data={"isOnlyIsale":"false"},headers={
    "Accept-Encoding": "gzip",
    "Host": "m.land.naver.com",
    "Referer": "https://m.land.naver.com/map/37.482968:127.0634:14:1168010300/VL/A1",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": userAgent3
})

temp=json.loads(r.text)

seoulCode = '1100000000'
gyunggiCode = '4100000000'


def get_gungu_info(sido_code):
    down_url = 'https://new.land.naver.com/api/regions/list?cortarNo='+sido_code
    r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
        "Accept-Encoding": "gzip",
        "Host": "m.land.naver.com",
        "Referer": "https://m.land.naver.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": userAgent3
    })
    temp=json.loads(r.text)

    gungu_info = [(item['cortarName'], item['cortarNo']) for item in temp['regionList']]  # 동 이름과 cortarNo 추출

    return gungu_info


def get_dong_info(gungu_code):
    down_url = 'https://new.land.naver.com/api/regions/list?cortarNo='+gungu_code
    r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
        "Accept-Encoding": "gzip",
        "Host": "m.land.naver.com",
        "Referer": "https://m.land.naver.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": userAgent3
    })
    temp=json.loads(r.text)

    dong_info = [(item['cortarName'], item['cortarNo']) for item in temp['regionList']]  # 동 이름과 cortarNo 추출
    
    return dong_info


def get_vl_list(dong_code):

    down_url = 'https://new.land.naver.com/api/houses/'+dong_code
    https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo=4182025000&rletTpCd=VL&tradTpCd=A1&z=14&lat=37.825363&lon=127.516049&btm=37.8050891&lft=127.4968658&top=37.8456313&rgt=127.5352322&pCortarNo=14_4182025000&addon=COMPLEX&bAddon=COMPLEX&isOnlyIsale=false

    r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
        "Accept-Encoding": "gzip",
        "Host": "m.land.naver.com",
        "Referer": "https://m.land.naver.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": userAgent3
    })
    temp=json.loads(r.text)

    vl_info = []

    print(temp)


    if 'result' in temp:
        for item in temp['result']:
            vl_name = item['list'].get('atclFetrDesc', '정보 없음')  # 매물 설명
            vl_price = item['list'].get('hanPrc', '가격 정보 없음')  # 매물 가격
            vl_info.append((vl_name, vl_price))
    
    return vl_info








seoulGunguList = get_gungu_info(seoulCode)
gyunggiGunguList = get_gungu_info(gyunggiCode)

for gungu_name, gungu_code in seoulGunguList:
    print(f"\n군구 이름: {gungu_name}, 군구 코드: {gungu_code}\n")
    dong_info= get_dong_info(gungu_code)
    for dong_name, dong_code in dong_info:
        print(f"  동 이름: {dong_name}, 동 코드: {dong_code}")
        vl_info = get_vl_list(dong_code)
        for vl_name, vl_price in vl_info:
            print(f"  매물 이름: {vl_name}, 매물 가격: {vl_price}")