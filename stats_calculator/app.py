from common import *
from normalcdf import NormalCDF
from inversenormal import InverseNormal

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Statistics Calculator")
        self.setMinimumSize(QSize(480, 270))

        tabs = QTabWidget()

        
        tabs.addTab(NormalCDF(), 'NormalCDF')
        tabs.addTab(InverseNormal(), 'InverseNormal')

        self.setCentralWidget(tabs)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()