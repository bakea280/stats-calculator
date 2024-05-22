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
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression

class LabeledTextbox(QWidget):
    def __init__(self, label_text, call_on_edit=None, regex_filter=None):
        super().__init__()

        self.label = QLabel(label_text)
        self.textbox = QLineEdit()

        if regex_filter:
            regex = QRegularExpression(regex_filter)
            validator = QRegularExpressionValidator(regex, self.textbox)
            self.textbox.setValidator(validator)

        if call_on_edit:
            self.textbox.textEdited.connect(call_on_edit)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        self.setLayout(layout)

equation_regex = '[0-9\Q.+-*/x^(), \E]*' 

class NormalCDF(QWidget):
    def __init__(self):
        super().__init__()

        mean_box = LabeledTextbox('mean (μ):', self.mean_changed, equation_regex)
        stddev_box = LabeledTextbox('standard deviation (σ):', self.stddev_changed, equation_regex)

        layout = QVBoxLayout()
        layout.addWidget(mean_box)
        layout.addWidget(stddev_box)

        
        # test = QLabel('bruhh')
        # test2 = QLabel('ok')
        # layout.addWidget(test)
        # layout.addWidget(test2)

        self.setLayout(layout)
    
    def mean_changed(self, text):
        print(f'mean text edited to: {text}')

    def stddev_changed(self, text):
        print(f'stddev text edited to: {text}')

if __name__ == '__main__': 
    app = QApplication(sys.argv)

    window = NormalCDF()
    window.show()

    app.exec()