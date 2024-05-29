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

EQUATION_REGEX = '[0-9\Q.+-*/x^(), \E]*' 

class LabeledTextbox(QWidget):
    def __init__(self, label_text, call_on_edit=None, placeholder_text=None, regex_filter=None):
        super().__init__()

        self.label = QLabel(label_text)
        self.textbox = QLineEdit()
        self.label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

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