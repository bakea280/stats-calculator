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

class LabeledTextbox(QWidget):
    def __init__(self, label_text, call_on_edit=False):
        super().__init__()

        self.label = QLabel(label_text)
        self.textbox = QLineEdit()

        if call_on_edit:
            self.textbox.textEdited.connect(call_on_edit)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        self.setLayout(layout)

        

class NormalCDF(QWidget):
    def __init__(self):
        super().__init__()

        self.mean = 0
        self.stddev = 1
        self.lowerbound = -1*10**10
        self.upperbound = 1*10**10
        self.p = None

        mean_box = LabeledTextbox('mean:', self.mean_changed)
        stddev_box = LabeledTextbox('standard deviation:', self.stddev_changed)
        self.p_label = QLabel('?')

        layout = QVBoxLayout()

        layout.addWidget(mean_box)
        layout.addWidget(stddev_box)
        layout.addWidget(self.p_label)

        # test = QLabel('bruhh')
        # test2 = QLabel('ok')
        # layout.addWidget(test)
        # layout.addWidget(test2)

        self.setLayout(layout)
    
    def calculate_p(self, mean, stddev, lower, upper):
        print(mean, stddev)
        print(lower)
        print(upper)
    
    def mean_changed(self, text):
        print(f'mean edited to:  {text}')
        try:
            self.mean = float(text)
            self.calculate_p(self.mean, self.stddev, self.lowerbound, self.upperbound)
        except:
            self.p = None

    def stddev_changed(self, text):
        print(f'stddev edited to: {text}')
    
app = QApplication(sys.argv)

window = NormalCDF()
window.show()

app.exec()