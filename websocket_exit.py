import pprint
import json

import send_order_exit
import settings
import variables
import datetime
import websocket
import sys


class WebsocketExitC:

    def __init__(self):
        self.isException = True
        # トレーリングストップで使う最高値 or 最安値
        self.peak_value = None

    def on_message(self, ws, message):
        self.print_with_time('--- RECV MSG. --- ')
        content = json.loads(message)
        cur_price = content["CurrentPrice"]
        if cur_price is None:
            return

        pprint.pprint("curPrice:" + str(cur_price))

        # トレーリングストップ
        if settings.side == 1:
            # 売建の場合最安値を保存
            if self.peak_value is None or cur_price < self.peak_value:
                self.peak_value = cur_price
            # 現在値が、最安値 + 指定された%を超えたら返済
            if cur_price >= self.peak_value * (1 + settings.trailing_stop_ratio):
                # 日通しで注文するために十分な値幅を取った指値にする
                variables.exit_limit_value = cur_price + settings.limit_order_margin
                self.settle()
        else:
            # 買建の場合最高値を保存
            if self.peak_value is None or cur_price > self.peak_value:
                self.peak_value = cur_price
            # 現在値が、最高値 - 指定された%を超えたら返済
            if cur_price <= self.peak_value * (1 - settings.trailing_stop_ratio):
                # 日通しで注文するために十分な値幅を取った指値にする
                variables.exit_limit_value = cur_price - settings.limit_order_margin
                self.settle()

        pprint.pprint("peakPrice:" + str(self.peak_value))

    # 返済
    def settle(self):
        self.isException = False

        # イクジット
        send_order_exit.send_order_exit()

    def on_error(self, ws, error):
        if len(error) != 0:
            self.print_with_time('--- ERROR --- ')
            print(error)

    def on_close(self, ws):
        self.print_with_time('--- DISCONNECTED --- ')

    def on_open(self, ws):
        self.print_with_time('--- CONNECTED --- ')

    def websocket_exit_a(self):
        self.print_with_time('--- webSocket_exit Start--- ')
        url = 'ws://localhost:' + settings.port + '/kabusapi/websocket'
        # websocket.enableTrace(True)
        ws = websocket.WebSocketApp(url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

        self.print_with_time('--- websocket_exit --- ')

        if self.isException:
            print("exit")
            sys.exit()

    @staticmethod
    def print_with_time(message):
        print(str(datetime.datetime.now()) + ' ' + message)
