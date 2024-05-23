import pyqtgraph as pg
import numpy as np
from scipy.stats import norm

mean, stddev = 0, 1
resolution = 100

x = np.linspace(mean - stddev*3, mean + stddev*3, resolution)
pg.plot(x, norm.pdf(x))

pg.exec()