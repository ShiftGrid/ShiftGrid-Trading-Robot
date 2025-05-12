import os
import sys
import warnings
import requests
import hashlib
import hmac
import uuid
import base64
import shutil
import math
import random
import time
from time import gmtime, strftime
import ntplib
import datetime
import json
from io import StringIO
import winsound
from threading import Thread
import colorama
from colorama import init
from colorama import Fore, Back, Style
import ctypes
from ctypes import *
import requests

class CONSOLE_CURSOR_INFO(Structure):
    _fields_ = [('dwSize', c_int),
                ('bVisible', c_int)]
LF_FACESIZE = 32    
STD_OUTPUT_HANDLE = -11
hStdOut = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
cursorInfo = CONSOLE_CURSOR_INFO()
cursorInfo.dwSize = 1
cursorInfo.bVisible = 0
windll.kernel32.SetConsoleCursorInfo(hStdOut, byref(cursorInfo))
class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * LF_FACESIZE)]    
font = CONSOLE_FONT_INFOEX()
font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
font.nFont = 12
font.dwFontSize.X = 8
font.dwFontSize.Y = 12
handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))
M = Fore.MAGENTA + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
G = Fore.GREEN + Style.BRIGHT
Y = Fore.YELLOW + Style.DIM
B = Fore.BLUE + Style.BRIGHT
R = Fore.RED + Style.NORMAL
W = Fore.WHITE + Style.NORMAL
RD = Fore.RED + Style.DIM

try:
    fc = open('settings.cfg', 'r')
    params = fc.read()
    fc.close()
except Exception:
    print("")
    print(R + " Cfg file is not exist")
    input()
try:
    key_params = params.split("\"")[1::2]
    exchange = key_params[0]
    account_type = key_params[1]
    api_key = key_params[2]
    secret_key = key_params[3]
    passphrase = key_params[4]
    base = key_params[5]
    symbol = key_params[6]
    grids_num = int(key_params[7])
    tp_prc = float(key_params[8])
    grid = float(key_params[9].split('/')[0])
    grid_mode = key_params[10]
    if grid_mode == "CUSTOM":
        grid_bias = "AUTO"
    else:    
        grid_bias = float(key_params[11])
    ini_amount = float(key_params[12].split('/')[0]) / 100
    ping = int(key_params[13])
    ping = random.randint(int(0.8 * ping),int(1.2 * ping))
    sounds = key_params[14]
    middle_multiplier = key_params[15]
    middle_band = float(key_params[16]) / 100
    middle_factor = float(key_params[17])
    withdraw = key_params[18]
    wdr_prc = float(key_params[19]) / 100
    time_delay = int(key_params[20])
    make_sure = int(key_params[21])
    wd_time = int(key_params[22])
    wd_switch = key_params[23]
    fail_attempt = int(key_params[24])
    timest_corr = int(key_params[25])
    err_counter = 0
    fail_counter = 0
except Exception:
    print("")
    print(R + " Check Cfg file!")
    input()

try:
    f = open("tmp/buy_id.txt", "x")
    f.close()
except Exception:
    pass
try:
    f = open("tmp/sell_id.txt", "x")
    f.close()
except Exception:
    pass
try:
    f = open("tmp/grid.txt", "x")
    f.close()
except Exception:
    pass
try:
    f = open("log.txt", "x")
    f.close()
except Exception:
    pass
try:
    f = open("tmp/buy_count.txt", "x")
    f.close()
except Exception:
    pass
try:
    f = open("tmp/sell_count.txt", "x")
    f.close()
except Exception:
    pass
try:
    f = open("tmp/mult_f.txt", "x")
    f.close()
except Exception:
    pass
try:
    f = open("tmp/strt_b.txt", "x")
    f.close()
except Exception:
    pass
try:
    f = open("tmp/ini_am.txt", "x")
    f.close()
except Exception:
    pass

def disable_quick_edit_mode():
    kernel32 = ctypes.WinDLL('kernel32')
    dword_for_std_input_handle = ctypes.wintypes.DWORD(-10)
    dword_for_enable_extended_flags = ctypes.wintypes.DWORD(0x0080)
    std_input_handle = kernel32.GetStdHandle(dword_for_std_input_handle)
    kernel32.SetConsoleMode(std_input_handle, dword_for_enable_extended_flags)
    last_error = kernel32.GetLastError()
    return last_error
disable_quick_edit_mode()

def prt_scr():
    try:
        print('\033[?25l', end="")
        os.system("cls")
        print("")
        print(M + " ShiftGrid ver.2.6.3 trading robot is working")
        print(" Exchange: ", C + exchange)
        print(strftime(G + " %Y-%m-%d %H:%M UTC" + Style.RESET_ALL, gmtime()), Y + f_mess)
        print(B + " Asset:          ", W + symbol)
        print(B + " Grid mode:      ", W + grid_mode)
        print(B + " Grid bias:      ", W + str(grid_bias))
        print(B + " Next grid step: ", W + "{:10.3f}".format(float(grid)), " %")
        print(B + " TakeProfit:     ", W + "{:10.3f}".format(float(tp_prc)), " %") 
        print(B + " Current price:  ", W + fmt.format(curr_price), "", base)
        if buy_price == "Not found":
            print(B + " Buy price:      ", RD + "No orders")
        else:
            log_buy_price = fmt.format(float(buy_price))
            print(B + " Buy price:      ", W + log_buy_price, "", base)
        if sell_price == "Not found":
            print(B + " Sell price:     ", RD + "No orders")
        else:
            log_sell_price = fmt.format(float(sell_price))
            print(B + " Sell price:     ", W + log_sell_price, "", base)                      
        if withdraw == "ON":
            print(B + " Total funds:    ", W + "{:10.3f}".format(total_balance + wallet), "", base)
            print(B + " Funds in stock: ", W + "{:10.3f}".format(total_balance), "", base)
            print(B + " Wallet:         ", W + "{:10.3f}".format(wallet), "", base)
        else:
            print(B + " Total funds:    ", W + "{:10.3f}".format(total_balance + wallet), "", base)
            print(B + " Funds at start: ", W + "{:10.3f}".format(strt_bal), "", base)
            PnL = ((total_balance + wallet - strt_bal) / strt_bal) * 100
            print(B + " Round PnL:      ", W + "{:10.3f}".format(PnL), " %")
    except Exception:
        os.system("cls")
        print(B + " Waiting...")

def init_sell():
    global ass_quant
    global base_quant
    global ass_balance
    global base_balance
    global ping
    global err_counter
    ping = 1
    buy_sell()
    try:
        depth = 2
        layer = 1
        price = float(get_price(symbolf, depth, layer)[0])
        base_quant = round(ass_quant * price, 2)
        base_delta = wdr_prc * base_quant
        cancel_all(symbolf)
        try:
            base_balance = float(get_balance(base)[0]) - base_delta
        except Exception:
            base_balance = 0.0
        if base_balance < base_quant:
            deal_volume = get_volume()
            price = float(get_real_price(symbolf, deal_volume)[1])
            t = strftime("%Y-%m-%d %H:%M UTC", gmtime())
            f = open("log.txt", "r")
            last_string = str(f.readlines()[-1])
            if "started" in last_string:
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                try:
                    ini_amount = float(key_params[12].split('/')[1]) / 100  
                except Exception:
                    ini_amount = float(key_params[12].split('/')[0]) / 100    
            else:
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                ini_amount = float(key_params[12].split('/')[0]) / 100
            isempty = os.stat('tmp/ini_am.txt').st_size == 0
            if isempty == False:
                f = open("tmp/ini_am.txt", "r")
                ini_amount = float(f.read())
                f.close()
            QRound = int(grids_num * ini_amount)
            if QRound == 0:
                QRound = 1
            write_ap_file("log.txt", t + " Initial sell " + str(QRound * ass_quant) + " " + symbol + " for " + str(price), "a") 
            sell = place_order("sell", QRound * ass_quant, price)
            print(" INITIAL SELL!") 
            time.sleep(time_delay)
        for i in range(make_sure):
            check = str(get_active_order(sell))
            i += 1
        if check == "Not found":
            print(" Success!")
            with open("tmp/ini_am.txt", 'w'):
                pass
            wd_write(str(int(time.time())))
            fc = open('settings.cfg', 'r')
            params = fc.read()
            fc.close()
            key_params = params.split("\"")[1::2]
            ping = int(key_params[13])
            ping = random.randint(int(0.8 * ping),int(1.2 * ping))
             
        else:
            cancel_all(symbolf)
            wd_write(str(int(time.time())))
            print(" It didn't work out. Trying again")
            write_to_file("tmp/ini_am.txt", str(ini_amount), "w")
            write_ap_file("log.txt", t + " It didn't work out, started again", "a")
            fc = open('settings.cfg', 'r')
            params = fc.read()
            fc.close()
            key_params = params.split("\"")[1::2]
            ping = int(key_params[13])
            ping = random.randint(int(0.8 * ping),int(1.2 * ping))
             
    except Exception:
        time.sleep(10)
        print(R + " Error")
        err_counter += 1
        if err_counter > 10:
            os.system("shutdown /r /t 10 /f")
            sys.exit()
         
def init_buy():
    global ass_quant
    global base_quant
    global ass_balance
    global base_balance
    global ping
    global err_counter
    ping = 1
    buy_sell()
    try:
        depth = 2
        layer = 1
        price = float(get_price(symbolf, depth, layer)[0])
        base_quant = round(ass_quant * price, 2)
        base_delta = wdr_prc * base_quant
        cancel_all(symbolf)
        try:
            base_balance = float(get_balance(base)[0]) - base_delta
        except Exception:
            base_balance = 0.0
        if ass_balance < ass_quant:    
            deal_volume = get_volume()
            price = float(get_real_price(symbolf, deal_volume)[0])
            t = strftime("%Y-%m-%d %H:%M UTC", gmtime())
            if price > (1.015 * strt_prc):
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                try:
                    ini_amount = float(key_params[12].split('/')[2]) / 100
                except Exception:
                    ini_amount = float(key_params[12].split('/')[0]) / 100
                try:
                    funds()       
                    depth = 1
                    layer = 0 
                    c_price = get_price(symbolf, depth, layer)
                    curr_price = (float(c_price[0]) + float(c_price[1])) / 2
                    total_balance = ((ass_balance + res_balance) * curr_price) + base_balance + base_res_balance
                    write_ap_file("tmp/strt_b.txt", str(curr_price), "w")
                    r_lot = (total_balance / grids_num) / curr_price
                    ass_quant = round_all(r_lot)
                    write_ap_file("tmp/strt_b.txt", str(ass_quant), "a")
                    write_to_file("tmp/strt_b.txt", str(total_balance + wallet), "a")
                except Exception:
                    print(R + " API access or network connection problem")    
            else:
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                ini_amount = float(key_params[12].split('/')[0]) / 100        
            f = open("log.txt", "r")
            last_string = str(f.readlines()[-1])
            if "started" in last_string:
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                try:
                    ini_amount = float(key_params[12].split('/')[1]) / 100
                except Exception:
                    ini_amount = float(key_params[12].split('/')[0]) / 100
            isempty = os.stat('tmp/ini_am.txt').st_size == 0
            if isempty == False:
                f = open("tmp/ini_am.txt", "r")
                ini_amount = float(f.read())
                f.close()        
            QRound = int(grids_num * ini_amount)
            if QRound == 0:
                QRound = 1
            write_ap_file("log.txt", t +  " Initial buy " + str(QRound * ass_quant) + " " + symbol + " for " + str(price), "a")    
            buy = place_order("buy", QRound * ass_quant, price)     
            print(" INITIAL BUY!")
            time.sleep(time_delay)
        for i in range(make_sure):
            check = str(get_active_order(buy))
            i += 1
        if check == "Not found":
            print(" Success!")
            with open("tmp/ini_am.txt", 'w'):
                pass
            wd_write(str(int(time.time())))
            fc = open('settings.cfg', 'r')
            params = fc.read()
            fc.close()
            key_params = params.split("\"")[1::2]
            ping = int(key_params[13])
            ping = random.randint(int(0.8 * ping),int(1.2 * ping))
             
        else:
            wd_write(str(int(time.time())))
            cancel_all(symbolf)
            print(" It didn't work out. Trying again")
            write_to_file("tmp/ini_am.txt", str(ini_amount), "w")
            write_ap_file("log.txt", t + " It didn't work out, started again", "a")
            fc = open('settings.cfg', 'r')
            params = fc.read()
            fc.close()
            key_params = params.split("\"")[1::2]
            ping = int(key_params[13])
            ping = random.randint(int(0.8 * ping),int(1.2 * ping))
                 
    except Exception:
        time.sleep(10)
        print(R + " Error")
        err_counter += 1
        if err_counter > 10:
            os.system("shutdown /r /t 10 /f")
            sys.exit()
         
def init_trade():
    global buy_id
    global sell_id
    global tp_price
    global next_price
    global tp_prc
    global grid
    global grid_bias
    global grid_mode
    global ass_balance
    global base_balance
    global base_quant
    global ass_quant
    global base_delta
    global base_quant
    global ping
    global err_counter
    ping = 1
    buy_sell()
    sound()
    if exchange == "Gate.io":
        symbolf = symbol + "_" + base
    else:
        symbolf = symbol + base    
    fmt = "{:10." + str(priceRound) + "f}"
    print(Y + " Initial trade...")
    fc = open('settings.cfg', 'r')
    params = fc.read()
    fc.close()
    f = open("tmp/strt_b.txt", "r")  
    lines = f.readlines()      
    ass_quant = float(lines[1])  
    try:
        cancel_all(symbolf)
        depth = 2
        layer = 1
        price = float(get_price(symbolf, depth, layer)[0])
        try:
            ass_balance = float(get_balance(symbol)[0])
        except Exception:
            ass_balance = 0.0
        ass_doll_balance = ass_balance * price
        base_quant = round(ass_quant * price, 2)
        base_delta = wdr_prc * base_quant
        try:
            base_balance = float(get_balance(base)[0]) - base_delta
        except Exception:
            base_balance = 0.0
        mf = 1.0
        if middle_multiplier == "ON":
            if abs(base_balance - ass_doll_balance) < middle_band * (base_balance + ass_doll_balance):
                mf = middle_factor
            else:
                mf = 1.0
        if base_balance < base_quant:
            init_sell()
        if ass_balance < ass_quant:
            init_buy()
        if ass_doll_balance > base_balance:
            if ass_balance > ass_quant:
                print(" Replace sell order...")      
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                grid = float(key_params[9].split('/')[0])                        
                sell_price = price + (price / 100) * grid
                sell = place_order("sell", ass_quant * mf, sell_price)
                print(" Sell order replaced")
                print(" Replace buy order...")
                buy_price = price - (price / 100) * tp_prc
                buy = place_order("buy", ass_quant * mf, buy_price)
                print(" Buy order replaced")
                wd_write(str(int(time.time())))
                write_to_file("tmp/sell_id.txt", str(sell), "w")
                write_to_file("tmp/buy_id.txt", str(buy), "w")
                write_to_file("tmp/mult_f.txt", str(mf), "w")
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                ping = int(key_params[13])
                ping = random.randint(int(0.8 * ping),int(1.2 * ping))
                 
            else:
                print(" Insufficient funds for the transaction!")
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                ping = int(key_params[13])
                ping = random.randint(int(0.8 * ping),int(1.2 * ping))
                 
        else:
            if base_balance > base_quant:
                print(" Replace buy order...")
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                grid = float(key_params[9].split('/')[0])                        
                buy_price = price - (price / 100) * grid
                deal_volume = ass_quant * mf
                get_real_price(symbolf, deal_volume)
                buy = place_order("buy", ass_quant * mf, buy_price)
                print(" Buy order replaced")
                print(" Replace sell order...")
                sell_price = price + (price / 100) * tp_prc
                deal_volume = ass_quant * mf
                get_real_price(symbolf, deal_volume)
                sell = place_order("sell", ass_quant * mf, sell_price)
                print(" Sell order replaced")
                wd_write(str(int(time.time())))
                write_to_file("tmp/sell_id.txt", str(sell), "w")
                write_to_file("tmp/buy_id.txt", str(buy), "w")
                write_to_file("tmp/mult_f.txt", str(mf), "w")
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                ping = int(key_params[13])
                ping = random.randint(int(0.8 * ping),int(1.2 * ping))
                 
            else:
                print(" Insufficient funds for the transaction!")
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                ping = int(key_params[13])
                ping = random.randint(int(0.8 * ping),int(1.2 * ping))
                 
    except Exception:
        time.sleep(10)
        print(R + " Error")
        err_counter += 1
        if err_counter > 10:
            os.system("shutdown /r /t 10 /f")
            sys.exit()
         
def trade():
    global buy_id
    global sell_id
    global tp_price
    global next_price
    global tp_prc
    global grid
    global grid_bias
    global grid_mode
    global base_quant
    global ass_quant
    global base_delta
    global base_quant
    global log_buy_price
    global log_sell_price
    global ping
    global err_counter
    global fail_counter
    ping = 1
    buy_sell()
    sound()    
    print(Y + " Readiness...")
    if exchange == "Gate.io":
        symbolf = symbol + "_" + base
    else:
        symbolf = symbol + base
    fmt = "{:10." + str(priceRound) + "f}"
    fail_counter += 1
    if fail_counter > fail_attempt:
        os.system("shutdown /r /t 10 /f")
        sys.exit()  
    fc = open('settings.cfg', 'r')
    params = fc.read()
    fc.close()
    f = open("tmp/strt_b.txt", "r")  
    lines = f.readlines()      
    ass_quant = float(lines[1]) 
    f = open("tmp/sell_count.txt", "r")
    sell_count = float(f.read())
    f.close()
    f = open("tmp/buy_count.txt", "r")
    buy_count = float(f.read())
    f.close()
    f = open("tmp/mult_f.txt", "r")
    mf = float(f.read())
    f.close()
    try:
        depth = 2
        layer = 1
        price = float(get_price(symbolf, depth, layer)[0])
        sell = get_active_order(sell_id)
        buy = get_active_order(buy_id)
        if sell == "Not found" and buy != "Not found":
            if buy != "Not found":  
                t = strftime("%Y-%m-%d %H:%M UTC", gmtime())
                try:
                    stg = t + " Sold " + str(ass_quant * mf) + " " + symbol + " for " + log_sell_price
                except Exception:
                    stg = t + " Sold " + str(ass_quant * mf) + " " + symbol
                while "  " in stg:
                    stg = stg.replace("  ", " ")
                write_ap_file("log.txt", stg, "a")
                cancel_all(symbolf)
                depth = 2
                layer = 1
                price = float(get_price(symbolf, depth, layer)[0])
                base_quant = round(ass_quant * price, 2)
                base_delta = wdr_prc * base_quant
                try:
                    ass_balance = float(get_balance(symbol)[0])    
                except Exception:
                    ass_balance = 0.0
                try:    
                    base_balance = float(get_balance(base)[0]) - base_delta
                except Exception:
                    base_balance = 0.0
                if ass_balance < ass_quant:
                    init_buy()
                if base_balance < ass_quant * price:
                    init_sell()
                mf = 1.0
                ass_doll_balance = ass_balance * price
                if middle_multiplier == "ON":
                    if abs(base_balance - ass_doll_balance) < middle_band * (base_balance + ass_doll_balance):
                        mf = middle_factor
                    else:
                        mf = 1.0
                if ass_balance > ass_quant:
                    print(" Replace sell order...")
                    if sell_count == 0:
                        fc = open('settings.cfg', 'r')
                        params = fc.read()
                        fc.close()
                        key_params = params.split("\"")[1::2]
                        grid = float(key_params[9].split('/')[0])
                    else:
                        f = open("tmp/grid.txt", "r")
                        grid = float(f.read())
                        f.close() 
                    sell_price = price + (price / 100) * grid
                    deal_volume = ass_quant * mf
                    get_real_price(symbolf, deal_volume)
                    sell = place_order("sell", ass_quant * mf, sell_price)
                    print(" Sell order replaced")
                    wd_write(str(int(time.time())))
                else:
                    init_trade()
                buy_price = price - (price / 100) * tp_prc    
                if base_balance > ass_quant * buy_price + base_delta:    
                    print(" Replace buy order...")
                    deal_volume = ass_quant * mf
                    get_real_price(symbolf, deal_volume)
                    buy = place_order("buy", ass_quant * mf, buy_price)
                    print(" Buy order replaced")
                    wd_write(str(int(time.time())))
                else:
                    init_trade()
                sell_count = sell_count + 1
                buy_count = 0
                if grid_mode == "ARITHMETIC":
                    grid = grid + grid_bias
                if grid_mode == "GEOMETRIC":
                    grid = grid * grid_bias
                if grid_mode == "EXPONENTIAL":
                    grid = grid ** grid_bias
                if grid_mode == "CUSTOM":
                    fc = open('settings.cfg', 'r')
                    params = fc.read()
                    fc.close()
                    key_params = params.split("\"")[1::2]
                    grid = key_params[9].split('/')
                    if sell_count in range (len(grid)):
                        grid = float(grid[int(sell_count)])
                    else:
                        grid = float(grid[-1]) 
                write_to_file("tmp/grid.txt", str(grid), "w")
                write_to_file("tmp/sell_id.txt", str(sell), "w")
                write_to_file("tmp/buy_id.txt", str(buy), "w")
                write_to_file("tmp/sell_count.txt", str(sell_count), "w")
                write_to_file("tmp/buy_count.txt", str(buy_count), "w")
                write_to_file("tmp/mult_f.txt", str(mf), "w")
                if withdraw == "ON" or withdraw == "IF_SELL_ONLY":
                    transfer_amount = round(0.95 * base_delta * mf, 2)
                    transfer(transfer_amount)
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                ping = int(key_params[13])
                ping = random.randint(int(0.8 * ping),int(1.2 * ping))
                     
        if buy == "Not found" and sell != "Not found":
            if sell != "Not found":
                t = strftime("%Y-%m-%d %H:%M UTC", gmtime())
                try:
                    stg = t + " Bought " + str(ass_quant * mf)+ " " + symbol + " for " + log_buy_price
                except Exception:
                    stg = t + " Bought " + str(ass_quant * mf)+ " " + symbol
                while "  " in stg:
                    stg = stg.replace("  ", " ")
                write_ap_file("log.txt", stg, "a")
                cancel_all(symbolf)
                depth = 2
                layer = 1
                price = float(get_price(symbolf, depth, layer)[0])
                base_quant = round(ass_quant * price, 2)
                base_delta = wdr_prc * base_quant
                try:
                    ass_balance = float(get_balance(symbol)[0])
                except Exception:
                    ass_balance = 0.0
                try:    
                    base_balance = float(get_balance(base)[0]) - base_delta
                except Exception:
                    base_balance = 0.0
                if ass_balance < ass_quant:
                    init_buy()
                if base_balance < ass_quant * price:
                    init_sell()
                mf = 1.0
                ass_doll_balance = ass_balance * price
                if middle_multiplier == "ON":
                    if abs(base_balance - ass_doll_balance) < middle_band * (base_balance + ass_doll_balance):
                        mf = middle_factor
                    else:
                        mf = 1.0
                if buy_count == 0:
                    fc = open('settings.cfg', 'r')
                    params = fc.read()
                    fc.close()
                    key_params = params.split("\"")[1::2]
                    grid = float(key_params[9].split('/')[0])
                else:
                    f = open("tmp/grid.txt", "r")
                    grid = float(f.read())
                    f.close()
                buy_price = price - (price / 100) * grid
                if base_balance > ass_quant * buy_price + base_delta:
                    print(" Replace buy order...")
                    deal_volume = ass_quant * mf
                    get_real_price(symbolf, deal_volume)
                    buy = place_order("buy", ass_quant * mf, buy_price)
                    print(" Buy order replaced")
                    wd_write(str(int(time.time())))
                else:
                    init_trade()
                if ass_balance > ass_quant:
                    print(" Replace sell order...")
                    sell_price = price + (price / 100) * tp_prc
                    deal_volume = ass_quant * mf
                    get_real_price(symbolf, deal_volume)
                    sell = place_order("sell", ass_quant * mf, sell_price)
                    print(" Sell order replaced")
                    wd_write(str(int(time.time())))
                else:
                    init_trade()
                buy_count = buy_count + 1
                sell_count = 0
                if grid_mode == "ARITHMETIC":
                    grid = grid + grid_bias
                if grid_mode == "GEOMETRIC":
                    grid = grid * grid_bias
                if grid_mode == "EXPONENTIAL":
                    grid = grid ** grid_bias
                if grid_mode == "CUSTOM":
                    fc = open('settings.cfg', 'r')
                    params = fc.read()
                    fc.close()
                    key_params = params.split("\"")[1::2]
                    grid = key_params[9].split('/')
                    if buy_count in range (len(grid)):
                        grid = float(grid[int(buy_count)])
                    else:
                        grid = float(grid[-1]) 
                write_to_file("tmp/grid.txt", str(grid), "w")
                write_to_file("tmp/sell_id.txt", str(sell), "w")
                write_to_file("tmp/buy_id.txt", str(buy), "w")
                write_to_file("tmp/sell_count.txt", str(sell_count), "w")
                write_to_file("tmp/buy_count.txt", str(buy_count), "w")
                write_to_file("tmp/mult_f.txt", str(mf), "w")
                if withdraw == "ON" or withdraw == "IF_BUY_ONLY" :
                    transfer_amount = round(0.95 * base_delta * mf, 2)
                    transfer(transfer_amount)
                fc = open('settings.cfg', 'r')
                params = fc.read()
                fc.close()
                key_params = params.split("\"")[1::2]
                ping = int(key_params[13])
                ping = random.randint(int(0.8 * ping),int(1.2 * ping))
                     
        if sell == "Not found" and buy == "Not found":
            init_trade()
    except Exception:
        time.sleep(10)
        print(R + " Error")
        err_counter += 1
        if err_counter > 10:
            os.system("shutdown /r /t 10 /f")
            sys.exit()

t = strftime("%Y-%m-%d %H:%M UTC", gmtime())
isempty = os.stat('log.txt').st_size == 0
if isempty == True:
    write_ap_file("log.txt", t + " The round has started ", "w")
isempty = os.stat('tmp/strt_b.txt').st_size == 0
if isempty == True:
    try:
        cancel_all(symbolf)
        funds()       
        depth = 1
        layer = 0 
        c_price = get_price(symbolf, depth, layer)
        curr_price = (float(c_price[0]) + float(c_price[1])) / 2
        total_balance = ((ass_balance + res_balance) * curr_price) + base_balance + base_res_balance
        write_ap_file("tmp/strt_b.txt", str(curr_price), "w")
        r_lot = (total_balance / grids_num) / curr_price
        ass_quant = round_all(r_lot)
        write_ap_file("tmp/strt_b.txt", str(ass_quant), "a") 
        write_to_file("tmp/strt_b.txt", str(total_balance + wallet), "a")
    except Exception:
        print(R + " API access or network connection problem")  
sound()
time.sleep(3)
os.system("cls")
print("")
print("")
print("")
print("")
print("")
print("")
print(G + "         SHIFTGRID 2.6.1 WELCOMES YOU!")
print(W + "")
wd_buffer = ""
wd_write(str(int(time.time())))
t1 = Thread(target = wd) 
if exchange == "Gate.io":
    symbolf = symbol + "_" + base
else:
    symbolf = symbol + base
try:
    conn = ntplib.NTPClient()
    response = conn.request('0.europe.pool.ntp.org', version=3)
    tm = datetime.datetime.fromtimestamp(response.tx_time, datetime.timezone.utc)
    tmm = int(tm.strftime('%M'))
    tms = int(tm.strftime('%S'))
    tm = datetime.datetime.now()
    tmsm = int(tm.strftime('%M'))
    tmss = int(tm.strftime('%S'))
    if tmm != tmsm or abs(tmss - tms) > 1:
        print(Y + " WARNING: Check your computer's clock ")
        print(Y + " synchronization with the Internet!")
        time.sleep(3)
except Exception:
    pass
while net_con == 0:
    try:
        funds()
        depth = 3
        layer = 2
        price = float(get_price(symbolf, depth, layer)[0])
        base_quant = int(base_balance)
        deal_volume = get_volume()
        get_real_price(symbolf, deal_volume)
        os.system("cls")
        print("")
        print("")
        print("")
        print(G + " Successfully connected to the exchange")
        print(G + " Please wait...")
        net_con = 1
    except Exception:
        print(Y + " Check your internet connection!")
        time.sleep(3)
time.sleep(3)
fmt = "{:10." + str(priceRound) + "f}"        
if wd_switch == "ON":
    t1.start()
if wd_switch != "ON":
    print(Y + " Built-in watchdog disabled!")
    time.sleep(2)
tr = Thread(target = prt_scr)    
if __name__ == "__main__":
    tr.start()

        















