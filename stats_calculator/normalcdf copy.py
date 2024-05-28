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
import pyqtgraph as pg

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

class NormalGraph(QWidget):
    def __init__(self, data):
        super().__init__()
        
        self.graph = pg.PlotWidget()

        self.normal_graph = pg.PlotWidget()
        self.pen = pg.mkPen(width=5)
        mean, stddev = 0, 1
        self.resolution = 100
        # x = np.linspace(mean - stddev*3, mean + stddev*3, self.resolution)
        # self.normal_graph.plot(x, norm.pdf(x), pen=self.pen)
        self.update_graph(data)

        layout = QVBoxLayout()
        # layout.addWidget(self.normal_graph)
        layout.addWidget(self.graph)
        self.setLayout(layout)

    def update_graph(self, data):
        x = np.linspace(data.mean - data.stddev*3, data.mean + data.stddev*3, self.resolution)
        self.graph.plot(x, norm.pdf(x), pen=self.pen)

class NormalCDF(QWidget):
    def __init__(self):
        super().__init__()

        self.defaults = {
            'mean': 0,
            'stddev': 1,
            'lowerbound': -1 * 10**10,
            'upperbound': 1 * 10**10
        }

        self.data = self.defaults
        
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

        self.graph = NormalGraph(self)

        layout = QHBoxLayout()

        layoutL = QVBoxLayout()
        layoutL.addWidget(mean_box)
        layoutL.addWidget(stddev_box)
        layoutL.addWidget(lowerbound_box)
        layoutL.addWidget(upperbound_box)
        layoutL.addWidget(self.p_label)

        layoutR = QVBoxLayout()
        layoutR.addWidget(self.graph)

        layout.addLayout(layoutL)
        layout.addLayout(layoutR)
        self.setLayout(layout)
    
    def mean_changed(self, text):
        if not text:
            self.mean = self.default_mean
        else:
            self.mean = text
        
        self.calculate_p()

    def stddev_changed(self, text):
        if not text:
            self.stddev = self.default_stddev
        else:
            self.stddev = text
        
        self.calculate_p()

    def lowerbound_changed(self, text):
        if not text:
            self.lowerbound = self.default_lowerbound
        else:
            self.lowerbound = text

        self.calculate_p()
    
    def upperbound_changed(self, text):
        if not text:
            self.upperbound = self.default_upperbound
        else:
            self.upperbound = text
    
        self.calculate_p()
    

    def set_p(self, value):
        self.p = value
        self.p_label.setText(f'p = {value}')

    def calculate_p(self):
        # try:
            # fail if invalid input
        mean = float(self.mean)
        stddev = float(self.stddev)
        lower = float(self.lowerbound)
        upper = float(self.upperbound)

        lower_cdf = norm.cdf(lower, mean, stddev)
        upper_cdf = norm.cdf(upper, mean, stddev)
        
        self.set_p(upper_cdf - lower_cdf)
        self.graph.update_graph(self)
        # except Exception as e:
        #     print('ERROR IN calculate_p', type(e), e)
        #     self.set_p('?')

if __name__ == '__main__': 
    app = QApplication(sys.argv)

    window = NormalCDF()
    window.show()

    app.exec()