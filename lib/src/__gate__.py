symbolf = symbol + "_" + base
host = "https://api.gateio.ws"
prefix = "/api/v4"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
key = api_key
secret = secret_key
def gen_sign(method, url, query_string=None, payload_string=None):    
    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", \
                                hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), \
                    hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}
def get_price(symbolf, depth, layer):
    global ping
    time.sleep(ping / 10)
    try:
        url = '/spot/order_book'
        query_param = 'currency_pair=' + symbolf  + '&limit=' + str(depth)
        r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers, verify=False).json()
        ask = r['asks'][layer][0]
        bid = r['bids'][layer][0]
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
        url = '/spot/order_book'
        query_param = 'currency_pair=' + symbolf  + '&limit=' + str(depth) + '&limit=500'
        r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers, verify=False).json()
        ask_vol = 0.0
        bid_vol = 0.0
        i = 0
        while ask_vol < deal_volume:
            ask = r["asks"][i][0]
            ask_vol = float(r["asks"][i][1])
            deal_price_ask = ask
            i += 1                  
        i = 0
        while bid_vol < deal_volume:
            bid = r["bids"][i][0]
            bid_vol = float(r["bids"][i][1])
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
        url = '/spot/accounts'
        query_param = 'currency=' + symbol
        sign_headers = gen_sign('GET', prefix + url, query_param)
        headers.update(sign_headers)
        b = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers, verify=False).json()
        bal = b[0]['available']
        res = b[0]['locked']
    except Exception:
        print(R + " API access or network connection problem")
        time.sleep(2)
        __main__()
    return bal, res
def get_active_order(order_id):
    global ping
    time.sleep(ping / 10)
    try:
        status = ""
        url = '/spot/orders/' + order_id
        query_param = 'currency_pair=' + symbolf
        sign_headers = gen_sign('GET', prefix + url, query_param)
        headers.update(sign_headers)
        act = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers, verify=False).json()
        status = act['status']
        act = act['id']
    except Exception:
        act = "not found"
    act = str(act)
    index = act.find("not found")
    if index != -1 or status == "closed" or status == "cancelled":
        act = "Not found"
    return act
def get_order_price(order_id):
    global ping
    time.sleep(ping / 10)
    try:
        url = '/spot/orders/' + order_id
        query_param = 'currency_pair=' + symbolf
        sign_headers = gen_sign('GET', prefix + url, query_param)
        headers.update(sign_headers)
        prc = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers, verify=False).json()
        prc = prc['price']       
    except Exception:
        pass
    prc = str(prc)
    index = prc.find("not found")
    if index != -1:
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
        url = '/spot/orders'
        query_param = ''
        fm_pr = "{:." + str(priceRound) + "f}"
        fm_qt = "{:." + str(quantityRound) + "f}"
        body = '{"text":"t-123456","currency_pair":"' + symbolf \
               + '","type":"limit","account":"spot","side":"' \
               + side + '","iceberg":"0","amount":"' + str(fm_qt.format(int(quantity * (10 ** quantityRound))/(10 ** quantityRound))) + '","price":"'\
               + str(fm_pr.format(round(orderPrice, priceRound))) + '","time_in_force":"gtc"}'
        sign_headers = gen_sign('POST', prefix + url, query_param, body)
        headers.update(sign_headers)
        order_id = requests.request('POST', host + prefix + url, headers=headers, data=body, verify=False).json()
        try:
            suss = order_id["message"]
            if "minimum is" in suss:
                print(R + " Insufficient transaction volume!")
                time.sleep(3)
                sys.exit()         
        except Exception:
            pass
        order_id = order_id["id"]
    except Exception:
        order_id = "not found"
    order_id = str(order_id)
    index = order_id.find("not found")
    if index != -1:
        order_id = "Not found"    
    return order_id
def cancel_all(symbolf):
    global ping
    time.sleep(ping / 10)
    try:
        url = '/spot/orders'
        query_param = 'currency_pair=' + symbolf
        sign_headers = gen_sign('DELETE', prefix + url, query_param)
        headers.update(sign_headers)
        cancel = requests.request('DELETE', host + prefix + url + "?" + query_param, headers=headers, verify=False).json()
    except Exception:
        pass
def transfer(transfer_amount):
    global ping
    time.sleep(ping / 10)
    try:
        pair = "BTC_" + base
        url = '/wallet/transfers'
        query_param = ''
        body = '{"currency":"' + base + '","from":"spot","to":"margin","amount":"' + \
               str(transfer_amount) + '","currency_pair":"' + pair + '"}'
        sign_headers = gen_sign('POST', prefix + url, query_param, body)
        headers.update(sign_headers)
        r = requests.request('POST', host + prefix + url, headers=headers, data=body, verify=False)
    except Exception:
        pass
def get_wallet():
    try:
        url = '/margin/accounts'
        query_param = ''
        sign_headers = gen_sign('GET', prefix + url, query_param)
        headers.update(sign_headers)
        wallet = requests.request('GET', host + prefix + url, headers=headers, verify=False).json()
        wallet = wallet[0]['quote']['available']
    except Exception:
        print(R + " API access or network connection problem")
        time.sleep(2)
        __main__()
    return wallet   
