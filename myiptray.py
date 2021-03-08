#!/usr/bin/env python3

from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageFont
import requests
import socket
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import sys
import os
import signal

ICON = 0
MENU = menu(
    item('ip_address', action=None),
    item('hostname', action=None),
    item('Exit', action=sys.exit)
)


def get_ip_hostname():
    try:
        re_pub_ip = requests.get('https://ifconfig.io/ip')
        ip = re_pub_ip.text.strip('\n')
        hostname = socket.gethostbyaddr(ip)[0]
    except:
        ip = 'without network'
        hostname = 'without network'
    return ip, hostname


def create_image(text='IP', width=48, height=48, color1=(0,0,0), color2=(255,255,255)):
    img = Image.new('RGB', (width, height), color1)
    im_a = img.convert('L').resize(img.size)
    im_rgba = img.copy()
    im_rgba.putalpha(im_a)
    d = ImageDraw.Draw(im_rgba)
    fnt = ImageFont.truetype(font='/usr/share/fonts/liberation-mono/LiberationMono-Bold.ttf', size=40)
    d.text((1, 1), text, font=fnt, fill=color2)
    return im_rgba


def create_icon(ip_address):
    global MENU
    return icon(ip_address, create_image(), menu=MENU)


def terminate():
    os.kill(os.getpid(), 15)


def update_icon(u_icon):
    global MENU
    while u_icon.visible:
        ip_address, hostname = get_ip_hostname()
        print(ip_address, hostname)
        MENU = menu(
            item(ip_address, action=None),
            item(hostname, action=None),
            item('Exit', action=terminate)
        )
        u_icon.menu = MENU
        u_icon.update_menu()
        sleep(10)


def main():
    ip_address, hostname = get_ip_hostname()
    print(ip_address, hostname)
    n_icon = create_icon(ip_address)
    n_icon.visible = True
    n_icon.run(setup=update_icon)


if __name__ == '__main__':
    main()
