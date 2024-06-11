#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/3
# @Author  : starnight_cyber
# @Github  : https://github.com/starnightcyber
# @Software: PyCharm
# @File    : fetch_org_vuls.py

import csv
import random
import ssl
import time

import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Do not support ssl and disable warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
timestamp = time.strftime("%Y-%m-%d", time.localtime(time.time()))

org_vuls = []


def load_orgs():
    with open("./orgs-names.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        cnt = 0
        for line in reader:
            try:
                cnt += 1
                org_url = line[2]
                resp = requests.get(org_url, timeout=10)
                # print(resp.text)
                # 解析 HTML
                total, handled = extract_data(resp.text)
                line.append(int(total))
                line.append(int(handled))
                valuable = 1 if int(handled) >= 10 else 0
                line.append(valuable)
                print(line)
                org_vuls.append(line)
                # if cnt == 10:
                #     break
            except Exception as e:
                print('[-] err => {}'.format(str(e)))
            finally:
                # 生成随机的休眠时间
                sleep_time = random.uniform(0, 5)
                print('sleep_time => {}'.format(sleep_time))
                # 休眠指定的时间
                time.sleep(sleep_time)


def extract_data(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # 查找所有的 dd 元素
        dd_tags = soup.find_all('dd', class_='privateSrcLoop')

        # 存储提取出来的数据的列表
        numbers = []
        # 遍历所有的 dd 标签并提取 p 标签内容
        for dd in dd_tags:
            p_tag = dd.find('p', class_='spp')
            if p_tag:
                numbers.append(p_tag.text)
        return numbers
    except:
        return [0, 0]


def save_results():
    with open("./org-vuls.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['index', 'company_id', 'company_name', 'total', 'handled', 'valuable'])
        for line in org_vuls:
            writer.writerow(line)


if __name__ == '__main__':
    load_orgs()
    save_results()
    pass
