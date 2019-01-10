# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from unittest import TestCase
from os import path

from matplotlib.figure import Figure

from ..core import _DataFrame
from ..core._io import import_file
from ..core.mining import analyze_regression, analyze_classification, analyze_clustering

from ..settings import COLORS_MAP, COLORS

FILE_DIR = path.dirname(path.abspath(__file__)) +'/_files'
DATA = import_file(FILE_DIR +'/_base.json')

df = _DataFrame(); df.append(DATA)
fig = Figure(); ax = fig.subplots()

class MiningTestCase(TestCase):
	def test_analyze_regression(self):
		_ = analyze_regression(
			df.last().get('age'),
			df.last().get('amount'),
			ax,
			COLORS.get('Naranja'),
			COLORS.get('Marrón'),
			metrics = False)
		self.assertEquals(_, None)

	def test_analyze_classification(self):
		_ = analyze_classification(
			df.last().get('age'),
			df.last().get('amount'),
			ax,
			COLORS_MAP.get('Verano'),
			COLORS.get('Naranja'),
			COLORS.get('Marrón'),
			10,
			metrics = False)
		self.assertEquals(_, None)

	def test_analyze_clustering(self):
		_ = analyze_clustering(
			df.last().get('age'),
			df.last().get('amount'),
			ax,
			5,
			COLORS_MAP.get('Accent'),
			COLORS_MAP.get('Verano'),
			metrics = False)
		self.assertEquals(_, None)