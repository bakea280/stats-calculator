from common import *

class InverseNormal(QWidget):
    def __init__(self):
        super().__init__()

        self.defaults = {
            'mean': 0,
            'stddev': 1,
            'area': 0.5,
            'x': 0.0
        }

        self.data = self.defaults.copy()

        mean_box = LabeledTextbox('mean (μ):', self.mean_changed, str(self.defaults['mean']), EQUATION_REGEX)
        stddev_box = LabeledTextbox('standard deviation (σ):', self.stddev_changed, str(self.defaults['stddev']), EQUATION_REGEX)
        area_box = LabeledTextbox('area (0 to 1):', self.area_changed, str(self.defaults['area']), EQUATION_REGEX)

        self.graph = InvNormalGraph(self.data)
        self.x_label = QLabel()
        self.calculate_x()

        layout = QHBoxLayout()

        layoutL = QVBoxLayout()
        layoutL.addWidget(mean_box)
        layoutL.addWidget(stddev_box)
        layoutL.addWidget(area_box)
        layoutL.addWidget(self.x_label)
        layoutL.setAlignment(layoutL.alignment() | Qt.AlignmentFlag.AlignTop)

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
        clipped_area = np.clip(data_new['area'], 0, 1)
        data_new['x'] = norm.ppf(clipped_area, data_new['mean'], data_new['stddev'])

        self.set_x(data_new['x'])
        self.graph.update_graph(data_new)

class InvNormalGraph(QWidget):
    def __init__(self, data):
        super().__init__()

        self.graph = pg.PlotWidget()
        self.graph.setBackground(BACKGROUND_COLOR)
        self.viewbox = self.graph.getViewBox()

        self.main_pen = pg.mkPen(width=2)
        self.bounds_pen = pg.mkPen(width=2, color=(168,147,120))
        self.resolution = 100

        self.main_line = self.graph.plot(pen=self.main_pen)
        self.bounds_line = self.graph.plot(pen=self.bounds_pen, fillLevel=0, brush=(235,217,193,200))
        self.x_text = pg.TextItem(anchor=(0.5, 0.8), color=(0,0,0,255), ensureInBounds=True)
        self.graph.addItem(self.x_text)
        self.update_graph(data)

        layout = QVBoxLayout()
        layout.addWidget(self.graph)
        self.setLayout(layout)

    def update_graph(self, data):
        graph_start = data['mean'] - data['stddev']*3
        graph_end = data['mean'] + data['stddev']*3
        graph_length = graph_end - graph_start

        pdf = lambda x: norm.pdf(x, data['mean'], data['stddev'])

        # draw normal distribution curve
        normal_x = np.linspace(graph_start, graph_end, self.resolution)
        normal_y = pdf(normal_x)
        self.main_line.setData(normal_x, normal_y)

        bounds_end = np.clip(data['x'], graph_start, graph_end) if not np.isnan(data['x']) else graph_end
        bounds_length = bounds_end - graph_start
        bounds_resolution = max(int((bounds_length / graph_length) * self.resolution), 0)
        
        # draw curve from lower bound to upper bound
        bounds_x = np.linspace(graph_start, bounds_end, bounds_resolution*2)
        bounds_y = pdf(bounds_x)
        self.bounds_line.setData(bounds_x, bounds_y)

        graph_center = (graph_start + graph_end)/2

        # draw 'x = ...' text
        self.x_text.setText(f'x ≈ {data["x"]:.2f}')
        self.x_text.setPos(bounds_end, 0)
        if bounds_end > graph_center:
            self.x_text.setAnchor((1, 0.8))
        elif bounds_end < graph_center:
            self.x_text.setAnchor((0, 0.8))
        else:
            self.x_text.setAnchor((0.5, 0.8))

        graph_max = normal_y.max()
        graph_view_max = graph_max + graph_max * 0.01

        # set viewbox limits
        self.viewbox.setLimits(
            xMin = graph_start,
            xMax = graph_end,
            yMin = 0,
            yMax = graph_view_max,

            maxXRange = graph_length,
            minYRange = graph_view_max,
            maxYRange = graph_view_max
        )


if __name__ == '__main__': 
    app = QApplication(sys.argv)

    window = InverseNormal()
    window.show()

    app.exec()