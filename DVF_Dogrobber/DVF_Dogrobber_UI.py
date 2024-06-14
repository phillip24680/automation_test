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

        # ...初始化代码...
        self.configuration_count = 1  # 新增变量，记录start_button2点击次数

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

        self.file_label = QLabel('Select Test Firmware:')
        self.file_label.setFont(QFont('Microsoft YaHei', 10))
        self.file_edit = QLineEdit()
        self.file_edit.setReadOnly(True)
        self.file_button = QPushButton('Select File')
        self.file_button.setFont(QFont('Microsoft YaHei', 10))
        self.start_button = QPushButton('Download Program')
        self.start_button.setFont(QFont('Microsoft YaHei', 10))
        # 创建文件选择相关的水平布局
        firmware_file_layout = QHBoxLayout()
        firmware_file_layout.addWidget(self.file_label)
        firmware_file_layout.addWidget(self.file_edit)
        firmware_file_layout.addWidget(self.file_button)
        firmware_layout.addLayout(firmware_file_layout)  # 添加水平布局到垂直布局中
        firmware_layout.addWidget(self.start_button)  # 下载按钮保持原位置
        firmware_group.setLayout(firmware_layout)

        # 分组：Configuration
        config_group = QGroupBox("Configuration")
        config_layout = QVBoxLayout()
        self.file_label2 = QLabel('Select Configure File:')
        self.file_label2.setFont(QFont('Microsoft YaHei', 10))
        self.file_edit2 = QLineEdit()
        self.file_edit2.setReadOnly(True)
        self.file_button2 = QPushButton('Select File')
        self.file_button2.setFont(QFont('Microsoft YaHei', 10))
        self.start_button2 = QPushButton('Start Configuration')
        self.start_button2.setFont(QFont('Microsoft YaHei', 10))
        # 创建文件选择相关的水平布局
        config_file_layout = QHBoxLayout()
        config_file_layout.addWidget(self.file_label2)
        config_file_layout.addWidget(self.file_edit2)
        config_file_layout.addWidget(self.file_button2)
        config_layout.addLayout(config_file_layout)  # 添加水平布局到垂直布局中
        config_layout.addWidget(self.start_button2)  # 配置开始按钮保持原位置
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
        self.file_button.clicked.connect(self.select_file)
        self.start_button.clicked.connect(self.start)
        self.file_button2.clicked.connect(self.select_file2)
        self.start_button2.clicked.connect(self.start_button2_clicked)  # 更改为新的槽函数

        self.tcp_socket = QTcpSocket(self)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Firmware')
        if file_path:
            self.file_edit.setText(file_path)

    def select_file2(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Configuration File')
        if file_path:
            self.file_edit2.setText(file_path)

    def start(self):
        print("Starting the process...")

    def show_configuration_message(self):
        # 弹窗显示配置信息
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Configuration Status")
        if self.configuration_count % 2 == 0:
            # 第一次点击
            message_box.setText("Configuring...")
            self.timer = QTimer.singleShot(3000, lambda: self.update_message_box(message_box,
                                                                                 "Normal configuration completed."))
        else:
            # 第二次点击
            message_box.setText("Configuring...")
            self.timer = QTimer.singleShot(3000, lambda: self.update_message_box(message_box,
                                                                                 "Fast configuration completed."))
        message_box.exec_()

    def update_message_box(self, message_box, new_text):
        # 更新弹窗文本并关闭弹窗
        message_box.setText(new_text)
        #message_box.button(QMessageBox.Ok).click()

    def start_button2_clicked(self):
        self.configuration_count += 1
        self.show_configuration_message()

    # 其他原有方法保持不变...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_icon = QIcon('tool_icon.png')  # 替换为你的图标路径
    app.setWindowIcon(app_icon)
    client = TCPClient()
    client.show()
    sys.exit(app.exec_())