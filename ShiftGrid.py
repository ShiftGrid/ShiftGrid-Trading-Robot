import os
import sys
os.system("color 0f")
os.system("mode con cols=40 lines=10")
import warnings
warnings.filterwarnings("ignore")
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
init()
from colorama import Fore, Back, Style
import ctypes
from ctypes import *
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib/src')))
import urlconn
from src import __main__
def prt_scr():
    print('\033[?25l', end="")
    os.system("cls")
    print("")
    print(M + " ShiftGrid trading robot (ver.2.6.1) launched")
tr = Thread(target = prt_scr)
if __name__ == "__main__":
    tr.start()
