import time
import serial

import sys

while (1):
    # 获取命令行参数
    args = input("Please enter COM and file name: ")  # 去除第一个参数（即脚本文件名）
    COM, Bin_Name = args.split()
    Bin_Command = 'fatload mmc 1 0x48000000' + ' ' + Bin_Name + '\r'

    # 初始化串口对象
    ser = serial.Serial()
    ser.port = COM  # 设置串口号，根据实际情况修改
    ser.baudrate = 115200  # 波特率
    ser.bytesize = serial.EIGHTBITS  # 数据位
    ser.stopbits = serial.STOPBITS_ONE  # 停止位
    ser.parity = serial.PARITY_NONE  # 校验位

    try:
        ser.open()
        if ser.isOpen():
            print('Serial port enabled')

        while (1):
            ser.write(b'\r')  # 发送 Enter 键
            time.sleep(0.2)
            ser.write(b'\r')  # 发送 Enter 键

            recv_data = ser.readline()  # 读取一行数据
            time.sleep(0.2)
            recv_data = ser.readline()  # 读取一行数据

            if recv_data.strip() == b'u-boot=>':
                ser.write(b'mmc dev 1\r')
                time.sleep(0.3)

                ser.write(Bin_Command.encode())
                time.sleep(0.5)

                ser.write(b'cp.b 0x48000000 0x7e0000 0x20000\r')
                time.sleep(0.5)

                ser.write(b'bootaux 0x7e0000\r')
                time.sleep(0.2)
                print('Start complete')

                input("Press Enter to continue...")
                sys.stdout.flush()
                break

            else:
                print(recv_data.strip())
                time.sleep(0.1)

    except serial.SerialException as e:
        print('Failed to open the serial port:', str(e))
        while True:
            time.sleep(1)










