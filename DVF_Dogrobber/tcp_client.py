import socket
import time

from global_configuration import generate_commands_to_be_sent


def verify_response(response_str_list):
    return (
        response_str_list[0] == "5A" and
        (response_str_list[1] == "AA" or response_str_list[1] == "55") and
        response_str_list[5] == "01"
    )

def send_data_to_server():
    # 服务器地址和端口
    SERVER_ADDRESS = '192.168.3.11'
    SERVER_PORT = 6666
    # 创建TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 连接到服务器
        s.connect((SERVER_ADDRESS, SERVER_PORT))

        # 要发送的数据列表
        commands_to_be_sent_dict = generate_commands_to_be_sent()  # 假设的数据

        # 发送数据并验证响应
        for value in commands_to_be_sent_dict.values():
            # 发送数据
            #print(value)
            s.sendall(bytes(value))

            #time.sleep(0.2)
            # 接收响应，这里假设服务器会立即回复，并且回复数据不大
            s.settimeout(1)  # 设置第一个回复的超时时间为1秒

            try:
                ack_response = s.recv(8)  # 尝试在1秒内读取最多8字节的数据
                if ack_response:
                    ack_response_str_list = [hex(byte)[2:].upper().zfill(2) for byte in ack_response]
                    if verify_response(ack_response_str_list):
                        print(ack_response_str_list)
                    else:
                        s.close()
                        return False

                else:
                    print("ack_response回复为空")
            except socket.timeout:
                print("ack_response回复超时")
                s.close()
                return False

                # 在尝试第二个回复之前，重新设置超时时间为3秒

            s.settimeout(3)
            try:
                notify_response = s.recv(8)  # 尝试在3秒内读取最多8字节的数据
                if notify_response:
                    notify_response_str_list = [hex(byte)[2:].upper().zfill(2) for byte in notify_response]
                    if verify_response(notify_response_str_list):
                        print(notify_response_str_list)
                    else:
                        s.close()
                        return False
                else:
                    print("notify_response回复为空")
            except socket.timeout:
                print("notify_response回复超时")
                s.close()
                return False

                # 如果你不再需要超时，可以将它设置为None
            s.settimeout(None)

        # 关闭连接
        s.close()
        # 正常流程结束，with语句会自动关闭s
        return True

#print(send_data_to_server())