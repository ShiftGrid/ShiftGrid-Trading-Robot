symbolf = symbol + base
http_client = requests.Session()
recv_window = str(5000)
base_url = "https://api.bybit.com"
def http_req(endpoint, method, payload):
    global time_stamp
    time_stamp = str(int(time.time() * 10 ** 3) + timest_corr)
    signature = gen_sign(payload)
    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }
    if(method == "POST"):
        response = http_client.request(method, base_url + endpoint, headers = headers, data = payload, verify=False)
    else:
        response = http_client.request(method, base_url + endpoint + "?" + payload, headers = headers, verify=False)    
    return response
def gen_sign(payload):
    param_str= str(time_stamp) + api_key + recv_window + payload
    hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
    signature = hash.hexdigest()
    return signature
def get_price(symbolf, depth, layer):
    global ping
    time.sleep(ping / 10)
    try:
        endpoint = "/v5/market/orderbook"
        method = "GET"
        params = 'category=' + 'spot' + '&symbol=' + symbolf + '&limit=' + str(depth)
        res = http_req(endpoint, method, params).json()
        ask = res["result"]['a'][layer][0]
        bid = res["result"]['b'][layer][0]
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
        endpoint = "/v5/market/orderbook"
        method = "GET"
        params = 'category=' + 'spot' + '&symbol=' + symbolf + '&limit=' + str(depth)
        res = http_req(endpoint, method, params).json()
        ask_vol = 0.0
        bid_vol = 0.0
        i = 0
        while ask_vol < deal_volume:
            ask = res["result"]['a'][i][0]
            ask_vol = float(res["result"]['a'][i][1])
            deal_price_ask = ask
            i += 1                  
        i = 0
        while bid_vol < deal_volume:
            bid = res["result"]["b"][i][0]
            bid_vol = float(res["result"]["b"][i][1])
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
    return deal_price_ask, deal_price_bid, priceRound, quantityRound
def get_quant_round(symbolf):
    global ping
    global quantityRound
    time.sleep(ping / 10)
    depth = 50
    deal_price_ask = ""
    deal_price_bid = "" 
    try:     
        endpoint = "/v5/market/orderbook"
        method = "GET"
        params = 'category=' + 'spot' + '&symbol=' + symbolf + '&limit=' + str(depth)
        res = http_req(endpoint, method, params).json()
        bid_vol = 0.0                
        i = 0
        while bid_vol <= 0:
            bid = res["result"]["b"][i][0]
            bid_vol = float(res["result"]["b"][i][1])
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
    return quantityRound    
def get_balance(symbol):
    global ping
    get_quant_round(symbolf)
    time.sleep(ping / 10)
    if account_type == "CLASSIC":
        acc_type = 'SPOT'
    else:
        acc_type = 'UNIFIED'
    try:
        endpoint = "/v5/account/wallet-balance"
        method = "GET"
        params = 'accountType=' + acc_type + '&coin=' + symbol
        response = http_req(endpoint, method, params).json()
        bal = response["result"]["list"][0]["coin"]
        res = response["result"]["list"][0]["coin"]
        if bal == [] or res == []:
            bal = 0
            res = 0
        else:
            if account_type == "CLASSIC":
                bal = response["result"]["list"][0]["coin"][0]["free"]
                res = response["result"]["list"][0]["coin"][0]["locked"]
            else:
                bal = response["result"]["list"][0]["coin"][0]["walletBalance"]
                res = response["result"]["list"][0]["coin"][0]["locked"]
                bal = float(bal) - float(res)
                fm_qt = "{:." + str(quantityRound) + "f}"
                bal = str(fm_qt.format(int(bal * (10 ** quantityRound))/(10 ** quantityRound)))
    except Exception:
        print(R + " API access or network connection problem")
        time.sleep(2)
        __main__()
    return bal, res
def get_active_order(order_id):
    global ping
    time.sleep(ping / 10)
    try:
        endpoint = "/v5/order/realtime"
        method = "GET"
        params = 'category=' + 'spot' + '&orderId=' + str(order_id)
        response = http_req(endpoint, method, params).json()
        act = response["result"]["list"][0]["orderId"]
        status = response["result"]["list"][0]["orderStatus"]
        if status == "Filled" or status == "Cancelled" or status == "Rejected":
            act = "Not found"
    except Exception:
        act = "Not found"
    return act
def get_order_price(order_id):
    global ping
    time.sleep(ping / 10)
    try:
        endpoint = "/v5/order/realtime"
        method = "GET"
        params = 'category=' + 'spot' + '&orderId=' + str(order_id)
        response = http_req(endpoint, method, params).json()
        prc = response["result"]["list"][0]["price"]
        status = response["result"]["list"][0]["orderStatus"]
        if status == "Filled" or status == "Cancelled" or status == "Rejected":
            prc = "Not found"
    except Exception:
        prc = "Not found"
    return prc
def place_order(side, quantity, orderPrice):
    global ping
    global quantityRound
    global priceRound
    time.sleep(ping / 10)
    depth = 3
    layer = 2
    price = float(get_price(symbolf, depth, layer)[0])
    base_quant = int(ass_quant * price)
    deal_volume = get_volume()
    get_real_price(symbolf, deal_volume)
    try:
        endpoint = "/v5/order/create"
        method = "POST"
        fm_pr = "{:." + str(priceRound) + "f}"
        fm_qt = "{:." + str(quantityRound) + "f}"
        params = '{"category":"spot","symbol":"' + symbolf + \
                 '","side":"' + side + '","orderType":"Limit","qty":"' + \
                 str(fm_qt.format(int(quantity * (10 ** quantityRound))/(10 ** quantityRound))) + \
                 '","price":"' + str(fm_pr.format(round(orderPrice, priceRound))) + '"}'
        res = http_req(endpoint, method, params)
        try:
            rst = res.json()
            suss = rst["retMsg"]
            if "quantity exceeded lower" in suss:
                print(R + " Insufficient transaction volume!")
                time.sleep(3)
                sys.exit()                    
        except Exception:
            pass
        order_id = res.json()["result"]["orderId"]
        order_id = str(order_id)
    except Exception:
        order_id = "Not found"
    return order_id
def cancel_all(symbolf):
    global ping
    time.sleep(ping / 10)
    try:
        endpoint = "/v5/order/cancel-all"
        method = "POST"
        params = '{"category":"spot","symbol":"' +  symbolf +'"}'
        response = http_req(endpoint, method, params)
    except Exception:
        pass    
def transfer(transfer_amount):
    global ping
    time.sleep(ping / 10)
    if account_type == "CLASSIC":
        acc_type = 'SPOT'
    else:
        acc_type = 'UNIFIED'
    try:
        tr_uuid = str(uuid.uuid4())
        endpoint = "/v5/asset/transfer/inter-transfer"
        method = "POST"
        params = '{"transferId":"' + tr_uuid + '","coin":"USDT","amount":"' + str(transfer_amount) + \
                 '","fromAccountType":"' + acc_type + '","toAccountType":"FUND"}'
        result = http_req(endpoint, method, params)
    except Exception:
        pass   
def get_wallet():
    global ping
    time.sleep(ping / 10)
    try:
        endpoint = "/v5/asset/transfer/query-account-coin-balance"
        method = "GET"
        params = 'accountType=' + 'FUND' + '&coin=USDT'
        wallet = http_req(endpoint, method, params).json()
        wallet = wallet["result"]["balance"]["walletBalance"]
    except Exception:
        print(R + " API access or network connection problem")
        time.sleep(2)
        __main__()
    return wallet   
