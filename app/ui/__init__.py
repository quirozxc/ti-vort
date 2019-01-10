# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.image import imread

from ..settings import STATIC_DIR, DISPLAY_LAYOUTS

from .base import Ui_vort_mainWindow

class Vort_Ui(Ui_vort_mainWindow):
	def __init__(self):
		super().__init__()

	def _make_displayPlot(self):
		self.display_plot = FigureCanvas(
			Figure(figsize = (5.714285714, 4.142857143), dpi = 70))
		self.display_plot.setParent(self.display_groupBox)
		self.display_plot.setGeometry(QtCore.QRect(5, 5, 400, 290))
		self.display_plot.setObjectName('display_plot')

	def print(self, msg):
		self.vort_centralWidget_currentStatus_label.setText(msg)

def make_ui(argv = None):
	app = QApplication(argv)
	window = QMainWindow()
	window.setWindowIcon(QIcon(STATIC_DIR +'/favicon.png'))
	
	ui = Vort_Ui()
	ui.setupUi(window)

	ui._make_displayPlot()

	def _print_presentation(display = None):
		ax = display.figure.subplots()
		display.figure.tight_layout(rect = DISPLAY_LAYOUTS[0])

		image_file = open(STATIC_DIR +'/vort_mainDisplay.png', mode = 'rb')
		image = imread(image_file)

		ax.imshow(image)
		ax.set_title('')
		ax.axis('off')
	_print_presentation(display = ui.display_plot)

	return (app, window, ui)