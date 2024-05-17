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

        mean_box = LabeledTextbox('mean: ', self.mean_changed)
        
        layout = QVBoxLayout()
        test = QLabel('bruhh')
        test2 = QLabel('ok')
        layout.addWidget(test)
        layout.addWidget(mean_box)
        layout.addWidget(test2)

        self.setLayout(layout)
    
    def mean_changed(self, text):
        print(f'text edited to: {text}')
    
app = QApplication(sys.argv)

window = NormalCDF()
window.show()

app.exec()