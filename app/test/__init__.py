# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

import unittest
from unittest import TestSuite, TextTestRunner

from .extraction import ExtractionTestCase
from .transformation import TransformationTestCase
from .integration import IntegrationTestCase
from .visualization import VisualizationTestCase
from .mining import MiningTestCase

cases = [ ExtractionTestCase,
		  TransformationTestCase,
		  IntegrationTestCase,
		  VisualizationTestCase,
		  MiningTestCase, ]

def test_runner():
	print()
	for case in cases:
		suite = TestSuite()
		suite.addTest(
			unittest.defaultTestLoader
			.loadTestsFromTestCase(case))
		TextTestRunner(verbosity = 2).run(suite)
		if not case.__name__ == 'MiningTestCase':
			print()
			print('######################################################################',
				end = '\n\n')