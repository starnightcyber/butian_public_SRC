#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/3
# @Author  : starnight_cyber
# @Github  : https://github.com/starnightcyber
# @Software: PyCharm
# @File    : fetch_orgs_chrome.py

import csv
import time

import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

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
orgs = []


def go_to_next_page():
    try:
        next_button = driver.find_element(By.CLASS_NAME, 'next')
        next_button.click()
        return True
    except:
        return False


def go_to_previous_page():
    try:
        prev_button = driver.find_element(By.CLASS_NAME, 'prev')
        prev_button.click()
        return True
    except:
        return False


def fetch_pages():
    # 获取首页
    url = 'https://www.butian.net/Reward/pub'
    driver.get(url=url)

    # 设置一个最大页数的限制，避免进入无限循环
    max_pages = 196
    current_page = 1
    index = 0
    while current_page <= max_pages:
        try:
            print(f'Parsing page {current_page}')
            # 找到所有的 "loophole-second" 类的 ul 元素
            uls = driver.find_elements(By.CLASS_NAME, "loophole-second")
            # 遍历每一个 ul 元素
            for ul in uls:
                index += 1
                # 获取 li 内部的 a 标签
                company_link = ul.find_element(By.TAG_NAME, 'a')
                company_name = company_link.text
                company_href = company_link.get_attribute('href')
                line = [index, company_name, company_href]
                orgs.append(line)
                print(line)
            if not go_to_next_page():
                break
            current_page += 1
            # 休眠一段时间以确保页面加载完毕
            time.sleep(3)
        except Exception as e:
            print('[-] err => {}'.format(str(e)))

    # 关闭浏览器
    driver.quit()


def save_results():
    with open("./orgs-names.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['index', 'company_id', 'company_name'])
        for line in orgs:
            writer.writerow(line)


if __name__ == '__main__':
    fetch_pages()
    save_results()
    pass
