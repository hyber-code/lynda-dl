import os
from colorama import Fore, init, Back, Style
import itertools
from req.sessions import *
import re
import time
import bs4
import sys
from urllib.request import urlopen
import subprocess
from googletrans import Translator

currentDir = os.getcwd()
session = Session()
ffmpeg_dir = os.path.join(currentDir,'ffmpeg.exe')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
    'X-Requested-With': 'XMLHttpRequest'
}
url_logout = 'https://www.lynda.com/signout'
ajax_subtitle = 'https://www.lynda.com/ajax/player/transcript?'
ajax_lession = 'https://www.lynda.com/ajax/course/'
url_login = 'https://www.lynda.com/portal/sip?org='
user_agent = 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
if os.name == "posix":
    ## ----------------------------------------------------------------------------------------------------------------------  ##
    init(autoreset=True)
    # colors foreground text:
    fc = "\033[0;96m"
    fg = "\033[0;92m"
    fw = "\033[0;97m"
    fr = "\033[0;91m"
    fb = "\033[0;94m"
    fy = "\033[0;33m"
    fm = "\033[0;35m"

    # colors background text:
    bc = "\033[46m"
    bg = "\033[42m"
    bw = "\033[47m"
    br = "\033[41m"
    bb = "\033[44m"
    by = "\033[43m"
    bm = "\033[45m"

    # colors style text:
    sd = Style.DIM
    sn = Style.NORMAL
    sb = Style.BRIGHT
else:
    ## ----------------------------------------------------------------------------------------------------------------------  ##
    init(autoreset=True)
    # colors foreground text:
    fc = Fore.CYAN
    fg = Fore.GREEN
    fw = Fore.WHITE
    fr = Fore.RED
    fb = Fore.BLUE
    fy = Fore.YELLOW
    fm = Fore.MAGENTA

    # colors background text:
    bc = Back.CYAN
    bg = Back.GREEN
    bw = Back.WHITE
    br = Back.RED
    bb = Back.BLUE
    by = Fore.YELLOW
    bm = Fore.MAGENTA

    # colors style text:
    sd = Style.DIM
    sn = Style.NORMAL
    sb = Style.BRIGHT
    ## ----------------------------------------------------------------------------------------------------------------------  ##


def Banner():
    banner = '''
                    %s%s        0000                                    
                    %s%s        ⁰000                           00
                    %s%s         000                           00
                    %s%s         000   00    00  00⁰   00   00⁰00     00
                    %s%s         000    00  00    0 0  0   00  00    0  0
                    %s%s         000     ⁰00⁰     0  0 0   00  00   00⁰⁰00
                    %s%s        00000    00      00   ⁰00   00⁰00  00    00
                    %s%s                00
                    %s%s                                        Dev by Ha Tien Loi
    ''' % (fg, sd, fr, sd, fg, sd, fc, sd, fc, sd, fc, sd, fg, sd, fg, sd, fg, sd)

    return banner
