import numpy as np
from scipy import signal
from matplotlib import pylab as plt
import R_picker

def load_data():
    """データ読み込み"""
    data = np.zeros((2,60000))
    for lead in range(1,3):
        filename="./Health_ecg.csv" # ファイル名指定
        data[lead-1] = np.loadtxt(filename,delimiter=",",usecols=lead, skiprows=2) # ヘッダー2行飛ばし、指定の行(誘導)を読み込む

    return data


def mdfilter(x):
    """メディアンフィルターを適用したノイズ除去"""
    WINDOW = 10
    zengo = np.zeros(WINDOW//2)
    x=list(x)
    zengo=list(zengo)
    prepro_data = zengo + x + zengo
    prepro_data = np.array(prepro_data,dtype=np.float64)

    after_data=[]
    for i in range(len(prepro_data)-1):
        tmp = prepro_data[i:i+WINDOW]
        after_data += [np.median(tmp)]

    y = np.array(after_data).reshape(-1)

    return y[:len(y)-WINDOW]


def detrend(x):
    """回帰分析を利用したトレンド除去"""
    z = np.polyfit(np.arange(len(x)), x, 14)
    v = np.poly1d(z)
    p = v(np.arange(len(x)))
    return (x - p)


def processing(data):
    """前処理とR波検出"""
    for i in range(len(data)):

        #トレンド除去
        # detrend_data = signal.detrend(data[i][j]) //scipyの機能を使う場合
        detrend_data = detrend(data[i])
        # plt.plot(detrend_data)
        # plt.show()

        # ノイズ除去
        denoise_data = mdfilter(detrend_data)
        # plt.plot(denoise_data)
        # plt.show()

        # R波検出
        # ピークのしきい値を 0.19 mV より上に設定
        # ピークの間隔が 650点以上と設定
        R_idx = R_picker.R_pick(denoise_data,0.19,650)
        # R_picker.max_plot(denoise_data,R_idx) # R波の部位をプロット
        # plt.show()

        for j in range(len(R_idx)):
            if j != 0 and j != len(R_idx)-1: # 中途半端な波形になりそうなものは除外
                basic = denoise_data[R_idx[j]-200:R_idx[j]+451]
                filename = "./Health_Basic/"+str(i)+"/"+str(j)+".csv"
                np.savetxt(filename, basic, delimiter=",")


def main():
    data = load_data()
    processing(data)


if __name__ == "__main__":
    main()
