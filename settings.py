port = "18080"
exchange = 2
# 注文パスワード
password = ""
# APIパスワード
apiPassword = ""
symbol = "167030018"
side = 1
if side == 1:
    opposite_side = 2
else:
    opposite_side = 1
limit_price = 26430
qty = 4
# トレーリングストップの割合を%で指定
trailing_stop_ratio = 1
# 指値注文で返済注文をする際の気配値からの値幅(絶対に約定するように余裕を持たせる
exit_limit_value = 1000
settlement_check_interval = 10
