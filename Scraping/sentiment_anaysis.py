
#事前にPythonに以下をインストール
from janome.tokenizer import Tokenizer
import pandas as pd
import matplotlib.pyplot as plt

#形態素分解を実行する関数
def do_tokenizer(df):
    # dfの2列目にツイート文が入っているので、colに1を格納。
    col = 1
    # 結果格納用リスト
    tweets_tokenized = []
    # for文の中で使う結果用リスト
    each_tweet = []
    # 形態素解析のクラスをインスタンス化
    t = Tokenizer()
    # 2列目に記載されているすべてのセルを1行目から順に読み取る。
    for row in range(len(df.index)):
        # df.iat[row, col].replace("A","B")はAをBに置き換える。今回の場合、記事のタイトル、ブログ名、URLを消去している。
        df.iat[row, col] = df.iat[row, col].replace("バッドデザイン賞を勝手にノミネートしてみた-2017年度版","")
        df.iat[row, col] = df.iat[row, col].replace("酔いどれデザイン日誌","")
        df.iat[row, col] = df.iat[row, col].replace("http://takachi.hatenablog.jp/entry/yamanashi","")
        # valにツイートを格納。
        val = df.iat[row, col]
        # valを形態素に分けたものをtokensに格納。
        tokens = t.tokenize(val)
        # 形態素ごとの処理。#名詞だけ、用言だけ、のようなときに使うが、今回は全ての形態素を使っている。
        for token in tokens:
            
            ########名詞のみの時のコード。関係なし。
            ##partOfSpeech = token.part_of_speech.split(',')[0]
            ##if partOfSpeech == u'名詞':
            ########
            
            # token.surfaceは表層形(語彙)。詳しくは　⇒　http://ailaby.com/janome/
            # each_tweetに格納。(例：each_tweet[0] ⇒　山梨、の、温泉、は、マジ、で、ヤバ、い)
            each_tweet.append(token.surface) 
        #tweets_tokenizedに格納。(tweets_tokenizedはリストのリスト(2次元配列))
        tweets_tokenized.append(each_tweet)
        each_tweet = []
    return(tweets_tokenized)



# 形態素解析結果の単語ごとにPN値を割り当てる関数
def search_pnvalue(data, pn_dict):
    pnvalue = []
    each_pnvalue = []
    for tweet_num in range(len(data)):
        for word in range(len(data[tweet_num])):
            if data[tweet_num][word] in pn_dict:
                pn = float(pn_dict[data[tweet_num][word]]) 
            else:
                #辞書にない時。
                pn = 'notfound'            
            each_pnvalue.append(pn)
        pnvalue.append(each_pnvalue)
        each_pnvalue = []
    return(pnvalue)






if __name__ == '__main__':
    #データの読み込み(最後に処理前のdataが欲しいので二つ作っておく。)
    data = pd.read_csv("hatena1.csv")
    tweets = pd.read_csv("hatena1.csv")
    

    # PN Tableを読み込み
    pn_df = pd.read_csv('pn_ja.dic.txt',\
                        sep=':',
                        encoding='cp932',
                        names=('Word','Reading','POS', 'PN')
                       )
    # 照合するために、PN Tableをデータフレームからdict型に変換しておく。(例：pn_dict["楽しい"] = 0.9)
    pn_dict = dict(zip(pn_df['Word'], pn_df['PN']))




    #0番目のツイートの3番目の形態素は tweets_tokenized[0][3]となる。
    tweets_tokenized = do_tokenizer(tweets)

    #0番目のツイートの3番目の形態素である tweets_tokenized[0][3] の pn値は pn[0][3] という対応。
    pn = search_pnvalue(tweets_tokenized, pn_dict)


    #各ツイートごとにpn値の平均を計算し、元のデータとくっつける。
    tweet_pn = []
    for tweet_num in range(len(tweets_tokenized)):
        sum = 0
        count = 0
        for word in range(len(tweets_tokenized[tweet_num])):
            if pn[tweet_num][word] != 'notfound':
                sum=sum+pn[tweet_num][word]
                count = count + 1
        #形態素数で平均
        if count == 0:
            tweet_pn.append(0)
        else:  
            tweet_pn.append(sum/count)
    data['pn'] = tweet_pn
    print(data[['pn','0']])
    
    tweets_tokenized_pn = []
    for tweet_num in range(len(tweets_tokenized)):
        tweets_tokenized_pn.append(dict(zip(tweets_tokenized[tweet_num], pn[tweet_num])))
    data['tweets_tokenized_pn'] = tweets_tokenized_pn
    #0以外をプロット
    plt.hist(data['pn'][data['pn']!=0],bins=50)
    plt.show()
    
    data.to_csv('hatena1_pn.csv')

    
