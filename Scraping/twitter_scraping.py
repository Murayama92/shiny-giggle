import time
from selenium import webdriver
import pandas as pd

#URL
URL = 'https://twitter.com/search?f=tweets&q=%E3%83%90%E3%83%83%E3%83%89%E3%83%87%E3%82%B6%E3%82%A4%E3%83%B3%E8%B3%9E%E3%82%92%E5%8B%9D%E6%89%8B%E3%81%AB%E3%83%8E%E3%83%9F%E3%83%8D%E3%83%BC%E3%83%88%E3%81%97%E3%81%A6%E3%81%BF%E3%81%9F-2017%E5%B9%B4%E5%BA%A6%E7%89%88&src=typd'

if __name__ == '__main__':
    try:
        #クローム起動
        browser = webdriver.Chrome()
        #URLへ移動
        browser.get(URL)
        #１秒止める
        time.sleep(1)
        #スクロール(以下では3回分スクロールする)
        for i in range(10):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        #ツイート箇所を抜き出す。listに格納されている。 ←※指定すれば日にちやアカウント名も取れます。また、リンクなども除けると思いますが、とりあえずやってません。
        tweet_text = browser.find_elements_by_xpath('//p[contains(@class, "TweetTextSize")]')
        #結果表示
        count = 1
        list = [[title.text]for title in tweet_text]
        df =pd.DataFrame(list)
        print(df)
        df.to_csv('hatena11.csv',encoding='utf-8')
        
        
    finally:
        browser.quit()