import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QComboBox
from PyQt5.QtCore import QThread, pyqtSignal

class SerialThread(QThread):
    received_data = pyqtSignal(str)

    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port

    def run(self):
        while True:
            if self.serial_port.in_waiting:
                data = self.serial_port.readline().decode().strip()
                self.received_data.emit(data)

class SerialTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('485 test')
        self.resize(400, 400)

        # 创建串口对象
        self.serial_port = serial.Serial()

        # 设置串口参数
        self.serial_port.baudrate = 115200
        self.serial_port.bytesize = serial.EIGHTBITS
        self.serial_port.stopbits = serial.STOPBITS_ONE
        self.serial_port.parity = serial.PARITY_NONE

        # 创建界面组件
        self.port_combobox = QComboBox()
        self.send_text = QTextEdit()
        self.send_text.setText("a")  # 设置发送区默认填入字符"a"
        self.receive_text = QTextEdit()
        self.connect_button = QPushButton("connect")
        self.disconnect_button = QPushButton("disconnect")
        self.send_button = QPushButton("send")

        # 获取可用串口列表并添加到端口选择框中
        available_ports = self.get_available_ports()
        self.port_combobox.addItems(available_ports)

        # 绑定按钮点击事件
        self.connect_button.clicked.connect(self.connect_serial)
        self.disconnect_button.clicked.connect(self.disconnect_serial)
        self.send_button.clicked.connect(self.send_data)

        # 创建布局并设置主窗口的中心部件
        layout = QVBoxLayout()
        layout.addWidget(self.port_combobox)
        layout.addWidget(self.send_text)
        layout.addWidget(self.receive_text)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.disconnect_button)
        layout.addWidget(self.send_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 创建串口接收线程
        self.serial_thread = SerialThread(self.serial_port)
        self.serial_thread.received_data.connect(self.display_received_data)

    def closeEvent(self, event):
        self.disconnect_serial()  # 关闭窗口时断开串口连接
        super().closeEvent(event)

    def get_available_ports(self):
        # 获取可用串口列表
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        return ports

    def connect_serial(self):
        # 打开串口
        port_name = self.port_combobox.currentText()
        self.serial_port.port = port_name
        try:
            self.serial_port.open()
            self.receive_text.append("Serial port connected")
            self.connect_button.setEnabled(False)  # 连接按钮置灰
            self.disconnect_button.setEnabled(True)  # 断开按钮可用
            self.serial_thread.start()  # 启动串口接收线程
        except serial.SerialException as e:
            self.receive_text.append(f"Serial port connection failure：{str(e)}")

    def disconnect_serial(self):
        # 关闭串口
        self.serial_thread.terminate()  # 停止串口接收线程
        self.serial_port.close()
        self.receive_text.append("Serial port disconnected")
        self.connect_button.setEnabled(True)  # 连接按钮可用
        self.disconnect_button.setEnabled(False)  # 断开按钮置灰

    def send_data(self):
        # 发送数据
        data = self.send_text.toPlainText().encode()
        try:
            self.serial_port.write(data)
            self.receive_text.append(f"send data：{data.decode()}")
        except serial.SerialException as e:
            self.receive_text.append(f"send failure：{str(e)}")

    def display_received_data(self, data):
        # 显示接收到的数据
        self.receive_text.append(f"receive Data：{data}")

if __name__ == "__main__":
    app = QApplication([])
    window = SerialTool()
    #window.setWindowTitle("485 test")  # 设置窗口标题
    #window.resize(400, 300)  # 设置窗口大小
    #window.send_text.setText("a")  # 设置发送区默认填入字符"a"
    window.show()
    app.exec_()

