from common import *

class InverseNormal(QWidget):
    def __init__(self):
        super().__init__()

        self.defaults = {
            'mean': 0,
            'stddev': 1,
            'area': 0.5,
            'x': 0
        }

        self.data = self.defaults.copy()

        mean_box = LabeledTextbox('mean (μ):', self.mean_changed, str(self.defaults['mean']), EQUATION_REGEX)
        stddev_box = LabeledTextbox('standard deviation (σ):', self.stddev_changed, str(self.defaults['stddev']), EQUATION_REGEX)
        area_box = LabeledTextbox('area:', self.area_changed, str(self.defaults['area']), EQUATION_REGEX)

        # self.graph = InvNormalGraph(self.data)
        self.x_label = QLabel()
        self.calculate_x()

        layout = QHBoxLayout()

        layoutL = QVBoxLayout()
        layoutL.addWidget(mean_box)
        layoutL.addWidget(stddev_box)
        layoutL.addWidget(area_box)
        layoutL.addWidget(self.x_label)

        layoutR = QVBoxLayout()
        # layoutR.addWidget(self.graph)

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
        self.calculate_x()
    def stddev_changed(self, text):
        self.check_input('stddev', text)
        self.calculate_x()
    def area_changed(self, text):
        self.check_input('area', text)
        self.calculate_x()
    
    def set_x(self, value):
        self.data['x'] = value
        self.x_label.setText(f'x = {value}')
    
    def calculate_x(self):
        invalid_inputs = []
        data_new = {}
        
        for key, value in self.data.items():
            if key == 'x':
                continue

            try:
                data_new[key] = float(value)
            except:
                invalid_inputs.append(key)
        
        if invalid_inputs:
            self.set_x('?')
            return
        
        # Calculate x
        data_new['x'] = norm.ppf(data_new['area'], data_new['mean'], data_new['stddev'])

        self.set_x(data_new['x'])
        # self.graph.update_graph(data_new)

class InvNormalGraph(QWidget):
    ...

if __name__ == '__main__': 
    app = QApplication(sys.argv)

    window = InverseNormal()
    window.show()

    app.exec()