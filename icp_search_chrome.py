#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/3
# @Author  : starnight_cyber
# @Github  : https://github.com/starnightcyber
# @Software: PyCharm
# @File    : icp_search_chrome.py

import csv
import random
import time

import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 设置Chrome的基本属性
options = webdriver.ChromeOptions()
# options.add_argument("headless")
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("detach", True)

# 设置Chrome驱动路径，加载设置后浏览器开始模拟访问
path = "./chromedriver"
s = Service(path)
driver = webdriver.Chrome(service=s, options=options)
driver.set_page_load_timeout(30)
org_domains = []


def icp_search(target):
    """
    Fetch target ICP beian using icp.chinaz.com
    :param target: Target org name
    :return: domain
    """
    try:
        # 获取首页
        url = 'https://icp.chinaz.com/{}'.format(target)
        driver.get(url=url)
        # 显式等待确保元素加载
        wait = WebDriverWait(driver, 10)
        permit_text = 'N/A'
        home_page_text = 'N/A'
        institution_nature_text = 'N/A'
        if 'home_page' in driver.page_source:
            # 获取 ICP 备案编号
            permit_element = wait.until(EC.presence_of_element_located((By.ID, "permit")))
            permit_text = permit_element.text
            # 获取备案域名
            home_page_element = wait.until(EC.presence_of_element_located((By.ID, "home_page")))
            home_page_text = home_page_element.text
            # 获取单位性质
            institution_nature_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//td[text()='主办单位性质']/following-sibling::td")))
            institution_nature_text = institution_nature_element.text
        else:
            # no beian info
            pass
        # 正常休眠时间 1-3s
        sleep_time = random.uniform(3, 10)
    except Exception as e:
        # 异常休眠 30-60s，站点一般会有防爬措施
        sleep_time = random.uniform(10, 30)
        print('[-] err => {}'.format(str(e)))
    finally:
        # 休眠指定的时间
        time.sleep(sleep_time)
        print('[*] sleep_time => {}'.format(sleep_time))
        return permit_text, home_page_text, institution_nature_text


def load_orgs():
    with open("./org-vuls.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        cnt = 0
        begin = 1
        end = 10000
        for line in reader:
            try:
                cnt += 1
                if cnt < begin:
                    continue
                if cnt == end:
                    break
                org_name = line[1]
                print('[*][{}] checking {}'.format(cnt, org_name))
                permit_text, home_page_text, institution_nature_text = icp_search(org_name)
                if cnt == 1:
                    time.sleep(15)
                line.append(permit_text)
                line.append(home_page_text)
                line.append(institution_nature_text)
                print(line)
                org_domains.append(line)
            except:
                pass


def save_results():
    with open("./org-domains_all.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['index', 'company_id', 'company_name', 'total', 'handled', 'valuable',
                         'ICP', 'domain', 'institution'])
        for line in org_domains:
            writer.writerow(line)


if __name__ == '__main__':
    load_orgs()
    save_results()
    pass
