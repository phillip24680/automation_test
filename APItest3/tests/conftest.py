import pytest
import requests
import json
@pytest.fixture(scope='session')
#@pytest.fixture装饰器整个模块运行前运行一次里面的方法
def token():
    """"获取token并返回"""
    url="https://login.microsoftonline.com/db8e2ba9-95c1-4fbb-b558-6bf8bb1d2981/oauth2/v2.0/token"
    # headers={}  #请求头信息
    data = {
        "grant_type": "client_credentials",
        "client_secret": "lVw8Q~otts8AAtJJmXI9kg1eK4_maOni6T2MBazG",
        "client_id": "047bb604-3a3d-4b2d-92ce-1c4da90426bf",
        "scope": "api://ab297213-23cd-43e6-aa6b-a5fa1b12dac1/.default"
    } #请求参数
    r=requests.post(url=url,data=data)
    #返回所有token信息
    token=str('Bearer'+' '+r.json()['access_token'])
    print(token)
    return token




