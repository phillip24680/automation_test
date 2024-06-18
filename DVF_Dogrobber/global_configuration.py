from openpyxl import load_workbook
from wifi_check import get_wifi_enable_test_suite,wifi_scan_request_command
#V1.0


def get_enable_test_suite(column_num, excel_file):
    # 加载Excel文件
    workbook = load_workbook(filename=excel_file)

    # 选择工作表
    global_sheet = workbook['Global Configuration']
    test_suite_dict = {}  # 存储执行fast configure的test suite
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
            test_suite_command = global_sheet.cell(row=row_num, column=2).value
            test_suite_dict[test_suite_name] = test_suite_command
        # 行号递增，移动到下一行
        row_num += 1
    return test_suite_dict

def calculate_crc_add_magicNumber(hex_data_list):
    # 将十六进制数求和
    sum_value = sum(hex_data_list)
    #sum_value = hex(sum_value)
    # 按位取反操作
    crc_result_0 = sum_value ^ 0xFF
    # 取后8位
    crc_result = crc_result_0 & 0xFF
    hex_data_list.append(crc_result)
    hex_data_list.insert(0, int('90'))

    return hex_data_list

def generate_commands_to_be_sent(excel_file):
    # 定义发送命令的字典
    command_dict = {}
    fast_config_scope = get_enable_test_suite(5, excel_file)   #获取fast config的范围
    if "Wi-Fi Check" in fast_config_scope:
        wifi_check_command = fast_config_scope["Wi-Fi Check"]
        wifi_scan_request_command_list = wifi_scan_request_command(excel_file)
        wifi_scan_request_command_list.insert(0, int(wifi_check_command))
        wifi_scan_request_command_list = [int(wifi_check_command)] + wifi_scan_request_command(excel_file)
        calculate_crc_add_magicNumber(wifi_scan_request_command_list)
        command_dict["Wi-Fi Check"] = wifi_scan_request_command_list

        #print(' '.join([hex(num)[2:].zfill(2).upper() for num in wifi_scan_request_command_list]))  # 打印字符串格式指令
        return command_dict
    else:
        test_scope = get_enable_test_suite(4, excel_file)  #获取Global Execution Option列的值
        # 生成测试范围与配置指令
        if len(test_scope) == 0:
            scope_command_list = ['06', '01', '00', '01']
            scope_command_list = [int(x, 16) for x in scope_command_list]
            calculate_crc_add_magicNumber(scope_command_list)
            #print(' '.join([hex(num)[2:].zfill(2).upper() for num in scope_command_list]))
            command_dict["test scope"] = scope_command_list
            return command_dict
        else:
            scope_command_list = ['06', '03', '00', '01', '03', '00']
            scope_command_list = [int(x, 16) for x in scope_command_list]
            calculate_crc_add_magicNumber(scope_command_list)
            #print(' '.join([hex(num)[2:].zfill(2).upper() for num in scope_command_list]))
            command_dict["test scope"] = scope_command_list

            wifi_check_command = test_scope["Wi-Fi Check"]
            wifi_scan_request_command_list = wifi_scan_request_command(excel_file)
            wifi_scan_request_command_list.insert(0, int(wifi_check_command))
            wifi_scan_request_command_list = [int(wifi_check_command)] + wifi_scan_request_command(excel_file)
            calculate_crc_add_magicNumber(wifi_scan_request_command_list)
            #print(' '.join([hex(num)[2:].zfill(2).upper() for num in wifi_scan_request_command_list]))
            command_dict["Wi-Fi Check"] = wifi_scan_request_command_list

            return command_dict

#print(generate_commands_to_be_sent())




