# Making_ECG_BasicWave

心電図波形(ECG)を基本波形ごとに分割する処理  
R波を探し出すことで「そこから前後に何点の区間を抽出」というアプローチ

使用言語: python3  
必要ライブラリ
```
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
```

実行する際は  
`python3 Make_BasicWave`


ここでは1人の健常者の12誘導心電図の"I","II"誘導のみを扱っている。  
使用した心電図データは以下URLである。
https://physionet.org/physiobank/database/ptbdb/

前処理としてトレンド除去、ノイズ除去を行なっている。  
次にR波をピッキングし、そこから前200点、後450点の合計651点を抽出した。  
R波をピッキングする際には「振幅の閾値」、及び「ピーク間隔の閾値」を情報として設定した。
