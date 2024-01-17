# frontend.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from backend import TCPClientBackend
from PyQt5.QtCore import Qt

class TCPClientFrontend(QWidget):
    def __init__(self):
        super().__init__()

        self.backend = TCPClientBackend()
        self.backend.data_received.connect(self.update_received_data)
        self.backend.connection_status_changed.connect(self.update_connection_status)

        self.init_ui()

    def init_ui(self):
        # 创建前端界面组件
        self.ip_label = QLabel('IP address:')
        self.ip_edit = QLineEdit()

        self.port_label = QLabel('Port number:')
        self.port_edit = QLineEdit()

        self.connect_button = QPushButton('Connect')
        self.disconnect_button = QPushButton('Disconnect')
        self.send_button = QPushButton('Send')
        self.send_textedit = QTextEdit()
        self.receive_textedit = QTextEdit()

        # 设置布局
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        input_layout.addWidget(self.ip_label)
        input_layout.addWidget(self.ip_edit)
        input_layout.addWidget(self.port_label)
        input_layout.addWidget(self.port_edit)

        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.disconnect_button)
        button_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.send_textedit)
        main_layout.addWidget(self.receive_textedit)

        self.setLayout(main_layout)

        # 连接信号槽
        self.connect_button.clicked.connect(self.connect_to_server)
        self.disconnect_button.clicked.connect(self.disconnect_from_server)
        self.send_button.clicked.connect(self.send_data)

    def connect_to_server(self):
        ip = self.ip_edit.text()
        port = int(self.port_edit.text())
        self.backend.connect_to_server(ip, port)

    def disconnect_from_server(self):
        self.backend.disconnect_from_server()

    def send_data(self):
        data = self.send_textedit.toPlainText()
        self.backend.send_data(data)

    def update_received_data(self, data):
        self.receive_textedit.append(data)

    def update_connection_status(self, connected):
        if connected:
            self.receive_textedit.append('Connected to the server')
        else:
            self.receive_textedit.append('Disconnected from the server')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    frontend = TCPClientFrontend()
    frontend.show()

    sys.exit(app.exec_())
