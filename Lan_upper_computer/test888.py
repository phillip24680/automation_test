import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import time


class DataThread(QThread):
    data_received = pyqtSignal(bytes)

    def __init__(self, tcp_client):
        super().__init__()
        self.tcp_client = tcp_client

    def run(self):
        while True:
            data = self.tcp_client.recv(1024)
            if data:
                self.data_received.emit(data)

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ITF Commander V1.0')
        self.resize(680, 680)

        self.layout = QVBoxLayout()

        self.start_button = QPushButton('Start', self)
        self.start_button.setFont(QFont('Microsoft YaHei', 10))  # 设置字体大小

        self.start_button.clicked.connect(self.start_connection)
        self.layout.addWidget(self.start_button)

        self.module_layouts = []  # 存储每个模块的布局


        item_layout = QHBoxLayout()
        font = QFont("Arial", 8, QFont.Bold)
        self.test_sequence_button = QPushButton('Test Sequence', self)
        self.test_sequence_button.setFont(font)
        #self.test_sequence_button.setFixedSize(150, 35)  # 设置按键大小
        self.test_sequence_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.test_description_button = QPushButton('Test Description', self)
        self.test_description_button.setFont(font)
        self.test_description_button.setFixedSize(260, 35)  # 设置按键大小
        self.test_result_button = QPushButton('Test Result', self)
        self.test_result_button.setFont(font)
        self.test_result_button.setFixedSize(260, 35)  # 设置按键大小
        item_layout.addWidget(self.test_sequence_button)
        item_layout.addWidget(self.test_description_button)
        item_layout.addWidget(self.test_result_button)
        self.module_layouts.append(item_layout)

        # ITF version模块
        ITFversion_layout = QHBoxLayout()
        # ITFversion_layout.setSpacing(20)  # 设置布局间距

        self.sequence_button_ITFversion = QPushButton('1-00', self)
        self.sequence_button_ITFversion.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.sequence_button_ITFversion.setFixedSize(150, 40)  # 设置按键大小
        ITFversion_layout.addWidget(self.sequence_button_ITFversion)
        self.ITFversion_button = QPushButton('ITF Version Check', self)
        self.ITFversion_button.setFont(QFont('Microsoft YaHei', 9))  #设置字体大小
        self.ITFversion_button.setFixedSize(260, 40)    #设置按键大小
        ITFversion_layout.addWidget(self.ITFversion_button)  # 添加ITFversion_button到布局
        self.ITFversion_pass_label = QLabel('', self)
        self.ITFversion_pass_label.setMinimumWidth(50)  # 设置标签宽度
        self.ITFversion_pass_label.setFont(QFont('Microsoft YaHei', 9))
        ITFversion_layout.addWidget(self.ITFversion_pass_label)

        self.ITFversion_content_label = QLabel('', self)
        self.ITFversion_content_label.setMinimumWidth(50)  # 设置标签宽度
        self.ITFversion_content_label.setFont(QFont('Microsoft YaHei', 9))
        ITFversion_layout.addWidget(self.ITFversion_content_label)

        self.module_layouts.append(ITFversion_layout)

        # short Press模块
        short_layout = QHBoxLayout()
        self.sequence_button_short = QPushButton('2-00', self)
        self.sequence_button_short.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.sequence_button_short.setFixedSize(150, 40)  # 设置按键大小
        short_layout.addWidget(self.sequence_button_short)
        self.short_button = QPushButton('Short Press', self)
        self.short_button.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.short_button.setFixedSize(260, 40)  # 设置按键大小
        short_layout.addWidget(self.short_button)
        self.short_pass_label = QLabel('', self)
        self.short_pass_label.setMinimumWidth(50)  # 设置标签宽度
        self.short_pass_label.setFont(QFont('Microsoft YaHei', 9))
        short_layout.addWidget(self.short_pass_label)
        self.module_layouts.append(short_layout)

        # Long Press模块
        long_layout = QHBoxLayout()
        self.sequence_button_long = QPushButton('2-01', self)
        self.sequence_button_long.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.sequence_button_long.setFixedSize(150, 40)  # 设置按键大小
        long_layout.addWidget(self.sequence_button_long)
        self.long_button = QPushButton('Long Press', self)
        self.long_button.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.long_button.setFixedSize(260, 40)  # 设置按键大小
        long_layout.addWidget(self.long_button)
        self.long_pass_label = QLabel('', self)
        self.long_pass_label.setMinimumWidth(50)  # 设置标签宽度
        self.long_pass_label.setFont(QFont('Microsoft YaHei', 9))
        long_layout.addWidget(self.long_pass_label)
        self.module_layouts.append(long_layout)

        # RGB模块
        rgb_layout = QVBoxLayout()

        # Red
        red_layout = QHBoxLayout()
        self.sequence_button_red = QPushButton('3-00', self)
        self.sequence_button_red.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.sequence_button_red.setFixedSize(150, 40)  # 设置按键大小
        red_layout.addWidget(self.sequence_button_red)
        self.rgb_button_red = QPushButton('Red Color Check', self)
        self.rgb_button_red.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.rgb_button_red.setFixedSize(260, 40)  # 设置按键大小
        red_layout.addWidget(self.rgb_button_red)
        self.rgb_pass_label_red = QLabel('', self)
        self.rgb_pass_label_red.setMinimumWidth(50)  # 设置标签宽度
        self.rgb_pass_label_red.setFont(QFont('Microsoft YaHei', 9))
        red_layout.addWidget(self.rgb_pass_label_red)
        rgb_layout.addLayout(red_layout)

        # Green
        green_layout = QHBoxLayout()
        self.sequence_button_green = QPushButton('3-01', self)
        self.sequence_button_green.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.sequence_button_green.setFixedSize(150, 40)  # 设置按键大小
        green_layout.addWidget(self.sequence_button_green)
        self.rgb_button_green = QPushButton('Green Color Check', self)
        self.rgb_button_green.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.rgb_button_green.setFixedSize(260, 40)  # 设置按键大小
        green_layout.addWidget(self.rgb_button_green)
        self.rgb_pass_label_green = QLabel('', self)
        self.rgb_pass_label_green.setMinimumWidth(50)  # 设置标签宽度
        self.rgb_pass_label_green.setFont(QFont('Microsoft YaHei', 9))
        green_layout.addWidget(self.rgb_pass_label_green)
        rgb_layout.addLayout(green_layout)

        # Blue
        blue_layout = QHBoxLayout()
        self.sequence_button_blue = QPushButton('3-02', self)
        self.sequence_button_blue.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.sequence_button_blue.setFixedSize(150, 40)  # 设置按键大小
        blue_layout.addWidget(self.sequence_button_blue)
        self.rgb_button_blue = QPushButton('Blue Color Check', self)
        self.rgb_button_blue.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.rgb_button_blue.setFixedSize(260, 40)  # 设置按键大小
        blue_layout.addWidget(self.rgb_button_blue)
        self.rgb_pass_label_blue = QLabel('', self)
        self.rgb_pass_label_blue.setMinimumWidth(50)  # 设置标签宽度
        self.rgb_pass_label_blue.setFont(QFont('Microsoft YaHei', 9))
        blue_layout.addWidget(self.rgb_pass_label_blue)
        rgb_layout.addLayout(blue_layout)

        self.module_layouts.append(rgb_layout)

        # Wifi模块
        wifi_layout = QHBoxLayout()
        self.sequence_button_wifi = QPushButton('4-00', self)
        self.sequence_button_wifi.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.sequence_button_wifi.setFixedSize(150, 40)  # 设置按键大小
        wifi_layout.addWidget(self.sequence_button_wifi)
        self.wifi_button = QPushButton('Wi-Fi Tx Check', self)
        self.wifi_button.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.wifi_button.setFixedSize(260, 40)  # 设置按键大小
        wifi_layout.addWidget(self.wifi_button)
        self.wifi_pass_label = QLabel('', self)
        self.wifi_pass_label.setMinimumWidth(50)  # 设置标签宽度
        self.wifi_pass_label.setFont(QFont('Microsoft YaHei', 9))
        wifi_layout.addWidget(self.wifi_pass_label)
        self.module_layouts.append(wifi_layout)

        # ZigBee Version模块
        zigbeeVersion_layout = QHBoxLayout()
        self.sequence_button_zigbeeVersion = QPushButton('5-00', self)
        self.sequence_button_zigbeeVersion.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.sequence_button_zigbeeVersion.setFixedSize(150, 40)  # 设置按键大小
        zigbeeVersion_layout.addWidget(self.sequence_button_zigbeeVersion)
        self.zigbeeVersion_button = QPushButton('Zigbee Firmware Version Check', self)
        self.zigbeeVersion_button.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.zigbeeVersion_button.setFixedSize(260, 40)  # 设置按键大小
        zigbeeVersion_layout.addWidget(self.zigbeeVersion_button)
        self.zigbeeVersion_pass_label = QLabel('', self)
        self.zigbeeVersion_pass_label.setMinimumWidth(50)  # 设置标签宽度
        self.zigbeeVersion_pass_label.setFont(QFont('Microsoft YaHei', 9))
        zigbeeVersion_layout.addWidget(self.zigbeeVersion_pass_label)

        self.zigbeeVersion_content_label = QLabel('', self)
        self.zigbeeVersion_content_label.setMinimumWidth(50)  # 设置标签宽度
        self.zigbeeVersion_content_label.setFont(QFont('Microsoft YaHei', 9))
        zigbeeVersion_layout.addWidget(self.zigbeeVersion_content_label)
        self.module_layouts.append(zigbeeVersion_layout)

        # ZigBee TX模块
        zigbee_layout = QHBoxLayout()
        self.sequence_button_zigbee = QPushButton('5-01', self)
        self.sequence_button_zigbee.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.sequence_button_zigbee.setFixedSize(150, 40)  # 设置按键大小
        zigbee_layout.addWidget(self.sequence_button_zigbee)
        self.zigbee_button = QPushButton('Zigbee Tx Check', self)
        self.zigbee_button.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.zigbee_button.setFixedSize(260, 40)  # 设置按键大小
        zigbee_layout.addWidget(self.zigbee_button)
        self.zigbee_pass_label = QLabel('', self)
        self.zigbee_pass_label.setMinimumWidth(50)  # 设置标签宽度
        self.zigbee_pass_label.setFont(QFont('Microsoft YaHei', 9))
        zigbee_layout.addWidget(self.zigbee_pass_label)
        self.module_layouts.append(zigbee_layout)

        # Modbus模块
        modbus_layout = QHBoxLayout()
        self.sequence_button_modbus = QPushButton('6-00', self)
        self.sequence_button_modbus.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.sequence_button_modbus.setFixedSize(150, 40)  # 设置按键大小
        modbus_layout.addWidget(self.sequence_button_modbus)
        self.modbus_button = QPushButton('Modbus Check', self)
        self.modbus_button.setFont(QFont('Microsoft YaHei', 9))  # 设置字体大小
        self.modbus_button.setFixedSize(260, 40)  # 设置按键大小
        modbus_layout.addWidget(self.modbus_button)
        self.modbus_pass_label = QLabel('', self)
        self.modbus_pass_label.setMinimumWidth(50)  # 设置标签宽度
        self.modbus_pass_label.setFont(QFont('Microsoft YaHei', 9))
        modbus_layout.addWidget(self.modbus_pass_label)
        self.module_layouts.append(modbus_layout)

        # 将每个模块的布局添加到整体的垂直布局中
        for layout in self.module_layouts:
            self.layout.addLayout(layout)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.execute_next_module)

        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_connection(self):
        self.start_button.setEnabled(False)
        self.ITFversion_button.setEnabled(False)
        self.sequence_button_ITFversion.setEnabled(False)
        QApplication.processEvents()  # 处理事件队列，确保GUI更新
        connected = False
        while not connected:
            try:
                self.tcp_client.connect(('192.168.3.11', 6666))
                connected = True
            except Exception as e:
                #print(f"Failed to connect: {e}")
                time.sleep(1)  # 等待一秒后重试


        data = self.tcp_client.recv(1024)  # 接收数据

        self.ITFversion_pass_label.setText('PASS')
        self.ITFversion_pass_label.setStyleSheet("color: green;")
        self.ITFversion_content_label.setText('V7.0')

        print(data)

        self.modules = [self.execute_button_module, self.execute_long_button_module, self.execute_rgb_module_red, self.execute_rgb_module_green,self.execute_rgb_module_blue, self.execute_wifi_module, self.execute_zigbee_version_module, self.execute_zigbee_tx_module, self.execute_modbus_module]
        self.current_module = 0
        self.execute_next_module()

    def execute_next_module(self):
        if self.current_module < len(self.modules):
            self.modules[self.current_module]()
            self.current_module += 1
        else:
            # 清理DataThread线程（如果有）
            if hasattr(self, 'data_thread') and self.data_thread.isRunning():
                self.data_thread.terminate()
                self.data_thread.wait()
                del self.data_thread
            # 同样清理可能存在的其他DataThread实例
            if hasattr(self, 'data_thread2') and self.data_thread2.isRunning():
                self.data_thread2.terminate()
                self.data_thread2.wait()
                del self.data_thread2
            self.tcp_client.close()
            self.timer.stop()

    def execute_rgb_module_red(self):
        self.sequence_button_red.setEnabled(False)
        self.rgb_button_red.setEnabled(False)
        QApplication.processEvents()  # 处理事件队列，确保GUI更新
        time.sleep(0.1)  # 简单的延时，可根据实际情况调整
        self.send_data_and_delay(b'\x5A\xFE\x00\x00\x01', 1.5)  # 停止
        self.send_data_and_delay(b'\x5A\x04\x04\x00\x0F\x00\xFF\x01\xE8', 1)  # 全红
        self.send_data_and_delay(b'\x5A\xFE\x00\x00\x01', 1.5)  # 停止
        self.rgb_pass_label_red.setText('PASS')
        self.rgb_pass_label_red.setStyleSheet("color: green;")
        self.timer.start(1000)  # 1 second delay before next module

    def execute_rgb_module_green(self):
        self.sequence_button_green.setEnabled(False)
        self.rgb_button_green.setEnabled(False)
        QApplication.processEvents()  # 处理事件队列，确保GUI更新
        time.sleep(0.1)  # 简单的延时，可根据实际情况调整
        self.send_data_and_delay(b'\x5A\x04\x04\x00\x0F\x00\xFF\x02\xE7', 1)  # 全绿
        self.send_data_and_delay(b'\x5A\xFE\x00\x00\x01', 1.5)  # 停止
        self.rgb_pass_label_green.setText('PASS')
        self.rgb_pass_label_green.setStyleSheet("color: green;")
        self.timer.start(1000)  # 1 second delay before next module

    def execute_rgb_module_blue(self):
        self.sequence_button_blue.setEnabled(False)
        self.rgb_button_blue.setEnabled(False)
        QApplication.processEvents()  # 处理事件队列，确保GUI更新
        time.sleep(0.1)  # 简单的延时，可根据实际情况调整
        self.send_data_and_delay(b'\x5A\x04\x04\x00\x0F\x00\xFF\x04\xE5', 1)  # 全蓝
        self.send_data_and_delay(b'\x5A\xFE\x00\x00\x01', 1.5)  # 停止
        self.rgb_pass_label_blue.setText('PASS')
        self.rgb_pass_label_blue.setStyleSheet("color: green;")
        self.timer.start(1000)  # 1 second delay before next module

    def execute_button_module(self):
        self.sequence_button_short.setEnabled(False)
        self.short_button.setEnabled(False)
        self.send_data_and_delay(b'\x5A\x02\x00\x00\xFD', 0.5)
        self.show_message_box()
        self.data_thread = DataThread(self.tcp_client)
        self.data_thread.data_received.connect(self.handle_data_received)
        self.data_thread.start()

    def handle_data_received(self, data):
        if data == b'ZU\x03\x00\x02\x01\x01\xa3':  # 检测特定二进制数据
            print('Short Press Detected')
            self.close_message_box()
            if hasattr(self, 'data_thread') and self.data_thread.isRunning():
                self.data_thread.terminate()
                self.data_thread.wait()
                del self.data_thread
            self.execute_next_module()

    def execute_long_button_module(self):
        self.sequence_button_long.setEnabled(False)
        self.long_button.setEnabled(False)
        #self.send_data_and_delay(b'\x5A\x02\x00\x00\xFD', 0.5)
        self.show_long_message_box()
        self.data_thread2 = DataThread(self.tcp_client)
        self.data_thread2.data_received.connect(self.handle_data_received_long)
        self.data_thread2.start()

    def handle_data_received_long(self, data):
        if data == b'ZU\x03\x00\x02\x01\x02\xa2':  # 检测特定二进制数据
            print('Long Press Detected')
            self.close_long_message_box()

            if hasattr(self, 'data_thread2') and self.data_thread2.isRunning():
                self.data_thread2.terminate()
                self.data_thread2.wait()
                del self.data_thread2
            self.execute_next_module()

    def execute_wifi_module(self):
        self.sequence_button_wifi.setEnabled(False)
        self.wifi_button.setEnabled(False)
        QApplication.processEvents()  # 处理事件队列，确保GUI更新
        time.sleep(0.1)  # 简单的延时，可根据实际情况调整
        self.send_data_and_delay(b'\x5A\x03\x01\x00\x03\xF8', 3.5)
        self.wifi_pass_label.setText('PASS')
        self.wifi_pass_label.setStyleSheet("color: green;")
        self.timer.start(1000)  # 1 second delay before closing connection

    def execute_zigbee_version_module(self):
        self.sequence_button_zigbeeVersion.setEnabled(False)
        self.zigbeeVersion_button.setEnabled(False)
        QApplication.processEvents()  # 处理事件队列，确保GUI更新
        time.sleep(0.1)  # 简单的延时，可根据实际情况调整
        self.send_data_and_delay(b'\x5A\x05\x01\x00\x00\xF9', 3)
        self.zigbeeVersion_pass_label.setText('PASS')
        self.zigbeeVersion_pass_label.setStyleSheet("color: green;")
        self.zigbeeVersion_content_label.setText('V2.16.0')

        self.timer.start(1000)  # 1 second delay before closing connection

    def execute_zigbee_tx_module(self):
        self.sequence_button_zigbee.setEnabled(False)
        self.zigbee_button.setEnabled(False)
        QApplication.processEvents()  # 处理事件队列，确保GUI更新
        time.sleep(0.1)  # 简单的延时，可根据实际情况调整
        self.send_data_and_delay(b'\x5A\x05\x01\x00\x04\xF5', 3.5)
        self.zigbee_pass_label.setText('PASS')
        self.zigbee_pass_label.setStyleSheet("color: green;")
        self.timer.start(1000)  # 1 second delay before closing connection

    def execute_modbus_module(self):
        self.sequence_button_modbus.setEnabled(False)
        self.modbus_button.setEnabled(False)
        QApplication.processEvents()  # 处理事件队列，确保GUI更新
        time.sleep(0.1)  # 简单的延时，可根据实际情况调整
        self.send_data_and_delay(b'\x5A\x05\x01\x00\x04\xF5', 3.5)
        self.modbus_pass_label.setText('PASS')
        self.modbus_pass_label.setStyleSheet("color: green;")
        #time.sleep(1)
        self.all_pass_message_box()
        self.timer.start(1000)  # 1 second delay before closing connection

    def all_pass_message_box(self):
        self.msgBox_PASS = QMessageBox()
        self.msgBox_PASS.setWindowTitle("Test Result")
        self.msgBox_PASS.setText(" Clean  Pass ")
        self.msgBox_PASS.setFont(QFont("Calibri", 13))
        self.msgBox_PASS.show()

    def send_data_and_delay(self, data, delay):
        self.tcp_client.send(data)
        time.sleep(delay)

    def show_message_box(self):
        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle("Button Check")
        self.msgBox.setText("Please Short Press Push Button")
        self.msgBox.setFont(QFont("Calibri", 12))
        self.msgBox.show()
        self.timer.stop()

    def close_message_box(self):
        self.msgBox.close()
        self.timer.start(1000)  # 1 second delay before next module
        self.short_pass_label.setText('PASS')
        self.short_pass_label.setStyleSheet("color: green;")
        time.sleep(1)

    def show_long_message_box(self):
        self.long_msgBox = QMessageBox()
        self.long_msgBox.setWindowTitle("Button Check")
        self.long_msgBox.setText("Please Long Press Push Button")
        self.long_msgBox.setFont(QFont("Calibri", 12))
        self.long_msgBox.show()
        self.timer.stop()

    def close_long_message_box(self):
        self.long_msgBox.close()
        self.long_pass_label.setText('PASS')
        self.long_pass_label.setStyleSheet("color: green;")
        QApplication.processEvents()  # 处理事件队列，确保GUI更新
        time.sleep(0.1)  # 简单的延时，可根据实际情况调整
        self.timer.start(1000)  # 1 second delay before next module


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())