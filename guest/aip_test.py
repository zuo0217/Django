#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Create time : 2018/4/16上午12:19
# Create by Saseny.Zhou
# File name: aip_test.py

import requests

"""添加发布会api测试"""
data = {
    "eid": 4,
    "name": "apple",
    "limit": 2000,
    "status": 1,
    "address": "shanghai",
    "start_time": "2018-04-16 10:00:00"
}
response = requests.post(url='http://127.0.0.1:8000/api/add_event/', data=data)
print(response.status_code)
print(response.json())

"""搜索发布会api测试"""
response = requests.get(url='http://127.0.0.1:8000/api/get_event_list/', data={'eid': 1})
print(response.status_code)
print(response.json())

"""添加嘉宾api测试"""
data = {
    "eid": 4,
    "realname": "seven",
    "phone": "15800982412",
    "email": "seven@mail.com"
}

response = requests.post(url='http://127.0.0.1:8000/api/add_guest/', data=data)
print(response.status_code)
print(response.json())

"""搜索嘉宾api测试"""
response = requests.get(url='http://127.0.0.1:8000/api/get_guest_list/', data={'eid': 1})
print(response.status_code)
print(response.json())

"""签名api测试"""
response = requests.post(url='http://127.0.0.1:8000/api/user_sign/', data={'eid': 4, "phone": "15800982412"})
print(response.status_code)
print(response.json())
