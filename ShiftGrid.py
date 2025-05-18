#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.



import os
import sys
import subprocess
import psutil
from winreg import *
os.system("color 0f")
os.system("mode con cols=46 lines=16")
print("")
print(" Robot starts. Please wait...")
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
from cryptography.fernet import Fernet
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
#import urlreq
time.sleep(2)
warnings.filterwarnings("ignore")
init()
ctypes.windll.kernel32.SetConsoleTitleA(b"ShiftGrid v2.6.3")
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
lk = bytes.fromhex(lc)
handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))
M = Fore.MAGENTA + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
G = Fore.GREEN + Style.BRIGHT
Y = Fore.YELLOW + Style.NORMAL
B = Fore.BLUE + Style.BRIGHT
R = Fore.RED + Style.NORMAL
W = Fore.WHITE + Style.NORMAL
RD = Fore.RED + Style.DIM

from src import __main__
def prt_scr():
    print('\033[?25l', end="")
    os.system("cls")
    print("")
    print(M + " *** ShiftGrid v2.6.3 trading robot works ***")
tr = Thread(target = prt_scr)
if __name__ == "__main__":
    tr.start()
