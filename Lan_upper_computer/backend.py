# backend.py
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtNetwork import QTcpSocket

class TCPClientBackend(QObject):
    data_received = pyqtSignal(str)
    connection_status_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.tcp_socket = QTcpSocket(self)

        self.tcp_socket.readyRead.connect(self.receive_data)
        self.tcp_socket.stateChanged.connect(self.handle_connection_status_change)

    @pyqtSlot()
    def connect_to_server(self, ip, port):
        self.tcp_socket.connectToHost(ip, port)

    @pyqtSlot()
    def disconnect_from_server(self):
        if self.tcp_socket.state() == QTcpSocket.ConnectedState:
            self.tcp_socket.disconnectFromHost()

    @pyqtSlot(str)
    def send_data(self, data):
        if self.tcp_socket.state() == QTcpSocket.ConnectedState:
            self.tcp_socket.writeData(bytes(data, encoding='utf-8'))

    def receive_data(self):
        data = self.tcp_socket.readAll().data().decode()
        self.data_received.emit(data)

    def handle_connection_status_change(self, state):
        if state == QTcpSocket.ConnectedState:
            self.connection_status_changed.emit(True)
        elif state == QTcpSocket.UnconnectedState:
            self.connection_status_changed.emit(False)
