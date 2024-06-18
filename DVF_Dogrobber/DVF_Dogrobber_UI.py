import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QButtonGroup, QRadioButton, QFileDialog, QProgressDialog, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from datetime import datetime
import subprocess
import time
from PyQt5.QtCore import QTimer

from tcp_client import send_data_to_server

class ExecuteProcessThread(QThread):
    progress_updated = pyqtSignal(int)
    process_finished = pyqtSignal(bool)

    def __init__(self, exe_name, args):
        super().__init__()
        self.exe_name = exe_name
        self.args = args

    def run(self):
        process = subprocess.Popen([self.exe_name] + self.args, cwd=".")
        return_code = process.wait()

class TCPClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DVF Dogrobber V1.0')
        self.resize(800, 400)


        # 添加图标
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap('icon.png'))  # 替换为你的图标路径
        self.icon_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        # 创建标题栏
        self.header_label = QLabel('DVF Dogrobber  v1.0')
        self.header_label.setFont(QFont('Microsoft YaHei', 15))
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("background-color: #32CD32; color: white;")
        self.header_label.setFixedHeight(50)

        # 创建界面组件
        self.ip_label = QLabel('IP address:')
        self.ip_label.setFont(QFont('Microsoft YaHei', 10))
        self.ip_edit = QLineEdit('192.168.3.11')
        self.ip_edit.setFont(QFont('Microsoft YaHei', 10))
        self.ip_edit.setStyleSheet("color: gray;")
        self.ip_edit.setEnabled(False)

        self.port_label = QLabel('Port number:')
        self.port_label.setFont(QFont('Microsoft YaHei', 10))
        self.port_edit = QLineEdit('6666')
        self.port_edit.setFont(QFont('Microsoft YaHei', 10))
        self.port_edit.setStyleSheet("color: gray;")
        self.port_edit.setEnabled(False)

        # 分组：Firmware Download
        firmware_group = QGroupBox("Firmware Download")
        firmware_layout = QVBoxLayout()

        self.firmware_file_label = QLabel('Select Test Firmware:')
        self.firmware_file_label.setFont(QFont('Microsoft YaHei', 10))
        self.firmware_file_edit = QLineEdit()
        self.firmware_file_edit.setReadOnly(True)
        self.firmware_file_button = QPushButton('Select File')
        self.firmware_file_button.setFont(QFont('Microsoft YaHei', 10))
        self.download_button = QPushButton('Download Program')
        self.download_button.setFont(QFont('Microsoft YaHei', 10))

        # 创建文件选择相关的水平布局
        firmware_file_layout = QHBoxLayout()
        firmware_file_layout.addWidget(self.firmware_file_label)
        firmware_file_layout.addWidget(self.firmware_file_edit)
        firmware_file_layout.addWidget(self.firmware_file_button)
        firmware_layout.addLayout(firmware_file_layout)  # 添加水平布局到垂直布局中
        firmware_layout.addWidget(self.download_button)  # 下载按钮保持原位置
        firmware_group.setLayout(firmware_layout)

        # 分组：Configuration
        config_group = QGroupBox("Configuration")
        config_layout = QVBoxLayout()
        self.configuration_file_label = QLabel('Select Configure File:')
        self.configuration_file_label.setFont(QFont('Microsoft YaHei', 10))
        self.configuration_file_edit = QLineEdit()
        self.configuration_file_edit.setReadOnly(True)
        self.configuration_file_button = QPushButton('Select File')
        self.configuration_file_button.setFont(QFont('Microsoft YaHei', 10))
        self.config_button = QPushButton('Start Configuration')
        self.config_button.setFont(QFont('Microsoft YaHei', 10))
        # 创建文件选择相关的水平布局
        config_file_layout = QHBoxLayout()
        config_file_layout.addWidget(self.configuration_file_label)
        config_file_layout.addWidget(self.configuration_file_edit)
        config_file_layout.addWidget(self.configuration_file_button)
        config_layout.addLayout(config_file_layout)  # 添加水平布局到垂直布局中
        config_layout.addWidget(self.config_button)  # 配置开始按钮保持原位置
        config_group.setLayout(config_layout)

        # 主布局
        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        header_layout.addWidget(self.header_label)

        input_layout.addWidget(self.ip_label)
        input_layout.addWidget(self.ip_edit)
        input_layout.addWidget(self.port_label)
        input_layout.addWidget(self.port_edit)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(firmware_group)
        main_layout.addWidget(config_group)
        main_layout.addLayout(button_layout)  # 即使当前为空布局也保留，以便后续可能的使用
        main_layout.addWidget(self.icon_label)

        self.setLayout(main_layout)

        # 连接信号槽
        self.firmware_file_button.clicked.connect(self.select_firmware_file)
        self.download_button.clicked.connect(self.download_button_clicked)
        self.configuration_file_button.clicked.connect(self.select_configuration_file)
        self.config_button.clicked.connect(self.config_button_clicked)  # 更改为新的槽函数

        self.tcp_socket = QTcpSocket(self)

    def select_firmware_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Firmware')
        if file_path:
            self.firmware_file_edit.setText(file_path)

    def select_configuration_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Configuration File')
        if file_path:
            self.configuration_file_edit.setText(file_path)

    def show_configuration_message(self):
        # 弹窗显示配置信息
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Configuration Status")

        message_box.setText("Configuring...")
        self.timer = QTimer.singleShot(1000, lambda: self.update_message_box(message_box, self.response_verify))

        message_box.exec_()

    def update_message_box(self, message_box, new_text):
        # 更新弹窗文本并关闭弹窗
        message_box.setText(new_text)
        #message_box.button(QMessageBox.Ok).click()

    def config_button_clicked(self):
        self.response_verify = send_data_to_server(self.configuration_file_edit.text())
        self.show_configuration_message()

    def select_firmware_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'select file')
        if file_path:
            self.firmware_file_edit.setText(file_path)

    def download_button_clicked(self):
        file_path = self.firmware_file_edit.text()
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_icon = QIcon('tool_icon.png')  # 替换为你的图标路径
    app.setWindowIcon(app_icon)
    client = TCPClient()
    client.show()
    sys.exit(app.exec_())