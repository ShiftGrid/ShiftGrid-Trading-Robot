symbolf = symbol + base
base_url = "https://api.bitget.com"
def gen_sign(method, endpoint, payload_string):
    timestamp = str(int(time.time() * 1000) + timest_corr)
    message = timestamp + method + endpoint + payload_string    
    signature = base64.b64encode(hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest())    
    headers = {
        "ACCESS-KEY": api_key,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json"
    }
    return headers
def get_price(symbolf, depth, layer):
    global ping
    time.sleep(ping / 10)
    try:
        endpoint = "/api/v2/spot/market/orderbook?symbol=" + symbolf + "&type=step0&limit=" + str(depth)
        res = requests.get(base_url + endpoint).json()
        ask = res["data"]["asks"][layer][0]
        bid = res["data"]["bids"][layer][0]
    except Exception:
        print(R + " API access or network connection problem")
        time.sleep(2)
        __main__()
    return ask, bid
def get_volume():
    global base_quant
    depth = 2
    layer = 1
    price = get_price(symbolf, depth, layer)
    price = (float(price[0]) + float(price[1])) / 2
    deal_volume = base_quant / price
    return deal_volume
def get_real_price(symbolf, deal_volume):
    global ping
    global quantityRound
    global priceRound
    time.sleep(ping / 10)
    depth = 500
    deal_price_ask = ""
    deal_price_bid = "" 
    try:     
        endpoint = "/api/v2/spot/market/orderbook?symbol=" + symbolf + "&type=step0&limit=" + str(depth)
        res = requests.get(base_url + endpoint).json()
        ask_vol = 0.0
        bid_vol = 0.0
        i = 0
        while ask_vol < deal_volume:
            ask = res["data"]["asks"][i][0]
            ask_vol = float(res["data"]["asks"][i][1])
            deal_price_ask = ask
            i += 1                  
        i = 0
        while bid_vol < deal_volume:
            bid = res["data"]["bids"][i][0]
            bid_vol = float(res["data"]["bids"][i][1])
            deal_price_bid = bid
            i += 1 
    except Exception:
        print(R + " API access or network connection problem")
        time.sleep(2)
        __main__()
    try:
        quantityRound = bid_vol
        quantityRound = int(len(str(quantityRound).split('.')[1]))
    except Exception:
        quantityRound = 0
    try:
        priceRound = deal_price_bid
        priceRound = int(len(str(priceRound).split('.')[1]))
    except Exception:
        priceRound = 0 
    return deal_price_ask, deal_price_bid
def get_balance(symbol):
    global ping
    time.sleep(ping / 10)
    try:
        endpoint = "/api/v2/spot/account/assets?coin=" + symbol
        payload_string = ''
        method = "GET"
        headers = gen_sign(method, endpoint, payload_string)
        response = requests.get(base_url + endpoint, headers=headers, data=payload_string).json()
        bal = response["data"][0]["available"]
        res = response["data"][0]["frozen"]
    except Exception:
        print(R + " API access or network connection problem")
        time.sleep(2)
        __main__()
    return bal, res
def get_active_order(order_id):
    global ping
    time.sleep(ping / 10)
    try:
        endpoint = "/api/v2/spot/trade/unfilled-orders?orderId=" + order_id
        payload_string = ''
        method = "GET"
        headers = gen_sign(method, endpoint, payload_string)
        response = requests.get(base_url + endpoint, headers=headers, data=payload_string).json()
        act = response["data"][0]["orderId"]
    except Exception:
        act = "Not found"
    if response["data"] == []:
        act = "Not found"        
    return act
def get_order_price(order_id):
    global ping
    time.sleep(ping / 10)
    try:
        endpoint = "/api/v2/spot/trade/unfilled-orders?orderId=" + order_id
        payload_string = ''
        method = "GET"
        headers = gen_sign(method, endpoint, payload_string)
        response = requests.get(base_url + endpoint, headers=headers, data=payload_string).json()
        prc = response["data"][0]["priceAvg"]
        prc = str(prc)
        if response["data"] == []:
            prc = "Not found"
    except Exception:
        prc = "Not found"
    return prc
def place_order(side, quantity, orderPrice):
    global ping
    time.sleep(ping / 10)
    depth = 3
    layer = 2
    price = float(get_price(symbolf, depth, layer)[0])
    base_quant = int(ass_quant * price)
    deal_volume = get_volume()
    get_real_price(symbolf, deal_volume)
    try:
        endpoint = "/api/v2/spot/trade/place-order"
        method = "POST"
        fm_pr = "{:." + str(priceRound) + "f}"
        fm_qt = "{:." + str(quantityRound) + "f}"
        payload_string = '{"symbol":"' + symbolf + '","side":"' + side + \
                    '","orderType":"limit","force":"gtc","price":"' + \
                    str(fm_pr.format(round(orderPrice, priceRound))) + '","size":"' + str(fm_qt.format(int(quantity * (10 ** quantityRound))/(10 ** quantityRound))) + '"}'
        headers = gen_sign(method, endpoint, payload_string)
        res = requests.post(base_url + endpoint, headers=headers, data=payload_string).json()
        try:
            suss = res["msg"]
            if "less than the minimum" in suss:
                print(R + " Insufficient transaction volume!")
                time.sleep(3)
                sys.exit()
        except Exception:
            pass
        order_id = res["data"]["orderId"]
        order_id = str(order_id)
    except Exception:
        order_id = "Not found"
    return order_id
def cancel_all(symbolf):
    global ping
    time.sleep(ping / 10)
    try:
        endpoint = "/api/v2/spot/trade/cancel-symbol-order"
        payload_string = '{"symbol":"' + symbolf + '"}'
        method = "POST"
        headers = gen_sign(method, endpoint, payload_string)
        response = requests.post(base_url + endpoint, headers=headers, data=payload_string).json()
    except Exception:
        pass
def transfer(transfer_amount):
    global ping
    time.sleep(ping / 10)
    try:
        endpoint = "/api/v2/spot/wallet/transfer"
        payload_string = '{"fromType":"spot","toType":"usdt_futures","amount":"' \
                        + str(transfer_amount) + '","coin":"'+ base + '"}'
        method = "POST"
        headers = gen_sign(method, endpoint, payload_string)
        res = requests.post(base_url + endpoint, headers=headers, data=payload_string).json()
    except Exception:
        pass
def get_wallet():
    global ping
    time.sleep(ping / 10)
    try:
        endpoint = "/api/v2/mix/account/account?symbol=btcusdt&productType=USDT-FUTURES&marginCoin=usdt"
        payload_string = ''
        method = "GET"
        headers = gen_sign(method, endpoint, payload_string)
        wallet = requests.get(base_url + endpoint, headers=headers, data=payload_string).json()
        wallet = wallet["data"]["available"]
    except Exception:
        print(R + " API access or network connection problem")
        time.sleep(2)
        __main__()
    return wallet



