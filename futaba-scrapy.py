# -*- coding:utf-8 -*-
import os
import re
import requests
from pyquery import PyQuery as q

url = 'http://dec.2chan.net/b/futaba.htm'

def page_get(root_url):
    resp = requests.get(root_url)
    html = resp.text
    query = q(html)

    url_list = []
    for res_page in query.find('.hsbn'):
        href = q(res_page).attr('href')
        url = root_url.replace('futaba.htm', '')
        url_list.append(os.path.join(url, href))

    return url_list


def parse(target_url_list):
    for url in target_url_list:
        resp = requests.get(url)
        html = resp.text
        query = q(html)
        dig_image(query)

def dig_image(query):
    p = re.compile('.*\/src\/.*\.jpg$')
    for link_list in query.find('a'):
        href = q(link_list).attr('href')
        if p.match(href):
            save_image(href)

def save_image(url):
    filename = os.path.basename(url)
    r = requests.get(url)
    if r.status_code == 200:
        with open('./img/%s' % filename, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)


url_list = page_get(url)
print url_list
parse(url_list)


