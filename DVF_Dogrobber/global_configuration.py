from openpyxl import load_workbook
from wifi_check import get_wifi_enable_test_suite,wifi_scan_request_command
#V1.0

# 加载Excel文件
workbook = load_workbook(filename='Lite DVF Configuration File_v0.2.xlsx')

# 选择工作表
global_sheet = workbook['Global Configuration']

def get_enable_test_suite(column_num):
    test_suite_list = []  # 存储执行fast configure的test suite
    # 初始化行号
    row_num = 4  # 从E4开始，行号为4
    # 循环读取，直到遇到空值
    while True:
        # 获取单元格值
        cell_value = global_sheet.cell(row=row_num, column=column_num).value  # 列号5对应E列
        if cell_value is None:  # 如果单元格为空，则停止循环
            break
        elif cell_value == 'Y':
            test_suite_name = global_sheet.cell(row=row_num, column=1).value
            test_suite_list.append(test_suite_name)
            test_suite_command = global_sheet.cell(row=row_num, column=2).value
            test_suite_list.append(test_suite_command)
        # 行号递增，移动到下一行
        row_num += 1
    return test_suite_list

def calculate_crc_add_magicNumber(hex_data_list):
    # 将十六进制字符串转换为整数，并求和
    sum_value = sum(hex_data_list)
    #sum_value = hex(sum_value)
    # 按位取反操作
    crc_result_0 = sum_value ^ 0xFF
    # 取后8位
    crc_result = crc_result_0 & 0xFF
    hex_data_list.append(crc_result)
    hex_data_list.insert(0, int('90'))

    return hex_data_list

fast_config_scope = get_enable_test_suite(5)
if fast_config_scope and any("Wi-Fi Check" in item for item in fast_config_scope):
    wifi_check_command = fast_config_scope[fast_config_scope.index("Wi-Fi Check") + 1]
    wifi_scan_request_command_list = wifi_scan_request_command()
    wifi_scan_request_command_list.insert(0, int(wifi_check_command))
    calculate_crc_add_magicNumber(wifi_scan_request_command_list)
    print(wifi_scan_request_command_list)
    #print(bytes(wifi_scan_request_command_list))  # 要发送配置wifi scan的指令

else:
    test_scope = get_enable_test_suite(4)
    #发送测试范围指令
    if len(test_scope) == 0:
        scope_command_list = ['06', '01', '00', '01']
        scope_command_list = [int(x, 16) for x in scope_command_list]
        calculate_crc_add_magicNumber(scope_command_list)
        print(scope_command_list)
    else:
        scope_command_list = ['06', '03', '00', '01', '03', '00']
        scope_command_list = [int(x, 16) for x in scope_command_list]
        calculate_crc_add_magicNumber(scope_command_list)
        print(scope_command_list)

    #发送配置指令
    if test_scope and any("Wi-Fi Check" in item for item in test_scope):
        wifi_check_command = test_scope[test_scope.index("Wi-Fi Check") + 1]
        wifi_scan_request_command_list = wifi_scan_request_command()
        wifi_scan_request_command_list.insert(0, int(wifi_check_command))
        calculate_crc_add_magicNumber(wifi_scan_request_command_list)
        print(wifi_scan_request_command_list)
        #print(bytes(wifi_scan_request_command_list))   #要发送配置wifi scan的指令



