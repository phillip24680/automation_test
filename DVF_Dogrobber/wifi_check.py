from openpyxl import load_workbook
import struct

# 加载Excel文件
workbook = load_workbook(filename='Lite DVF Configuration File_v0.2.xlsx')

# 选择工作表
wifi_check_sheet = workbook['Wi-Fi Check']

def get_wifi_enable_test_suite():
    wifi_test_suite_list = []  # 存储执行fast configure的test suite
    cell_value = wifi_check_sheet.cell(row=4, column=3).value
    if cell_value == 'Y':
        test_suite_subCommand = wifi_check_sheet.cell(row=4, column=2).value
        wifi_test_suite_list.append(test_suite_subCommand)
    return wifi_test_suite_list

sub_suite_fast = []  #存储执行fast configure的test suite
# 初始化行号
row_num = 4  # 从E4开始，行号为4
# 循环读取，直到遇到空值
while True:
    # 获取单元格值
    cell_value = wifi_check_sheet.cell(row=row_num, column=4).value  # 列号5对应E列
    if cell_value is None:  # 如果单元格为空，则停止循环
        break
    elif cell_value == 'Y':
        test_suite = wifi_check_sheet.cell(row=row_num, column=1).value
        sub_suite_fast.append(test_suite)
        #print(sub_suite_fast[row_num - 4])
    else:
        pass#print(workbook.cell(row=row_num, column=4).value)
    # 行号递增，移动到下一行
    row_num += 1

#把字符串转换为16进制格式输出，且每个字节间空一格
def string_to_hex_spaced(s):
    return ' '.join(['{:02x}'.format(ord(c)) for c in s])

def int_to_hex_le(value, byte_length):
    """
    Convert an integer to a hexadecimal string in little-endian format with specified byte length.
    """
    # Pack the integer into bytes using little-endian format
    packed_value = struct.pack(f'<{byte_length}s', struct.pack('<i', value)[:byte_length])

    # Convert to hex and format: remove '0x' prefix and add space between each byte
    hex_str = ' '.join(f'{b:02x}' for b in packed_value)

    return hex_str

def set_bits_from_reversed_string(bit_positions_str):
    # 将逗号分隔的字符串转换为整数列表，并确保在有效范围内
    values = [16 - int(position.strip()) for position in bit_positions_str.split(',') if
              1 <= int(position.strip()) <= 14]
    # 确保位置是唯一的并排序
    values = sorted(set(values))

    # 初始化一个16位全为0的二进制数
    bit_string = '0' * 16

    # 遍历有效值（现在是从高位到低位，但因为我们逆序处理了values，实际上设置的是低位到高位）
    for value in values:
        bit_string = bit_string[:value] + '1' + bit_string[value + 1:]

    # 转换为整数
    hex_value_int = int(bit_string, 2)

    # 确保转换结果适应2字节（16位），对于小于16位的情况，在前面补充0
    hex_value_padded = f"{hex_value_int:04x}"  # 确保至少两位，最多四位（两位对于一个字节，这里是两个字节）

    # 转换为小端模式的16进制字符串，每个字节间加空格
    try:
        hex_value_le = ' '.join(f'{b:02x}' for b in bytes.fromhex(hex_value_padded)[::-1])
    except ValueError as e:
        print(f"Error converting to hex: {e}")
        hex_value_le = "Error"

    return hex_value_le

def wifi_scan_request_command():
    Wifi_scan_subcommand = wifi_check_sheet.cell(row=4, column=2).value
    Timeout = wifi_check_sheet.cell(row=4, column=7).value
    Element_number = wifi_check_sheet.cell(row=5, column=7).value
    SSID_length = len(wifi_check_sheet.cell(row=7, column=7).value)
    SSID_string = wifi_check_sheet.cell(row=7, column=7).value
    Channel_list = wifi_check_sheet.cell(row=8, column=7).value

    wifi_scan_payload = Wifi_scan_subcommand + " " + int_to_hex_le(Timeout, 2) + " " + int_to_hex_le(Element_number, 1) + " " \
                        + int_to_hex_le(SSID_length, 1) + " " + string_to_hex_spaced(SSID_string) + " " + set_bits_from_reversed_string(Channel_list)

    payload_length = int(len(wifi_scan_payload.replace(' ', ''))/2)
    payload_length_hex = ' '.join(f'{b:02x}' for b in payload_length.to_bytes(2, byteorder='little'))
    wifi_scan_request_command = payload_length_hex + " " + wifi_scan_payload   #payload length + payload

    #wifi_scan_request_command_list = [int(s, 16) for s in wifi_scan_request_command.split()]
    wifi_scan_request_command_list = wifi_scan_request_command.split()  #16进制数列表（字符串形式）

    wifi_scan_request_command_list = [int(x, 16) for x in wifi_scan_request_command_list]   #字符串形式转换为整数列表
    return wifi_scan_request_command_list


