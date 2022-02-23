import urllib.request
import urllib.error
import json
import pprint
import settings
import variables
import sys


def send_order_entry():

    obj = {'Password': settings.password,
           'Symbol': settings.symbol,
           'Exchange': 2,
           'TradeType': 1,
           'TimeInForce': 1,
           'Side': settings.side,
           'Qty': settings.qty,
           'FrontOrderType': 20,
           'Price': settings.limit_price,
           'ExpireDay': 0}

    json_data = json.dumps(obj).encode('utf-8')

    url = 'http://localhost:' + settings.port + '/kabusapi/sendorder/future'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', variables.token)

    try:
        print('###sendorder_entry')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)

            # エントリ注文の注文IDを保存
            variables.entryOrderID = content['OrderId']
            # 返済用建玉数を初期設定
            variables.exitQty = settings.qty

            return

    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

    sys.exit()
