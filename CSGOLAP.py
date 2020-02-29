import requests
import json
import os
import paramiko
import datetime
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import plotly_express as px
import plotly
import sys


def login(username,password):
    #todo
    pass

def getItem(goods_id,page_num,headers,mode):
    payload = {'game':'csgo','goods_id':goods_id,'page_num':str(page_num),'sort_by':'default','mode':'','allow_tradable_cooldown':'1','_':''}
    r = requests.get('https://buff.163.com/api/market/goods/sell_order',params = payload,headers=headers)
    js = r.json()
    if mode == 1:
        itemPrice = []
        itemWear = []
        for x in range(0,10):
            itemPrice.append(float(getInfo(js,x,'price')))
            itemWear.append(float(getWear(js,x)))
        return [itemPrice,itemWear]
    elif mode == 2:
        return [getName(js,str(goods_id)),'null']
    

def getInfo(js,goods_id,item):
    content = js['data']['items'][goods_id][item]
    if content == '':
        content = '*null'
    return content

def getWear(js,goods_id):
    return js['data']['items'][goods_id]['asset_info']['paintwear']

def getName(js,goods_id):
    return js['data']['goods_infos'][goods_id]['name']

def flatten(a):
    if not isinstance(a, (list, )):
        return [a]
    else:
        b = []
        for item in a:
            b += flatten(item)
    return b

def main():
    print('Counter-Strike Lowest Actual Price Counter')
    if len(sys.argv) != 3:
        analyze = int(input("请输入你要分析的csgo饰品id: "))
        page_full = int(input("请输入你要分析的csgo饰品数量(x10): "))
    else:
        analyze = int(sys.argv[1])
        page_full = int(sys.argv[2])
    login('','')
    data_all = []
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer':'https://buff.163.com/',
        'Cookie':'mail_psc_fingerprint=01fde5382cc83a2df5599647c6b1bccc; _ntes_nnid=8f32ece229cabf2b415c5d84bed54e45,1553513994953; _ntes_nuid=8f32ece229cabf2b415c5d84bed54e45; usertrack=CrHum1ynbCoMKKIsAwU+Ag==; vinfo_n_f_l_n3=549968d4ed4cfbe3.1.0.1570117734269.0.1570117797098; nts_mail_user=pumusy4546997@163.com:-1:1; Device-Id=4zwPlnjIQUO6zLQtEYTy; _ga=GA1.2.1629007142.1575890972; _ns=NS1.2.255152277.1581691039; Locale-Supported=zh-Hans; game=csgo; _gid=GA1.2.1894175785.1582985758; NTES_YD_SESS=Ga.vA045gNGC9CgP_xTvS9MBsXCHriUmW.VlWS06WQXd5EnP5.MfeYbDXZ7skRTn.mzOibeTobgqjU.V0x6YfmWDCaM1D9Fz.wFLXlz4oGEilolLgN2BWWRP93swQLuq73dGG800mI6MYGl2.akzO1lrgeRUinXlCMXfS_gAk_ZHSCwmC_8fAoHiZvZzhlGHqq02jUfJ6j5GgxqXMw.XjvUTlKUL59kD4wS7lRJuBR5wO; S_INFO=1582985877|0|3&80##|19946167252; P_INFO=19946167252|1582985877|0|netease_buff|00&99|shh&1579923113&netease_buff#shh&null#10#0#0|&0|null|19946167252; session=1-Sqz4Loze6hIo69NmH8Oxe5t6iQKEvPysQD_ZTGn3tyjG2046555823; _gat_gtag_UA_109989484_1=1; csrf_token=ImRjZWRlMTI2N2QwYzRlNTU2OTgyY2I4ZDdiNzdiMjk2MTBjMmRjYzEi.ETwHCA.n9lwH7yd6lDR_2pbJICdMUDCANg'
    }
    itemName = getItem(analyze,1,headers,2)[0]
    # print(price)
    # print(wear)
    # price_draw = np.array(flatten(price))
    # wear_draw = np.array(flatten(wear))
    # plt.scatter(wear_draw,price_draw,zorder = 0,picker = True)
    # plt.show()
    for x in range(1,page_full+1):
        data = getItem(analyze,x,headers,1)
        data_all.append([itemName,data[1][0],data[0][0],x,1])
        data_all.append([itemName,data[1][1],data[0][1],x,2])
        data_all.append([itemName,data[1][2],data[0][2],x,3])
        data_all.append([itemName,data[1][3],data[0][3],x,4])
        data_all.append([itemName,data[1][4],data[0][4],x,5])
        data_all.append([itemName,data[1][5],data[0][5],x,6])
        data_all.append([itemName,data[1][6],data[0][6],x,7])
        data_all.append([itemName,data[1][7],data[0][7],x,8])
        data_all.append([itemName,data[1][8],data[0][8],x,9])
        data_all.append([itemName,data[1][9],data[0][9],x,10])
    df = pd.DataFrame(data_all, columns=['name','wear', 'price', 'page','number'])
    fig = px.scatter(df, x ="wear",y ="price",hover_name='name',hover_data=['page','number'],color = 'page')
    fig.show()
    


main()


    
    
