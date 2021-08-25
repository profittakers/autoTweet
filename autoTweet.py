# -*- coding: utf-8 -*-

#tweet automation

import time
import datetime
import urllib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import six
from requests_oauthlib import OAuth1Session
import json
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

public_holiday_csv_url="https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"
holiday_file = public_holiday_csv_url.split("/")[-1]
today = str(datetime.datetime.today().strftime('%Y-%m-%d'))

def auto_tweet(today):
    CK = 'GBtfAhHDFNvBdqBY6l6u0ydTL'
    CS = '7l3edUAkeOJIeIs3rwH4HwR2BBQ6uEZqYM9PquivV3KU7KB55J'
    AT = '1418994768131117057-Xm5743Q55FOgnzd6ln2S6Y8kmnxINJ'
    AS = 'j2qLjhLOYw5y0bDHIich3l70wGfKpCwWDFzT65djqtfnB'
    
    twitter = OAuth1Session(CK, CS, AT, AS)

    url_media = "https://upload.twitter.com/1.1/media/upload.json"
    url_text = "https://api.twitter.com/1.1/statuses/update.json"
    
    # 画像 URL
    img_url = "file:///D:/Work/BitcoinOption/program/tweet_table_{}.jpg" .format(today)
    response = urllib.request.urlopen(img_url)
    data = response.read()
    files = {"media" : data}
    req_media = twitter.post(url_media, files = files)
    
    # レスポンス
    if req_media.status_code != 200:
        print ("画像アップロード失敗: %s", req_media.text)
        exit()
    
    # media_id を取得
    media_id = json.loads(req_media.text)['media_id']
    
    # 投稿した画像をツイートに添付したい場合はこんな風に取得したmedia_idを"media_ids"で指定してツイートを投稿
    message = '世界の市況'
    params = {'status': message, "media_ids": [media_id]}
    req_media = twitter.post(url_text, params = params)

"""
def auto_fav():
    for status in api.user_timeline(id='@(任意のツイッターID)'):
            #status.idでひとつひとつのツイートに存在するidを取得
            tweet_id = status.id 
    
            if status.text == 'a':
                try:
                    api.create_favorite(tweet_id)
                except:
                    print('error')
"""

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], Edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in  six.iteritems(mpl_table._cells):
        cell.set_edgecolor(Edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax


def create_tweet_data():
    #nikkei
    url0 = "https://stocks.finance.yahoo.co.jp/"
    selector0 = "#one-header > dl > dd:nth-child(3) > strong"
    diffselector0 = "#main > div:nth-child(7) > div:nth-child(1) > table > tr > td:nth-child(1) > dl > dd.pad4.clearFix > span > strong:nth-child(2)"
    #ose nikkei fut
    url1 = "https://www.bloomberg.co.jp/markets/stocks/futures"
    selector1 = "#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(8) > td:nth-child(4) > span"
    diffselector1 = "#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(8) > td:nth-child(5) > span"
    #WTI clude oil
    url2 = "https://www.bloomberg.co.jp/energy"
    selector2 = "#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > span"
    diffselector2 = "#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(1) > td:nth-child(5) > span"
    #nasdaq
    url3 = "https://www.bloomberg.co.jp/markets/stocks/world-indexes/americas"
    selector3 = "#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(15) > td:nth-child(2) > span"
    diffselector3 = "#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(15) > td:nth-child(4)"
    #dow indu
    url4 = "https://www.bloomberg.co.jp/markets/stocks/world-indexes/americas"
    selector4 = "#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(5) > td:nth-child(2) > span"
    diffselector4 = "#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(5) > td:nth-child(4)"
    #sp500
    url5 = "https://www.bloomberg.co.jp/markets/stocks/world-indexes/americas"
    selector5 = "#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(14) > td:nth-child(2) > span"
    diffselector5 ="#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(14) > td:nth-child(4)"
    #usd-jpy
    url6 = "https://www.bloomberg.co.jp/markets/currencies/americas"
    selector6 = "#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > span"
    diffselector6 = "#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(1) > td:nth-child(4) > span"
    #tresury10y
    url7 = "https://www.bloomberg.co.jp/markets/rates-bonds/government-bonds/us"
    selector7 ="#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(6) > td:nth-child(3) > span"
    diffselector7 = "#content > div > div > div.section-front__main-content > div.data-tables.first > div > table > tbody > tr:nth-child(6) > td:nth-child(4) > span"
    #xaujpy
    url8 = "https://www.bloomberg.co.jp/quote/XAUJPY:CUR"
    selector8 = "#content > div > div > div > div > div > div.price"
    diffselector8 = "#content > div > div > div.basic-quote > div > div > div.change-container > div:nth-child(2)"
    #xbtjpy
    url9 = "https://www.cnbc.com/quotes/BTCJPY="
    selector9 = "#MainContentContainer > div > div.QuotePageBuilder-row > div.QuotePageBuilder-mainContent.QuotePageBuilder-col > div.QuoteStrip-container > div.QuoteStrip-dataContainer > div.QuoteStrip-lastTimeAndPriceContainer > div.QuoteStrip-lastPriceStripContainer > span.QuoteStrip-lastPrice"
    diffselector9 = "#MainContentContainer > div > div.QuotePageBuilder-row > div.QuotePageBuilder-mainContent.QuotePageBuilder-col > div.QuoteStrip-container > div.QuoteStrip-dataContainer > div.QuoteStrip-lastTimeAndPriceContainer > div.QuoteStrip-lastPriceStripContainer > span.QuoteStrip-changeUp > span:nth-child(3)"
    #VIX
    url10 = "https://www.bloomberg.co.jp/quote/VIX:IND"
    selector10 = "#content > div > div > div.basic-quote > div > div > div.price"
    diffselector10 = "#content > div > div > div.basic-quote > div > div > div.change-container > div:nth-child(2)"
    
    urllist = [url0, url1, url2, url3, url4, url5, url6, url7, url8, url9, url10]
    selectorlist = [selector0, selector1, selector2, selector3, selector4, selector5, selector6, selector7, selector8, selector9, selector10]
    diffselectorlist = [diffselector0, diffselector1, diffselector2, diffselector3, diffselector4, diffselector5, diffselector6, diffselector7, diffselector8, diffselector9, diffselector10]

    datalist=[]
    for i in range(11):
        try:
            response = requests.get(urllist[i])
            time.sleep(3)
            soup = BeautifulSoup(response.text, 'html.parser')
            value = soup.select_one(selectorlist[i]).text.replace(",","").replace("%", "").replace("(","").replace(")","")
            diff = soup.select_one(diffselectorlist[i]).text.replace(",","").replace("%", "").replace("(","").replace(")","")
            datalist.append(value)
            datalist.append(diff)
        except:
            datalist.append("0")
            datalist.append("0")
            number=str(i)
            print(f"{number}th data could not be retrieved")
    return datalist
    
def get_holiday_flg(date):
    # 通常の土日
    if (date.weekday() >= 5):
        return True
    # 祝日
    holidays_df = pd.read_table(holiday_file, delimiter=',', encoding="SHIFT-JIS")
    if date.strftime("%Y-%m-%d") in holidays_df['国民の祝日・休日月日'].tolist():
        return True
    return False

def get_previous_businessday():
    urllib.request.urlretrieve(public_holiday_csv_url, holiday_file)

    # 年始から日付を回す
    date = datetime.datetime.today()
    date += datetime.timedelta(days=-1)
    while get_holiday_flg(date):
        date += datetime.timedelta(days=-1)
    date=date.strftime('%Y-%m-%d')
    return date

def changeNKAtopercent(datalist, df):
    predflist = df.values.tolist()[0]
    datalist[3] =str(round((float(datalist[2]) - float(predflist[2])) / float(predflist[2]) * 100, 3))
    return datalist

def changeXBTtopercent(datalist, df):
    predflist = df.values.tolist()[0]
    datalist[19] =str(round((float(datalist[18]) - float(predflist[18])) / float(predflist[18]) * 100, 3))
    return datalist

def create_database(datalist):
    df = pd.read_excel("data.xlsx", index_col=0)
    collist = df.columns.tolist()
    yesterday = get_previous_businessday()
    datalist = changeNKAtopercent(datalist, df)
    datalist = changeXBTtopercent(datalist, df)
    df1 = pd.DataFrame(datalist, index = collist, columns = [yesterday]).T
    df=pd.concat([df1,df], sort = False)
    df.to_excel("data.xlsx", sheet_name= "historical_data")
    return df
    
def create_tweet_table(df,today):
    dflist0 = df.values.tolist()[0]
    index_list = ["", 'Indicies', "", 'Futures', "", 'Currency, Rates, Comodities']
    columns_list = ["", "", "", "", ""]
    Indicies_names_list = ["日経平均", "S&P500", "NASDAQ", "DOW工業株30種平均", "VIX"]
    indicies_list = [str(dflist0[0])+ "  " + "(" + str(dflist0[1]) + "%)",
                     str(dflist0[10])+ "  " + "(" + str(dflist0[11]) + "%)",
                     str(dflist0[6])+ "  " + "(" + str(dflist0[7]) + "%)",
                     str(dflist0[8])+ "  " + "(" + str(dflist0[9]) + "%)",
                     str(dflist0[20])+ "  " + "(" + str(dflist0[21]) + "%)"]
    
    futures_names_list = ["大取日経先物", "WTI原油先物", "", "", ""]
    futures_list = [str(dflist0[2])+ "  " + "(" + str(dflist0[3]) + "%)",
                    str(dflist0[4])+ "  " + "(" + str(dflist0[5]) + "%)",
                    "",
                    "",
                    ""]
    
    other_names_list = ["USD/JPY", "ビットコイン", "金", "10年米国債", ""]
    other_list = [str(dflist0[12])+ "  " + "(" + str(dflist0[13]) + "%)",
                  str(dflist0[18])+ "  " + "(" + str(dflist0[19]) + "%)",
                  str(dflist0[16])+ "  " + "(" + str(dflist0[17]) + "%)",
                  str(dflist0[14])+ " (利回り" + str(dflist0[15]) + "%)",
                  "",]
    
    tweet_table_list = [Indicies_names_list, indicies_list, futures_names_list, futures_list, other_names_list, other_list]
    tweet_table = pd.DataFrame(tweet_table_list, index = index_list, columns=columns_list)
    
    #pd.get_option("display.max_columns")
    #pd.set_option('display.max_columns', 50)
    
    fig = go.Figure(data=[go.Table(
            columnwidth =  [22, 22, 22, 22, 22], #カラム幅の変更
            cells=dict(values=tweet_table.values.T,line_color='white', align='center', font = dict(color = 'black', size = 10))
            )])
    fig.update_layout(title={'text': "Market summary",'y':0.85,'x':0.5,'xanchor': 'center'})#タイトル位置の調整
    fig.layout.title.font.size= 24 #タイトルフォントサイズの変更
    fig_title = "tweet_table_{}.jpg".format(today)
    fig.write_image(fig_title)
    

def main():
    datalist = create_tweet_data()
    df = create_database(datalist)
    create_tweet_table(df, today)
    auto_tweet(today)
    
if __name__ == "__main__":
    main()
    
    
    