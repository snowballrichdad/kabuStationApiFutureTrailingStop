# kabuStationApiFutureTrailingStop
auカブコム証券のkabuステーションAPIを利用した先物取引のトレーリングストッププログラムです。
建玉管理をして、このプログラムから発注した注文と、手動や他のプログラムから発注した注文が混同しないようにしています。
よかったら参考にしてください。

# プログラムの流れ
1. setting.pyで指定した価格、売買方向で指値注文
2. 全約定したらトレーリングストップを開始。最高値(最安値)から指定した%下落(上昇)したら決済
