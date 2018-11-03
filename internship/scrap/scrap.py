import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def outputcsv(prec,city,name,cname):

        columns = (
                    '年','月','日',
                    '現地平均気圧(hPa)', '海面平均気圧(hpa)',
                    '降水量合計', '1時間最大降水量', '10分間最大降水量', '平均気温(℃)', '最高気温(℃)', '最低気温(℃)',
                    '平均湿度(%)','最小湿度(%)',
                    '平均風速','最大風速','最大風速時の風向','最大瞬間風速','最大瞬間風速時の風向',
                    '日照時間(h)','降雪合計(cm)','最深積雪値',
                    '天気概要昼','天気概要夜'
                    )

        all_df = []
        for year in range(2015,2018):

                for month in range(1,13):

                        url_base = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=" + str(prec) + "&block_no=" + str(city) + "&year=" + str(year) + "&month=" + str(month) + "&day=1&view=p1"
                        #url_base = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_a1.php?prec_no=" + prec + "&block_no=" + city + "&year=" + str(year) + "&month=" + str(month) + "&day=1&view=p1"

                        r = requests.get(url_base)

                        try:
                            r.raise_for_status() # check for error
                        except Exception as e:
                            print('Error: {}'.format(e))
                            continue # go to next if error

                        r.encoding = r.apparent_encoding

                        #対象である表をスクレイピング
                        soup = BeautifulSoup(r.text,'lxml')
                        rows = soup.findAll('tr',class_='mtx')

                        #表の最初の１〜３行目はカラム情報なのでスライス
                        rows = rows[4:]

                        #for文で1日〜最終日までの１行を取得
                        for row in rows:
                                data = row.findAll('td')

                                #１行の中データを取り出す
                                day_row=[]
                                day_row.extend([year,month])
                                for d in data:
                                        day_row.append(d.text)

                                day_df = pd.DataFrame(columns=columns)
                                day_df.loc[0] = day_row
                                all_df.append(day_df)

                        time.sleep(1) # wait for 1 sec

        df = pd.concat(all_df, ignore_index=True)

        #日付をdatatime型に変換
        df['日付'] = pd.to_datetime(df['年'].astype(str) + ' / ' + df['月'].astype(str) + ' / ' + df['日'].astype(str))
        dtfrm = df.set_index('日付')
        del dtfrm['年'],dtfrm['月'],dtfrm['日']

        dtfrm.to_csv("weather_day/weather_" + name + "_" + cname + ".csv", index=True, encoding="shift_jis")

#都道府県毎のURLパターン
url_list =[
            [14,47412,"Hokkaido","Sapporo","札幌"],
            [31,47575,"Aomori","Aomori","青森"],
            [33,47584,"Iwate","Morioka","盛岡"],
            [34,47590,"Miyagi","Sendai","仙台"],
            [32,47582,"Akita","Akita","秋田"],
            [35,47588,"Yamagata","Yamagata","山形"],
            [36,47595,"Fukushima","Fukushima","福島"],
            [40,47629,"Ibaraki","Mito","水戸"],
            [41,47615,"Tochigi","Utsunomiya","宇都宮"],
            [42,47624,"Gunma","Maebashi","前橋"],
            #[43,"0363","Saitama","Saitama","埼玉"],
            [45,47648,"Chiba","Choshi","銚子"],
            [44,47662,"Tokyo","Tokyo","東京"],
            [46,47670,"Kanagawa","Yokohama","横浜"],
            [54,47604,"Niigata","Niigata","新潟"],
            [55,47607,"Toyama","Toyama","富山"],
            [56,47605,"Ishikawa","Kanazawa","金沢"],
            [57,47616,"Fukui","Fukui","福井"],
            [49,47638,"Yamanashi","Kofu","甲府"],
            [48,47610,"Nagano","Nagano","長野"],
            [52,47632,"Gifu","Gifu","岐阜"],
            [50,47656,"Shizuoka","Shizuoka","静岡"],
            [51,47636,"Aichi","Nagoya","名古屋"],
            [53,47651,"Mie","Tsu","津"],
            [60,47761,"Shiga","Hikone","彦根"],
            [61,47759,"Kyoto","Kyoto","京都"],
            [62,47772,"Osaka","Osaka","大阪"],
            [63,47770,"Hyogo","Kobe","神戸"],
            [64,47780,"Nara","Nara","奈良"],
            [65,47777,"Wakayama","Wakayama","和歌山"],
            [69,47746,"Tottori","Tottori","鳥取"],
            [68,47741,"Shimane","Matsue","松江"],
            [66,47768,"Okayama","Okayama","岡山"],
            [67,47765,"Hiroshima","Hiroshima","広島"],
            [81,47784,"Yamaguchi","Shimonoseki","下関"],
            [71,47895,"Tokushima","Tokushima","徳島"],
            [72,47891,"Kagawa","Takamatsu","高松"],
            [73,47887,"Ehime","Matsuyama","松山"],
            [74,47893,"Kochi","Kochi","高知"],
            [82,47807,"Fukuoka","Fukuoka","福岡"],
            [85,47813,"Saga","Saga","佐賀"],
            [84,47817,"Nagasaki","Nagasaki","長崎"],
            [86,47819,"Kumamoto","Kumamoto","熊本"],
            [83,47815,"Oita","Oita","大分"],
            [87,47830,"Miyazaki","Miyazaki","宮崎"],
            [88,47827,"Kagoshima","Kagoshima","鹿児島"],
            [91,47936,"Okinawa","Naha","那覇"]
]

#for n in range(len(url_list)): #札幌だけならrange(1)
for n in range(1):
    outputcsv(url_list[n][0],url_list[n][1],url_list[n][2],url_list[n][3])
