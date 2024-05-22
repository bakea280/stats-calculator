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

import numpy as np
from scipy.stats import norm

class LabeledTextbox(QWidget):
    def __init__(self, label_text, call_on_edit=None, placeholder_text=None, regex_filter=None):
        super().__init__()

        self.label = QLabel(label_text)
        self.textbox = QLineEdit()

        if placeholder_text:
            self.textbox.setPlaceholderText(placeholder_text)

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

class NormalCDF(QWidget):
    def __init__(self):
        super().__init__()

        self.default_mean = 0
        self.default_stddev = 1
        self.default_lowerbound = -1 * 10**10
        self.default_upperbound = 1 * 10**10

        self.mean = self.default_mean
        self.stddev = self.default_stddev
        self.lowerbound = self.default_lowerbound
        self.upperbound = self.default_upperbound
        self.p = 1.0

        equation_regex = '[0-9\Q.+-*/x^(), \E]*' 

        mean_box = LabeledTextbox('mean (μ):', self.mean_changed, str(self.mean), equation_regex)
        stddev_box = LabeledTextbox('standard deviation (σ):', self.stddev_changed, str(self.stddev), equation_regex)
        lowerbound_box = LabeledTextbox('lower bound:', self.lowerbound_changed, '-∞', equation_regex)
        upperbound_box = LabeledTextbox('upper bound:', self.upperbound_changed, '∞', equation_regex)
        self.p_label = QLabel(f'p = {self.p}')

        layout = QVBoxLayout()
        layout.addWidget(mean_box)
        layout.addWidget(stddev_box)
        layout.addWidget(lowerbound_box)
        layout.addWidget(upperbound_box)
        layout.addWidget(self.p_label)

        self.setLayout(layout)
    
    def mean_changed(self, text):
        if not text:
            self.mean = self.default_mean
        else:
            self.mean = text
        
        self.calculate_p(self.mean, self.stddev, self.lowerbound, self.upperbound)

    def stddev_changed(self, text):
        if not text:
            self.stddev = self.default_stddev
        else:
            self.stddev = text
        
        self.calculate_p(self.mean, self.stddev, self.lowerbound, self.upperbound)

    def lowerbound_changed(self, text):
        if not text:
            self.lowerbound = self.default_lowerbound
        else:
            self.lowerbound = text

        self.calculate_p(self.mean, self.stddev, self.lowerbound, self.upperbound)
    
    def upperbound_changed(self, text):
        if not text:
            self.upperbound = self.default_upperbound
        else:
            self.upperbound = text
    
        self.calculate_p(self.mean, self.stddev, self.lowerbound, self.upperbound)
    
    def set_p(self, value):
        self.p = value
        self.p_label.setText(f'p = {value}')

    def calculate_p(self, mean, stddev, lower, upper):
        try:
            # fail if invalid input
            mean = float(mean)
            stddev = float(stddev)
            lower = float(lower)
            upper = float(upper)

            lower_cdf = norm.cdf(lower, mean, stddev)
            upper_cdf = norm.cdf(upper, mean, stddev)
            
            self.set_p(upper_cdf - lower_cdf)
        except Exception as e:
            print('ERROR IN calculate_p', type(e), e)
            self.set_p('?')

if __name__ == '__main__': 
    app = QApplication(sys.argv)

    window = NormalCDF()
    window.show()

    app.exec()