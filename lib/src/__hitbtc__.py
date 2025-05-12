symbolf = symbol + base
def get_price(symbolf, depth, layer):
    global ping
    time.sleep(ping / 10)
    try:
        rec = requests.get("https://api.hitbtc.com/api/3/public/orderbook/" + \
                               symbolf + "?depth=" + str(depth)).json()
        ask = rec["ask"][layer][0]
        bid = rec["bid"][layer][0]       
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
        rec = requests.get("https://api.hitbtc.com/api/3/public/orderbook/" + \
                               symbolf + "?depth=" + str(depth)).json()        
        ask_vol = 0.0
        bid_vol = 0.0
        i = 0
        while ask_vol < deal_volume:
            ask = rec["ask"][i][0]
            ask_vol = float(rec["ask"][i][1])
            deal_price_ask = ask
            i += 1           
        i = 0
        while bid_vol < deal_volume:
            bid = rec["bid"][i][0]
            bid_vol = float(rec["bid"][i][1])
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
        session = requests.session()
        session.auth = (api_key, secret_key)
        b = session.get("https://api.hitbtc.com/api/3/spot/balance/" + \
                            symbol).json()
        bal = b["available"]
        res = b["reserved"]        
    except Exception:
        print(R + " API access or network connection problem")
        time.sleep(2)
        __main__()
    return bal, res
def get_active_order(order_id):
    global ping
    time.sleep(ping / 10)
    try:
        session = requests.session()
        session.auth = (api_key, secret_key)
        act = session.get("https://api.hitbtc.com/api/3/spot/order/" + order_id).json()
        act = act["client_order_id"]       
    except Exception:
        act = "Not found"
    act = str(act)
    index = act.find("error")
    if index != -1:
        act = "Not found"
    return act
def get_order_price(order_id):
    global ping
    time.sleep(ping / 10)
    try:
        session = requests.session()
        session.auth = (api_key, secret_key)
        prc = session.get("https://api.hitbtc.com/api/3/spot/order/" + order_id).json()
        prc = prc["price"]       
        prc = str(prc)
        index = prc.find("error")
        if index != -1:
            prc = "Not found"
    except Exception:
        pass    
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
        session = requests.session()
        session.auth = (api_key, secret_key)
        fm_pr = "{:." + str(priceRound) + "f}"
        fm_qt = "{:." + str(quantityRound) + "f}"
        orderData = {'symbol': symbolf, 'side': side, \
                     'quantity': str(fm_qt.format(int(quantity * (10 ** quantityRound))/(10 ** quantityRound))), 'price': str(fm_pr.format(round(orderPrice, priceRound)))}
        order_id = session.post("https://api.hitbtc.com/api/3/spot/order/", \
                         data = orderData).json()
        order_id = order_id["client_order_id"]
        order_id = str(order_id)
        index = order_id.find("error")
        if index != -1:
            order_id = "Not found"
    except Exception:
        pass    
    return order_id
def cancel_all(symbolf):
    time.sleep(ping / 10)
    try:
        session = requests.session()
        session.auth = (api_key, secret_key)
        cancel = session.delete("https://api.hitbtc.com/api/3/spot/order?symbol=" + symbolf).json()
    except Exception:
        pass
def transfer(transfer_amount):
    global ping
    time.sleep(ping / 10)
    try:    
        session = requests.session()
        session.auth = (api_key, secret_key)
        transferData = {'currency': base, 'amount': str(transfer_amount), \
                     'source':'spot', 'destination':'wallet'}
        res = session.post("https://api.hitbtc.com/api/3/wallet/transfer", \
                         data = transferData).json()
    except Exception:
        pass
def get_wallet():
    try:
        session = requests.session()
        session.auth = (api_key, secret_key)
        wallet = session.get("https://api.hitbtc.com/api/3/wallet/balance/" + \
                            base).json()
        wallet = wallet['available']
    except Exception:
        print(R + " API access or network connection problem")
        time.sleep(2)
        __main__()
    return wallet
