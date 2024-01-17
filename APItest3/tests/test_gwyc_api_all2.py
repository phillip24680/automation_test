import  pytest
import json

from base import method
from utils import operationExcel

import allure

import time

import requests

@pytest.mark.usefixtures("token")
@pytest.mark.parametrize("data,title",zip(operationExcel.OperationExcel().getExceldatas()
    ,operationExcel.OperationExcel().Case_name()))#装饰器进行封装用例
#参数化运行所有用例
def test_api(data,token,title):
    # 设置测试用例的标题
    allure.dynamic.title(title)

    # 对请求头作为空处理并添加token
    headers=data[operationExcel.ExcelVarles.case_headers]
    if len(str(headers).split())== 0:
        pass
    elif len(str(headers))>= 0:
        headers=json.loads(headers)#转换为字典
        headers['Authorization']=token#获取登录返回的token并添加到读取出来的headers里面
        headers=headers

    #对请求参数做为空处理
    params=data[operationExcel.ExcelVarles.case_data]
    if len(str(params).split())== 0:
        pass
    elif len(str(params))>= 0:
        params=params

    #断言封装
    case_code=str(data[operationExcel.ExcelVarles.case_code])
    def case_result_assert(r):
        assert  str(r.status_code) == case_code#状态码
        assert data[operationExcel.ExcelVarles.case_result] in json.dumps(r.json(),ensure_ascii=False)#响应数据

    #执行用例
    if data[operationExcel.ExcelVarles.case_method]=='get':
        start_time = time.time()
        r=method.ApiRequest().send_requests(
            method='get',
            url=data[operationExcel.ExcelVarles.case_url],
            data=params,
            headers=headers
        )
        end_time = time.time()
        response_time = end_time - start_time
        #with allure.step('记录接口响应时间'):
        allure.attach(f'接口响应时间：{response_time:.2f}秒','接口响应时间')
        # allure.attach(r.text, '接口返回内容')
        allure.attach(json.dumps(r.json(), ensure_ascii=False, indent=4), "接口响应内容", allure.attachment_type.JSON)



        print (r.json())
        print(response_time)
        #h = float(data[operationExcel.ExcelVarles.case_response_time)
        assert round(response_time,2) < float(data[operationExcel.ExcelVarles.case_response_time])
        case_result_assert(r=r)
    elif data[operationExcel.ExcelVarles.case_method]=='post':
        r = method.ApiRequest().send_requests(
            method='post',
            url=data[operationExcel.ExcelVarles.case_url],
            json=json.loads(params),
            headers=headers)
        # writeContent(r.json()['data']['access_tonken'])#提取出返回数据中想要的变量写入到文件中供其他接口使用
        print (r.json())
        case_result_assert(r=r)


if __name__ == '__main__':
    """执行并生成allure测试报告"""
    pytest.main(["-s","-v","--alluredir","./report/result"]) #运行输出并在report/result目录下生成json文件
    import subprocess #通过标准库中的subprocess包来fork一个子进程，并进行一个外部的程序
    subprocess.call('allure generate report/result/ -o report/html --clean',shell=True)#读取json文件并生成html报告，
                         # --clean若目录存在则先清除
    subprocess.call('allure open -h 127.0.0.1 -p 9999 ./report/html',shell=True)#生成一个本地的服务并自动打开html报告