import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QButtonGroup, QRadioButton, QFileDialog, QProgressDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtNetwork import QTcpSocket

from PyQt5.QtCore import QTimer

from datetime import datetime
import subprocess
import time
from PyQt5.QtGui import QFont


class TCPClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ITF Dogrobber')
        self.resize(600, 600)

        self.disconnect_flag = False  # 添加断开标志

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


        self.connect_button = QPushButton('connect')
        self.connect_button.setFont(QFont('Microsoft YaHei', 9))
        self.connect_button.setEnabled(True)
        self.disconnect_button = QPushButton('disconnect')
        self.disconnect_button.setFont(QFont('Microsoft YaHei', 9))

        self.send_button = QPushButton('send')
        self.send_button.setFont(QFont('Microsoft YaHei', 9))

        self.view_textedit = QTextEdit()
        self.view_textedit.setFont(QFont('Microsoft YaHei', 9))
        self.send_textedit = QTextEdit()
        self.send_textedit.setFont(QFont('Microsoft YaHei', 9))
        self.send_textedit.setMaximumHeight(60)

        self.view_textedit.setReadOnly(True)
        self.send_format_ascii = False  # 默认发送格式为Hex

        self.hex_radio = QRadioButton('Hex')
        self.ascii_radio = QRadioButton('ASCII')

        # 创建关于导入文件界面组件
        self.file_label = QLabel('select file:')
        self.file_label.setFont(QFont('Microsoft YaHei', 9))
        self.file_edit = QLineEdit()
        self.file_edit.setReadOnly(True)
        self.file_button = QPushButton('select file')
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
        file_layout = QHBoxLayout()
        input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_edit)
        file_layout.addWidget(self.file_button)
        file_layout.addWidget(self.start_button)

        input_layout.addWidget(self.ip_label)
        input_layout.addWidget(self.ip_edit)
        input_layout.addWidget(self.port_label)
        input_layout.addWidget(self.port_edit)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(file_layout)

        main_layout.addWidget(self.hex_radio)
        main_layout.addWidget(self.ascii_radio)
        main_layout.addLayout(button_layout)

        self.send_area_label = QLabel('Sending area:')
        self.send_area_label.setFont(QFont('Microsoft YaHei', 9))
        self.receive_area_label = QLabel('Data display area:')
        self.receive_area_label.setFont(QFont('Microsoft YaHei', 9))


        main_layout.addWidget(self.send_area_label)
        main_layout.addWidget(self.send_textedit)
        main_layout.addWidget(self.receive_area_label)
        main_layout.addWidget(self.view_textedit)


        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.disconnect_button)
        button_layout.addWidget(self.send_button)


        self.setLayout(main_layout)

        # 连接信号槽
        self.connect_button.clicked.connect(self.connect_to_server)
        self.disconnect_button.clicked.connect(self.disconnect_from_server)
        self.send_button.clicked.connect(self.send_data)
        self.hex_radio.clicked.connect(lambda: self.set_send_format(False))
        self.ascii_radio.clicked.connect(lambda: self.set_send_format(True))

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
        self.tcp_socket.connectToHost(ip, port)

        self.tcp_socket.stateChanged.connect(self.handle_connection_status_change)

        self.disconnect_flag = False  # 初始化标志值

    def handle_connection_status_change(self, state):
        if state == QTcpSocket.ConnectedState:
            self.connect_button.setEnabled(False)
        elif state == QTcpSocket.UnconnectedState:
            if not self.disconnect_flag:  # 如果尚未弹出过提示窗口
                QMessageBox.information(self, 'TCP', 'TCP connection disconnected')
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
        args = ["-b", "ram_burn_indus_fw.lst", "imx-boot", file_path]

        if file_path:
            # 在这里执行启动操作，例如读取文件内容等

            # 创建进度条弹窗
            self.progress_dialog = QProgressDialog(self)
            self.progress_dialog.setModal(False)  # 设置为非模态对话框，不会阻塞代码执行
            self.progress_dialog.setWindowTitle('Progress')
            self.progress_dialog.setLabelText('Loading...')
            self.progress_dialog.setRange(0, 100)

            self.progress_dialog.show()

            # 设置进度条弹窗的大小
            self.progress_dialog.setFixedSize(280, 100)

            # 设置计时器，每0.5秒增加25%进度
            self.progress_timer = QTimer(self)
            self.progress_timer.timeout.connect(self.increase_progress)
            self.progress_timer.start(500)

            # 设置定时器，在2秒后触发进度完成操作
            self.complete_timer = QTimer(self)
            self.complete_timer.timeout.connect(self.complete_progress)
            self.complete_timer.setSingleShot(True)
            self.complete_timer.start(3000)

            # 启动进程
            subprocess.run([exe_name] + args, cwd=".")
        else:
            print('Please select a file first')

    def increase_progress(self):
        if self.progress_dialog:
            value = self.progress_dialog.value() + 25
            self.progress_dialog.setValue(value)

    def complete_progress(self):
        self.progress_dialog.setLabelText('Progress completed')  # 更新进度条文本
        self.progress_dialog.setValue(100)

        # 停止计时器
        self.progress_timer.stop()

        # 处理达到100%时的操作，例如显示完成信息或执行其他任务


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = TCPClient()
    client.show()
    sys.exit(app.exec_())