import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
    QLayout
)

from layout_colorwidget import Color
from normalcdf import NormalCDF

# class NormalCDFTab(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.label1 = QLabel('Label 1:')
#         self.label2 = QLabel('Label 2:')

#         self.textbox1 = QLineEdit()
#         self.textbox2 = QLineEdit()

#         # self.textbox1.setSizePolicy(
#         #     QSizePolicy.Policy.Fixed,
#         #     QSizePolicy.Policy.Fixed,
#         # )
#         # self.textbox2.setSizePolicy(
#         #     QSizePolicy.Policy.Fixed,
#         #     QSizePolicy.Policy.Fixed,
#         # )

#         h_layout1 = QHBoxLayout()
#         h_layout1.addWidget(self.label1)
#         h_layout1.addWidget(self.textbox1)

#         h_layout2 = QHBoxLayout()
#         h_layout2.addWidget(self.label2)
#         h_layout2.addWidget(self.textbox2)

#         v_layout = QVBoxLayout()
#         v_layout.addLayout(h_layout1)
#         v_layout.addLayout(h_layout2)

#         v_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)

#         self.setLayout(v_layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Statistics Calculator")
        self.setMinimumSize(QSize(480, 270))

        tabs = QTabWidget()
        # tabs.setTabPosition(QTabWidget.TabPosition.West)
        # tabs.setMovable(True)

        
        tabs.addTab(NormalCDF(), 'NormalCDF')
        
        for n, color in enumerate(["red", "green", "blue", "yellow"]):
            tabs.addTab(Color(color), color)

        self.setCentralWidget(tabs)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()