import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QButtonGroup, QRadioButton, QFileDialog, QProgressDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtNetwork import QTcpSocket

from PyQt5.QtWidgets import QDialog

from PyQt5.QtCore import QTimer

from datetime import datetime
import subprocess

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal

from PyQt5.QtGui import QIcon

from PyQt5.QtGui import QTextCharFormat, QTextCursor, QTextDocument
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
from serial_test import SerialTool

import time
from pythonping import ping


class PingThread(QThread):
    ping_result = pyqtSignal(str)

    def __init__(self, host):
        super().__init__()
        self.host = host

    def run(self):
        count = 0
        for response in ping(self.host, count=5, timeout=0.2):
            self.ping_result.emit(str(response))
            time.sleep(0.36)
            count += 1
            if count == 5:
                break

        if response.success:
            self.ping_result.emit(f"{self.host} ping successful.")
        else:
            self.ping_result.emit(f"{self.host} ping failed.")

class ExecuteProcessThread(QThread):
    progress_updated = pyqtSignal(int)
    process_finished = pyqtSignal(bool)

    def __init__(self, exe_name, args):
        super().__init__()
        self.exe_name = exe_name
        self.args = args

    def run(self):
        # 执行命令
        process = subprocess.Popen([self.exe_name] + self.args, cwd=".")
        return_code = process.wait()

class PhotoViewerDialog(QDialog):
    def __init__(self, photo_path, description_text, parent=None):
        super(PhotoViewerDialog, self).__init__(parent)
        self.setWindowTitle("ITF Team Photo")

        # 加载图片
        photo_label = QLabel()
        photo_pixmap = QPixmap(photo_path)
        photo_label.setPixmap(photo_pixmap)
        photo_label.setAlignment(Qt.AlignCenter)

        # 设置 QLabel 的最大宽度和最大高度
        max_width = 850  # 设置您期望的最大宽度
        max_height = 850  # 设置您期望的最大高度
        photo_label.setMaximumSize(max_width, max_height)

        # 创建滚动区域
        scroll_area = QVBoxLayout()
        scroll_area.addWidget(photo_label)

        # 添加滚动的文字说明
        self.description_text_edit = QTextEdit()
        self.description_text_edit.setPlainText(description_text)
        self.description_text_edit.setReadOnly(True)

        # 设置文字格式
        self.set_text_format()

        # 创建垂直布局
        v_layout = QVBoxLayout()
        v_layout.addLayout(scroll_area)
        v_layout.addWidget(self.description_text_edit)

        self.setLayout(v_layout)

        # 设置定时器，每隔一段时间滚动文字
        self.scroll_timer = QTimer(self)
        self.scroll_timer.timeout.connect(self.scroll_description)
        self.scroll_timer.start(2500)  # 设置滚动间隔为 3 秒

    def set_text_format(self):
        cursor = self.description_text_edit.textCursor()

        # 设置加粗
        format_bold = QTextCharFormat()
        #format_bold.setFontWeight(QFont.Bold)
        cursor.setPosition(0)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.mergeCharFormat(format_bold)

        # 设置颜色为紫色
        format_purple = QTextCharFormat()
        format_purple.setForeground(Qt.magenta)
        cursor.mergeCharFormat(format_purple)

        # 设置文字的字体和大小
        font = QFont("Microsoft YaHei", 10)  # 设置字体为微软雅黑，大小为10
        self.description_text_edit.setFont(font)

        # 将背景颜色更改为更淡的蓝色
        self.description_text_edit.setStyleSheet("background-color: #FFFFE0;")

    def scroll_description(self):
        current_scroll_value = self.description_text_edit.verticalScrollBar().value()
        max_scroll_value = self.description_text_edit.verticalScrollBar().maximum()

        # 如果当前滚动值已经是最底部，则滑动到最顶部
        if current_scroll_value == max_scroll_value:
            # 滑动到最顶部
            self.description_text_edit.verticalScrollBar().setValue(0)
        else:
            # 滑动到下一步位置
            self.description_text_edit.verticalScrollBar().setValue(current_scroll_value + 10)


class TCPClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(' ')
        self.resize(800, 800)

        # 创建界面组件
        self.hex_radio = QRadioButton('Hex')
        self.ascii_radio = QRadioButton('ASCII')

        self.disconnect_flag = False  # 添加断开标志

        #添加图标
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap('icon.png'))  # 替换icon.png为您的图标文件名
        self.icon_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        # 创建界面组件 -- 标题栏
        self.header_label = QLabel('                                    ITF Dogrobber                           V6.0')
        self.header_label.setFont(QFont('Microsoft YaHei', 15))
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("background-color: #32CD32; color: white;")
        self.header_label.setFixedHeight(50)  # 设置高度为40像素


        # 创建界面组件
        self.ip_label = QLabel('IP address:')
        self.ip_label.setFont(QFont('Microsoft YaHei', 9))
        self.ip_edit = QLineEdit()

        self.ip_edit.setText("192.168.3.11")
        self.ip_edit.setFont(QFont('Microsoft YaHei', 9))
        self.ip_edit.setEnabled(False)
        self.ip_edit.setStyleSheet("color: gray;")

        self.port_label = QLabel('Port number:')
        self.port_label.setFont(QFont('Microsoft YaHei', 9))
        self.port_edit = QLineEdit()
        self.port_edit.setText('6666')
        self.port_edit.setFont(QFont('Microsoft YaHei', 9))
        self.port_edit.setEnabled(False)
        self.port_edit.setStyleSheet("color: gray;")

        self.ping_button0 = QPushButton('Ping Eth0 : 192.168.3.10')
        self.ping_button0.setFont(QFont('Microsoft YaHei', 9))
        self.ping_button1 = QPushButton('Ping Eth1 : 192.168.3.11')
        self.ping_button1.setFont(QFont('Microsoft YaHei', 9))

        self.connect_button = QPushButton('Connect')
        self.connect_button.setFont(QFont('Microsoft YaHei', 9))
        self.connect_button.setEnabled(True)
        self.disconnect_button = QPushButton('Disconnect')
        self.disconnect_button.setFont(QFont('Microsoft YaHei', 9))

        self.send_button = QPushButton('Send')
        self.send_button.setFont(QFont('Microsoft YaHei', 9))


        # 添加清除按钮
        self.clear_data_button = QPushButton('Clear Data')
        self.clear_data_button.setFont(QFont('Microsoft YaHei', 9))

        self.view_textedit = QTextEdit()
        self.view_textedit.setFont(QFont('Microsoft YaHei', 10))
        self.send_textedit = QTextEdit()
        self.send_textedit.setFont(QFont('Microsoft YaHei', 10))
        self.send_textedit.setMaximumHeight(60)

        self.view_textedit.setReadOnly(True)
        self.send_format_ascii = False  # 默认发送格式为Hex

        # 创建modbus按钮
        self.modbus_test_button = QPushButton('485 Test')
        self.modbus_test_button.setFont(QFont('Microsoft YaHei', 9))
        self.modbus_test_button.clicked.connect(self.open_serial_tool)

        # 创建关于导入文件界面组件
        self.file_label = QLabel('Select file:')
        self.file_label.setFont(QFont('Microsoft YaHei', 9))
        self.file_edit = QLineEdit()
        self.file_edit.setReadOnly(True)
        self.file_button = QPushButton('Select file')
        self.file_button.setFont(QFont('Microsoft YaHei', 9))
        self.start_button = QPushButton('Download program')
        self.start_button.setFont(QFont('Microsoft YaHei', 9))


        format_group = QButtonGroup()
        format_group.addButton(self.hex_radio)
        format_group.addButton(self.ascii_radio)

        # self.ascii_radio.setChecked(True)  # 默认选中ASCII
        self.hex_radio.setChecked(True)  # 默认选中Hex

        # 设置布局
        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        ping_button_layout = QHBoxLayout()
        file_layout = QHBoxLayout()
        input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        send_button_layout = QHBoxLayout()  # 新增的布局

        header_layout.addWidget(self.header_label)

        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_edit)
        file_layout.addWidget(self.file_button)
        file_layout.addWidget(self.start_button)

        input_layout.addWidget(self.ip_label)
        input_layout.addWidget(self.ip_edit)
        input_layout.addWidget(self.port_label)
        input_layout.addWidget(self.port_edit)

        ping_button_layout.addWidget(self.ping_button0)
        ping_button_layout.addWidget(self.ping_button1)



        main_layout.addLayout(header_layout)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(file_layout)

        main_layout.addLayout(ping_button_layout)

        # main_layout.addWidget(self.hex_radio)
        # main_layout.addWidget(self.ascii_radio)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(send_button_layout)  # 添加新的布局

        self.send_area_label = QLabel('Sending area:')
        self.send_area_label.setFont(QFont('Microsoft YaHei', 9))
        self.receive_area_label = QLabel('Data display area:')
        self.receive_area_label.setFont(QFont('Microsoft YaHei', 9))

        main_layout.addWidget(self.send_area_label)
        main_layout.addWidget(self.send_textedit)
        main_layout.addWidget(self.clear_data_button)
        main_layout.addWidget(self.receive_area_label)

        main_layout.addWidget(self.view_textedit)

        main_layout.addWidget(self.icon_label)

        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.disconnect_button)
        button_layout.addWidget(self.modbus_test_button)

        send_button_layout.addWidget(self.send_button)  # 将发送按钮添加到新的布局

        self.setLayout(main_layout)

        # 连接信号槽
        self.connect_button.clicked.connect(self.connect_to_server)
        self.disconnect_button.clicked.connect(self.disconnect_from_server)
        self.send_button.clicked.connect(self.send_data)

        self.ping_button0.clicked.connect(self.ping_eth0)
        self.ping_button1.clicked.connect(self.ping_eth1)
        # self.hex_radio.clicked.connect(lambda: self.set_send_format(False))
        # self.ascii_radio.clicked.connect(lambda: self.set_send_format(True))

        self.clear_data_button.clicked.connect(self.clear_data)

        # 连接信号槽（关于文件导入）
        self.file_button.clicked.connect(self.select_file)
        self.start_button.clicked.connect(self.start)

        # 创建TCP套接字
        self.tcp_socket = QTcpSocket(self)

        # 关联信号槽
        self.tcp_socket.readyRead.connect(self.receive_data)

    def connect_to_server(self):
        ip = self.ip_edit.text()
        port = int(self.port_edit.text())
        if self.tcp_socket.state() != QTcpSocket.ConnectedState:
            self.tcp_socket.connectToHost(ip, port)
            connected = self.tcp_socket.waitForConnected(1200)  # 设置超时为1.2秒
            if connected:
                self.connect_button.setEnabled(False)
                self.tcp_socket.stateChanged.connect(self.handle_connection_status_change)
            else:
                QMessageBox.information(self, 'TCP', 'TCP connection failed')
                self.connect_button.setEnabled(True)  # 在连接失败时恢复按钮状态
        else:
            QMessageBox.information(self, 'TCP', 'TCP connection already established')

        self.disconnect_flag = False  # 初始化标志值

    def handle_connection_status_change(self, state):
        if state == QTcpSocket.ConnectedState:
            self.connect_button.setEnabled(False)
        elif state == QTcpSocket.UnconnectedState:
            if not self.disconnect_flag:  # 如果尚未弹出过提示窗口
                #QMessageBox.information(self, 'TCP', 'TCP connection disconnected')
                self.connect_button.setEnabled(True)
                self.disconnect_flag = True  # 设置标志为True，表示已经弹出过提示窗口

    def disconnect_from_server(self):
        if self.tcp_socket.state() == QTcpSocket.ConnectedState:
            self.tcp_socket.disconnectFromHost()

            if not self.disconnect_flag:  # 如果尚未弹出过提示窗口
                QMessageBox.information(self, 'TCP', 'TCP connection disconnected')
                self.disconnect_flag = True  # 设置标志为True，表示已经弹出过提示窗口
        else:
            QMessageBox.information(self, 'TCP', 'TCP connection not established')

        self.connect_button.setEnabled(True)

    def receive_data(self):
        if self.send_format_ascii:
            data = self.tcp_socket.readAll().data().decode()
        else:
            hex_data = self.tcp_socket.readAll().toHex().data().decode().upper()
            receive_current_time = datetime.now().time().strftime("%H:%M:%S.%f")[:-3]  #获得当前时间
            data = ' '.join(hex_data[i:i + 2] for i in range(0, len(hex_data), 2))  # 把data数据以每两个字符空一格
            receive_message = f"[{receive_current_time}] Receive:{data}"

            byte_data = bytes.fromhex(hex_data)   #把16进制字符串格式数据转换为字节数组
            if byte_data == b'Forever':
                self.show_photo_viewer()


        self.view_textedit.append(receive_message)

    def set_send_format(self, is_ascii):
        self.send_format_ascii = is_ascii

    def send_data(self):
        if self.tcp_socket.state() == QTcpSocket.ConnectedState:
            data = self.send_textedit.toPlainText()
            if self.send_format_ascii:
                self.tcp_socket.writeData(bytes(data, encoding='utf-8'))
            else:
                send_current_time = datetime.now().time().strftime("%H:%M:%S.%f")[:-3]  # 获得当前时间
                send_message = f"[{send_current_time}] Send:{data}"
                self.view_textedit.append(send_message)  # 把发送数据信息显示在数据显示区
                hex_data = bytes.fromhex(data)
                self.tcp_socket.writeData(hex_data)
        else:
            QMessageBox.information(self, 'TCP', 'Please establish a TCP connection first')

    def clear_data(self):
        self.view_textedit.clear()

    def closeEvent(self, event):
        self.tcp_socket.disconnectFromHost()
        self.tcp_socket.waitForDisconnected()

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'select file')
        if file_path:
            self.file_edit.setText(file_path)

    def start(self):
        file_path = self.file_edit.text()
        exe_name = "uuu.exe"
        args = ["-b", "emmc_burn_indus_fw_ddr.lst", "flash.bin", file_path]

        if file_path:
            # 在开始新任务之前停止并重新启动定时器
            if hasattr(self, 'progress_timer') and self.progress_timer.isActive():
                self.progress_timer.stop()
            # 创建并启动线程
            self.execute_thread = ExecuteProcessThread(exe_name, args)
            #self.execute_thread.process_finished.connect(self.complete_progress)
            self.execute_thread.start()

            # 显示进度条弹窗
            self.show_progress_dialog()
        else:
            print('Please select a file first')


    def show_progress_dialog(self):
        # 创建进度条弹窗
        self.progress_dialog = QProgressDialog(self)
        self.progress_dialog.setModal(False)  # 设置为非模态对话框，不会阻塞代码执行
        self.progress_dialog.setWindowTitle('Progress')
        self.progress_dialog.setLabelText('Loading...')
        self.progress_dialog.setRange(0, 100)
        self.progress_dialog.setValue(0)  # 设置初始值为0


        self.progress_dialog.show()

        # 设置进度条弹窗的大小
        self.progress_dialog.setFixedSize(280, 100)

        # 设置计时器，每0.5秒增加25%进度
        self.progress_timer = QTimer(self)
        self.progress_timer.start(1350)
        self.progress_timer.timeout.connect(self.increase_progress)

    def increase_progress(self):
        if self.progress_dialog and self.progress_dialog.isVisible():
            current_value = self.progress_dialog.value()
            max_value = self.progress_dialog.maximum()
            if current_value < 100:
                value = current_value + 10
                self.progress_dialog.setValue(value)
            else:
                # 进度条达到最大值，关闭进度条弹窗
                self.progress_timer.stop()  # 停止计时器
                self.progress_dialog.close()

    def decrypt_image(self):
        # 打开加密图片并读取数据
        encrypted_path = 'ITF_Team_Photo_encrypted.jpg'
        output_path = 'ITF_Team_Photo_decrypted.jpg'
        with open(encrypted_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        # 提取IV（初始化向量）和加密数据
        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]

        key = b'this_is_a_key123'
        # 创建AES对象并进行解密
        cipher = AES.new(key, AES.MODE_CBC, iv)
        raw_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        # 将解密后的数据写入输出文件
        with open(output_path, 'wb') as output_file:
            output_file.write(raw_data)

    def show_photo_viewer(self):
        self.decrypt_image()    #对'ITF_Team_Photo_encrypted.jpg'照片进行解密
        photo_path = 'ITF_Team_Photo_decrypted.jpg'  # 照片文件路径
        description_text = 'Samson : Patience is the key in life.\n' \
                           'Tom : Connecting people and world.\n' \
                           'Phillip : Experience is the best teacher.\n' \
                           'Sarah : Peace life,Peace world.\n' \
                           'Yuan : You are the best.\n' \
                           'Julien : Leadership lights the way, communication binds us, and support propels everyone forward - together, they illuminate the journey of greatness.'  # 说明文字
        viewer_dialog = PhotoViewerDialog(photo_path, description_text, self)
        viewer_dialog.exec_()
        try:
            os.remove('ITF_Team_Photo_decrypted.jpg')  #删除解密后的照片
        except FileNotFoundError:
            pass  # 如果文件不存在，则忽略

    def open_serial_tool(self):
        self.serial_tool_window = SerialTool()
        self.serial_tool_window.show()

    def ping_eth0(self):
        self.ping_thread = PingThread("192.168.3.10")
        self.ping_thread.ping_result.connect(self.handle_ping_result)
        self.ping_thread.start()

    def ping_eth1(self):
        self.ping_thread = PingThread("192.168.3.11")
        self.ping_thread.ping_result.connect(self.handle_ping_result)
        self.ping_thread.start()

    def handle_ping_result(self, result):
        self.view_textedit.append(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app_icon = QIcon('tool_icon.png')  # 图标文件名
    app.setWindowIcon(app_icon)

    client = TCPClient()
    client.show()
    sys.exit(app.exec_())