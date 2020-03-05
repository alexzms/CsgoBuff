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

#todo list: 
# 0:sticker analyze
# 8:better hover
# 9:login system

DEBUG = True


def login(username,password):
    #todo
    pass

def getItem(goods_id,page_num,headers,mode,sort = "price",keyword = ""):
    payload = {'game':'csgo','goods_id':goods_id,'page_num':str(page_num),'sort_by':sort,'mode':'','allow_tradable_cooldown':'1','_':''}
    r = requests.get('https://buff.163.com/api/market/goods/sell_order',params = payload,headers=headers)
    js = r.json()
    if mode == 1:
        itemPrice = []
        itemWear = []
        itemSticker = []
        itemImportance = []
        for x in range(0,10):
            importance = 0
            itemPrice.append(float(getInfo(js,x,'price')))
            itemWear.append(float(getWear(js,x)))
            stickers = getSticker(js,x)
            if (keyword in stickers[0][0]) or (keyword in stickers[1][0]) or (keyword in stickers[2][0]) or (keyword in stickers[3][0]):
                importance = 1
            itemSticker.append(stickers)
            itemImportance.append(importance)
        return [itemPrice,itemWear,itemSticker,itemImportance]
    elif mode == 2:
        return [getName(js,str(goods_id)),[],[]]
    

def getInfo(js,goods_id,item):
    content = js['data']['items'][goods_id][item]
    if content == '':
        content = '*null'
    return content

def getSticker(js,goods_id):
    stickers = js['data']['items'][goods_id]['asset_info']['info']['stickers']
    ret_sticker = []
    for x in range(0,len(stickers)):
        try: 
            ret_sticker.append([stickers[x]['name'],str((1-float(stickers[x]['wear']))*100) + ' %'])
        except:
            ret_sticker.append([stickers[x]['name'],'100.0 %'])
    for x in range(len(stickers),4):
        ret_sticker.append(['empty','empty'])
    return ret_sticker


def getWear(js,goods_id):
    return js['data']['items'][goods_id]['asset_info']['paintwear']

def getName(js,goods_id):
    return js['data']['goods_infos'][goods_id]['name']


def main():
    print('Counter-Strike Lowest Actual Price Counter')
    sort_method = ''
    if len(sys.argv) != 5:
        analyze = int(input("请输入你要分析的csgo饰品id: "))
        page_full = input("请输入你要分析的csgo饰品数量(x10)(格式：{起始页-终止页}): ")
        sort_method = input("请输入排序顺序(price(低到高),priced(高到低),wear,weard,new,old): ")
        keyword = input("请输入检索贴纸名称（片段）: ")
    else:
        analyze = int(sys.argv[1])
        page_full = sys.argv[2]
        sort_method = sys.argv[3]
        keyword = sys.argv[4]
        print ('已从启动参数获得参数')

    # page parse
    page_split = page_full.split('-')
    if len(page_split) != 2:
        print ("error - page input invalid")
        os.system('pause')
        return

    # sort parse
    if sort_method == 'price':
        sort_method = 'price.asc'
    elif sort_method == 'priced':
        sort_method = 'price.desc'
    elif sort_method == 'wear':
        sort_method = 'paintwear.asc'
    elif sort_method == 'wear':
        sort_method = 'paintwear.desc'
    elif sort_method == 'new':
        sort_method = 'created.desc'
    elif sort_method == 'old':
        sort_method = 'created.asc'

    page_start = int(page_split[0])
    page_end = int(page_split[1])
    login('','')
    data_all = []
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer':'https://buff.163.com/',
        'Cookie':'Device-Id=5O7uvnHzq4CxBpYJJXjo; _ga=GA1.2.197175233.1583391618; _gid=GA1.2.1393834490.1583391618; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=QuTlPR.llgPEBw4wxAM8W_OdqIi98SznzDbfdAmJdX4USnZrSDeaKRv74_sIugkZDyihTvKkxvl1MVDbm2JRayd75wez70tiDCtH4fijxQnTfxfHl.qoddgr0GICXH91sGUQQYmmyEJeRQfqDwuihzfWlKgVTZ4f5e4aAOlPuO_BD1qD2qhFvfmdimpZYWKNBDP.p.SYFUuNVjgLkdw.tqokf6VHS0u7jCAsfgL9ogSCh; S_INFO=1583420955|0|3&80##|19946167252; P_INFO=19946167252|1583420955|0|netease_buff|00&99|shh&1583391644&netease_buff#shh&null#10#0#0|&0|null|19946167252; session=1-X28xdjl9bY_rL1IdAYssNy-89jXgUT8j3cyPkY8TQb1A2046555823; csrf_token=IjJmYWU4YzhhOWY4NTU3YjU3OTExZjIyOTU0NmRiZDVlNzVhMmUyZTci.EUKsxA.22MLTFMXt9cgtb3YcOpESJ_105s'
    }
    itemName = getItem(analyze,1,headers,2,'default',"")[0]
    # print(price)
    # print(wear)
    # price_draw = np.array(flatten(price))
    # wear_draw = np.array(flatten(wear))
    # plt.scatter(wear_draw,price_draw,zorder = 0,picker = True)
    # plt.show()
    print("正在获取数据..")
    for x in range(page_start,page_end+1):
        data = getItem(analyze,x,headers,1,sort_method,keyword)
        for y in range(0,10):
            data_all.append([itemName,data[1][y],data[0][y],x,1,data[2][y][0][0],data[2][y][0][1],data[2][y][1][0],data[2][y][1][1],data[2][y][2][0],data[2][y][2][1],data[2][y][3][0],data[2][y][3][1],data[3][y]])
        print('|',end = '')
    df = pd.DataFrame(data_all, columns=['name','wear', 'price', 'page','number','sticker1_name','sticker1_wear','sticker2_name','sticker2_wear','sticker3_name','sticker3_wear','sticker4_name','sticker4_wear','importance'])
    fig = px.scatter(df,title = sort_method, x ="wear",y ="price",symbol = "importance",hover_name='name',hover_data=['page','number','sticker1_name','sticker1_wear','sticker2_name','sticker2_wear','sticker3_name','sticker3_wear','sticker4_name','sticker4_wear'],color = 'importance',labels=dict(wear = "磨损",price = "价格",page = "页码",number = "位数",sticker1_name = "        贴纸1",sticker1_wear = "贴纸1磨损",sticker2_name = "        贴纸2",sticker2_wear = "贴纸2磨损",sticker3_name = "        贴纸3",sticker3_wear = "贴纸3磨损", sticker4_name = "        贴纸4",sticker4_wear = "贴纸4磨损",importance = "贴纸片段匹配"))
    fig.show()
    


main()


    
    
