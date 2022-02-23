import urllib.request
import urllib.error
import json
import pprint
import settings
import variables
import sys


def send_order_exit():
    obj = {'Password': settings.password,
           'Symbol': settings.symbol,
           'Exchange': 2,
           'TradeType': 2,
           'TimeInForce': 1,
           'Side': settings.opposite_side,
           'Qty': variables.exitQty,
           'ClosePositions': variables.closePositions,
           'FrontOrderType': 20,
           'Price': variables.exit_limit_value,
           'ExpireDay': 0}
    json_data = json.dumps(obj).encode('utf-8')

    url = 'http://localhost:' + settings.port + '/kabusapi/sendorder/future'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', variables.token)

    try:
        print('###settle_now')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)

            return

    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
        # 決済内容に誤りがあります はポジション取得遅延のせいなので無視
        if content['Code'] == 8:
            return

    except Exception as e:
        print(e)

    sys.exit()
