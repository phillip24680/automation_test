import time

import serial
import threading

# 初始化串口对象
ser = serial.Serial()
ser.port = 'COM3'  # 设置串口号，根据实际情况修改
ser.baudrate = 115200  # 波特率
ser.bytesize = serial.EIGHTBITS  # 数据位
ser.stopbits = serial.STOPBITS_ONE  # 停止位
ser.parity = serial.PARITY_NONE  # 校验位

stop_event = threading.Event()  # 用于停止线程的事件





def send_enter():
    while not stop_event.is_set():
        ser.write(b'\r')  # 发送 Enter 键
        stop_event.wait(1)  # 每次发送后等待 1 秒

def receive_data():
    while not stop_event.is_set():
        global recv_data
        recv_data = b'0'
        recv_data = ser.readline()  # 读取一行数据
        stop_event.wait(1)

        if recv_data:
            print('接收到数据:', recv_data.strip())


try:
    # 打开串口
    ser.open()
    if ser.isOpen():
        print('串口已打开')

        # 创建并启动发送线程
        send_thread = threading.Thread(target=send_enter)
        send_thread.start()

        # 创建并启动接收线程
        receive_thread = threading.Thread(target=receive_data)
        receive_thread.start()

        while(1):
            state = recv_data.strip()
            if (state == b'u-boot=>'):
                stop_event.set()  # 设置停止事件
                ser.write(b'mmc dev 1')
                time.sleep(1)
                ser.write(b'fatload mmc 1 0x48000000 industrial_firmware_2_1.bin')
                time.sleep(1)
                ser.write(b'cp.b 0x48000000 0x7e0000 0x20000')
                time.sleep(1)
                ser.write(b'bootaux 0x7e0000')
                break

            elif input('按下回车键停止发送和接收线程...'):
                stop_event.set()  # 设置停止事件
                break

        # 等待发送和接收线程完成
        send_thread.join()
        receive_thread.join()

except serial.SerialException as e:
    print('串口打开失败:', str(e))

finally:
    # 关闭串口
    if ser.isOpen():
        ser.close()
        print('串口已关闭')