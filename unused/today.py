import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt6.QtCore import QSize

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Statistics Calculator')

        self.label1 = QLabel('Label 1:')
        self.label2 = QLabel('Label 2:')

        self.textbox1 = QLineEdit()
        self.textbox2 = QLineEdit()

        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(self.label1)
        h_layout1.addWidget(self.textbox1)

        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(self.label2)
        h_layout2.addWidget(self.textbox2)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout1)
        v_layout.addLayout(h_layout2)

        self.setLayout(v_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())