from common import *
from normalcdf import NormalCDF
from inversenormal import InverseNormal

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Statistics Calculator")
        icon = QIcon('resources/icon.svg')
        self.setWindowIcon(icon)
        self.setMinimumSize(QSize(480, 270))

        tabs = QTabWidget()

        tabs.addTab(NormalCDF(), 'NormalCDF')
        tabs.addTab(InverseNormal(), 'InverseNormal')

        self.setCentralWidget(tabs)


app = QApplication(sys.argv)

with open('resources/styles.qss') as f:
    stylesheet = f.read()
app.setStyleSheet(stylesheet)

window = MainWindow()
window.show()

app.exec()