import requests
import json
import pandas as pd

down_url = 'https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo=1168010800&rletTpCd=VL&tradTpCd=A1&z=14&lat=37.513583&lon=127.031375&btm=37.4932238&lft=127.0121918&top=37.5339366&rgt=127.0505582&pCortarNo=14_1168010800&addon=COMPLEX&bAddon=COMPLEX'
r = requests.get(down_url,data={"isOnlyIsale":"false"},headers={
    "Accept-Encoding": "gzip",
    "Host": "m.land.naver.com",
    "Referer": "https://m.land.naver.com/map/37.482968:127.0634:14:1168010300/VL/A1",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
})

temp=json.loads(r.text)



# def get_sido_info():
#     down_url = 'https://new.land.naver.com/api/regions/list?cortarNo=1100000000'
#     r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
#        "Accept-Encoding": "gzip",
#     "Host": "m.land.naver.com",
#     "Referer": "https://m.land.naver.com/map/37.482968:127.0634:14:1168010300/VL/A1",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-origin",
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
#     })
   
#     temp=json.loads(r.text)

#     print(temp)

#     # temp=list(pd.DataFrame(temp["regionList"])["cortarNo"])
#     return temp

seoul = 1100000000
gyunggi = 4100000000


def get_gungu_info(sido_code):
    down_url = 'https://new.land.naver.com/api/regions/list?cortarNo='+sido_code
    r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
        "Accept-Encoding": "gzip",
        "Host": "new.land.naver.com",
        "Referer": "https://new.land.naver.com/complexes/102378?ms=37.5018495,127.0438028,16&a=APT&b=A1&e=RETAIL",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    })
    temp=json.loads(r.text)


    # print(temp['regionList'][0])
    # print(temp['regionList')


    # temp=list(pd.DataFrame(temp['regionList'])["cortarNo"])
    return temp


def get_dong_info(gungu_code):
    down_url = 'https://new.land.naver.com/api/regions/list?cortarNo='+gungu_code
    r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
        "Accept-Encoding": "gzip",
        "Host": "new.land.naver.com",
        "Referer": "https://new.land.naver.com/complexes/102378?ms=37.5018495,127.0438028,16&a=APT&b=A1&e=RETAIL",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    })
    temp=json.loads(r.text)
    temp=list(pd.DataFrame(temp['regionList'])["cortarNo"])
    return temp


def get_apt_list(dong_code):
    down_url = 'https://new.land.naver.com/api/regions/complexes?cortarNo='+dong_code+'&realEstateType=APT&order='
    r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
        "Accept-Encoding": "gzip",
        "Host": "new.land.naver.com",
        "Referer": "https://new.land.naver.com/complexes/102378?ms=37.5018495,127.0438028,16&a=APT&b=A1&e=RETAIL",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    })
    temp=json.loads(r.text)






    try:
        temp=list(pd.DataFrame(temp['complexList'])["complexNo"])
    except:
        temp=[]
    return temp








sido code = seoul
# gungu_list=get_gungu_info(sido_list[0])
# dong_list=get_dong_info(gungu_list[0])
# get_apt_list(dong_list[0])[0]




print(sido_list)