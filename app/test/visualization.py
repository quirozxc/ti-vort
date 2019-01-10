# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from unittest import TestCase
from os import path

from matplotlib.figure import Figure

from ..core import _DataFrame
from ..core._io import import_file
from ..core.visualization import draw_figure

FILE_DIR = path.dirname(path.abspath(__file__)) +'/_files'
DATA = import_file(FILE_DIR +'/_base.json')

class VisualizationTestCase(TestCase):
	def test_build_figure(self):
		fig = Figure(); ax = fig.subplots()
		df = _DataFrame(); df.append(DATA)
		_ = draw_figure(df, ax,
			kind 	= 'Área',
			color 	= 'Naranjas',
			alpha 	= 5 / 10,
			stacked = True,
			point 	= False,
			grid 	= True,
			legend  = True)
		self.assertEquals(_, None)