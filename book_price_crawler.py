#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import urllib.parse
import urllib.request as urlrequest
import os.path
import os
import time
from random import randint
import socket
import json
import ssl
import io

ssl._create_default_https_context = ssl._create_unverified_context

socket.setdefaulttimeout(2*60) # wait for maximum two miniutes for downloading the file
PROXY_FILE = './proxies.csv'

proxy_list = ['no',]
# with open(PROXY_FILE) as input_proxy_file:
#     proxy_list = ['no',]
#     for line in input_proxy_file:
#         proxy_ip, proxy_port = line.split('\t')
#         proxy_list.append("{}:{}".format(proxy_ip, proxy_port))

book_name_dict = {}

with io.open('books.csv',encoding='utf8',errors='ignore') as input_book_file:
    for line in input_book_file:
        try:
            words = line.strip().split('\t')
            book_id = words[0]
            book_name = words[1]
            book_name_dict[book_id] = book_name
        except:
            book_name_dict[book_id] = 'null'

book_ids = []

with open('book_list') as input_book_list:
    for line in input_book_list:
        words = line.strip().split()
        book_ids.append(words[0])

for book_id in book_ids:
    currentTime = datetime.now()
    time_str = currentTime.strftime("%Y-%m-%d-%H-%M-%S")
    print("crawl {}...".format(time_str))

    for proxy_url in proxy_list:
        try:
            print("try use proxy {} ...".format(proxy_url))
            if proxy_url != 'no':
                # create the object, assign it to a variable
                proxy = urlrequest.ProxyHandler({'https': proxy_url})
                # construct a new opener using your proxy settings
                opener = urlrequest.build_opener(proxy)
            else:
                opener = urlrequest.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30')]
            # install the openen on the module-level
            urlrequest.install_opener(opener)
            book_name = book_name_dict[book_id]
            #if book_name == 'null':
            #    continue
            print(book_id, book_name, "...")
            amazon_url = "https://www.amazon.com/s/url=search-alias%3Dstripbooks&field-keywords={}"
            book_name = book_name_dict[book_id]
            book_name_words = book_name.strip().split()
            book_name_search = '+'.join(book_name_words)
            urlrequest.urlretrieve(amazon_url.format(book_name_search),'./books/{}'.format(book_id))
            # print(response.read().decode('utf8'))
            time.sleep(3)

        except Exception as e:
            print(e)
            print("exception, try again...")