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
pg.setConfigOptions(antialias=True)

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
        self.graph.setBackground('w')

        self.main_pen = pg.mkPen(width=2)
        self.bounds_pen = pg.mkPen(width=2, color=(168,147,120))
        self.resolution = 100

        self.main_line = self.graph.plot(pen=self.main_pen)
        self.bounds_line = self.graph.plot(pen=self.bounds_pen, fillLevel=0, brush=(235,217,193,200))
        self.area_text = pg.TextItem(anchor=(0.5, 1), color=(0,0,0,255))
        self.graph.addItem(self.area_text)
        self.update_graph(data)

        layout = QVBoxLayout()
        layout.addWidget(self.graph)
        self.setLayout(layout)

    def update_graph(self, data):
        graph_start = data['mean'] - data['stddev']*3
        graph_end = data['mean'] + data['stddev']*3
        graph_length = graph_end - graph_start

        # draw normal distribution curve
        normal_x = np.linspace(graph_start, graph_end, self.resolution)
        self.main_line.setData(normal_x, norm.pdf(normal_x, data['mean'], data['stddev']))

        bounds_start = max(data['lowerbound'], graph_start)
        bounds_end = min(data['upperbound'], graph_end)
        bounds_length = bounds_end - bounds_start
        bounds_resolution = int((bounds_length / graph_length) * self.resolution)
        
        # draw curve from lower bound to upper bound
        bounds_x = np.linspace(bounds_start, bounds_end, bounds_resolution*2)
        self.bounds_line.setData(bounds_x, norm.pdf(bounds_x, data['mean'], data['stddev']))

        if not 'p' in data.keys():
            print(data.keys())
            return
        
        bounds_center = (bounds_start + bounds_end)/2

        self.area_text.setText(f'A = {data["p"]:.2}')
        self.area_text.setPos(bounds_center, norm.pdf(bounds_center, data['mean'], data['stddev'])/2)

        

class NormalCDF(QWidget):
    def __init__(self):
        super().__init__()

        self.defaults = {
            'mean': 0,
            'stddev': 1,
            'lowerbound': -1 * 10**10,
            'upperbound': 1 * 10**10
        }

        self.data = self.defaults.copy()
        # self.data['p'] = 1.0

        equation_regex = '[0-9\Q.+-*/x^(), \E]*' 

        mean_box = LabeledTextbox('mean (μ):', self.mean_changed, str(self.defaults['mean']), equation_regex)
        stddev_box = LabeledTextbox('standard deviation (σ):', self.stddev_changed, str(self.defaults['stddev']), equation_regex)
        lowerbound_box = LabeledTextbox('lower bound:', self.lowerbound_changed, '-∞', equation_regex)
        upperbound_box = LabeledTextbox('upper bound:', self.upperbound_changed, '∞', equation_regex)

        self.graph = NormalGraph(self.data)
        self.p_label = QLabel()
        self.calculate_p()

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

    def check_input(self, key, text):
        if text == '':
            self.data[key] = self.defaults[key]
        else:
            self.data[key] = text
    
    def mean_changed(self, text):
        self.check_input('mean', text)
        self.calculate_p()
    def stddev_changed(self, text):
        self.check_input('stddev', text)
        self.calculate_p()
    def lowerbound_changed(self, text):
        self.check_input('lowerbound', text)
        self.calculate_p()
    def upperbound_changed(self, text):
        self.check_input('upperbound', text)
        self.calculate_p()

    def set_p(self, value):
        self.data['p'] = value
        self.p_label.setText(f'p = {value}')

    def calculate_p(self):
        invalid_inputs = []
        data_new = {} # data as floats
        for key, value in self.data.items():
            if key == 'p':
                continue

            try:
                data_new[key] = float(value)
            except:
                invalid_inputs.append(key)

        if invalid_inputs:
            print('these inputs are invalid: ' + ', '.join(invalid_inputs))
            return

        lower_cdf = norm.cdf(data_new['lowerbound'], data_new['mean'], data_new['stddev'])
        upper_cdf = norm.cdf(data_new['upperbound'], data_new['mean'], data_new['stddev'])
        data_new['p'] = upper_cdf - lower_cdf
        
        self.set_p(data_new['p'])
        self.graph.update_graph(data_new)

if __name__ == '__main__': 
    app = QApplication(sys.argv)

    window = NormalCDF()
    window.show()

    app.exec()