import numpy as np
from matplotlib import pylab as plt
from tqdm import tqdm

def max_plot(re,axis):
    """最大値だけの折れ線グラフ"""
    max_data = []
    for i in range(len(axis)):
        max_data += [re[axis[i]]]
    max_data = np.array(max_data)
    plt.plot(axis,max_data,'o')
    return 0


def decision_peak(data,max_idx_tmp,width_thr):
    """ピーク間隔の閾値を考慮したピーク候補の決定"""
    max_idx = []
    i = 0
    while i < len(max_idx_tmp):
        dis = 0
        loop_flag = 0
        j = i+1
        while j < len(max_idx_tmp) and dis < width_thr:
            dis = max_idx_tmp[j] - max_idx_tmp[i]
            j += 1
            loop_flag = 1
        if loop_flag == 1:
            j -= 2
        else:
            j -= 1
        max_idx += [max_idx_tmp[i] + np.argmax(data[max_idx_tmp[i]:max_idx_tmp[j]+1])]
        i = j + 1
    max_idx = np.array(max_idx)

    return max_idx


def R_pick(data,height_thr,width_thr):
    """R波ピッキング"""
    # height_thr:振幅の閾値       この値以上のピークをピッキング
    # weight_thr:ピーク間隔の閾値  この値以上離れているピークを探す


    # 振幅閾値を超えるタイミングと下回るタイミングの取得
    up_idx = []
    down_idx = []
    up_flag = 0
    for i in range(len(data)):
        if data[i] > height_thr:
            if  i != 0 and data[i-1] <= height_thr and up_flag == 0:
                up_idx += [i]
                up_flag = 1
        else:
            if i != 0 and data[i-1] > height_thr and up_flag == 1:
                down_idx += [i]
                up_flag = 0

    up_idx = np.array(up_idx)
    down_idx = np.array(down_idx)

    if len(up_idx) > len(down_idx):
        up_idx = np.delete(up_idx,len(up_idx)-1)


    # 上記の振幅の閾値を上回るタイミングと下回るタイミング間でピークを検出
    max_idx_tmp = []
    for i in range(len(up_idx)):
        max_idx_tmp += [up_idx[i]+np.argmax(data[up_idx[i]:down_idx[i]+1])]
    max_idx_tmp = np.array(max_idx_tmp)


    # ピーク間のタイミングが閾値以上のピークを検出
    inf = True
    while inf:
        max_idx = decision_peak(data,max_idx_tmp,width_thr)
        if len(max_idx) == len(max_idx_tmp):
            break
        else:
            max_idx_tmp = max_idx

    # データ尾の整理
    if len(max_idx) > 1:
        if abs(max_idx[len(max_idx)-2] - max_idx[len(max_idx)-1]) < width_thr:
            max_idx[len(max_idx)-2] = max_idx[len(max_idx)-2] + np.argmax(data[max_idx[len(max_idx)-2]:max_idx[len(max_idx)-1]+1])
            max_idx = np.delete(max_idx,len(max_idx)-1)

    return max_idx
