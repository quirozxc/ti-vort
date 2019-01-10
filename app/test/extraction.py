# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from unittest import TestCase
from os import path

from ..core.extraction import execute_extraction
from ..core._io import import_file

from ..settings import APP_TEST_DATABASE_URL

class Any():
	pass

FILE_DIR = path.dirname(path.abspath(__file__)) +'/_files'

class ExtractionTestCase(TestCase):
	def test_extrac_from_database(self):
		connection = Any(); df = list()
		connection.db_url = APP_TEST_DATABASE_URL
		_ = execute_extraction(
			connection,
			'SELECT name, lastname, age, amount, datestamp FROM test_extract_wd_table',
			df)
		self.assertEquals(len(df[0]), 49)

	def test_extract_from_xlsx_file(self):
		_ = import_file(FILE_DIR +'/_xlsx.xlsx')
		self.assertEquals(type(_).__name__, 'DataFrame')

	def test_extract_from_xls_file(self):
		_ = import_file(FILE_DIR +'/_xls.xls')
		self.assertEquals(type(_).__name__, 'DataFrame')

	def test_extract_from_csv_file(self):
		_ = import_file(FILE_DIR +'/_csv.csv')
		self.assertEquals(type(_).__name__, 'DataFrame')

	def test_extract_from_tsv_file(self):
		_ = import_file(FILE_DIR +'/_tsv.tsv')
		self.assertEquals(type(_).__name__, 'DataFrame')

	def test_extract_from_json_file(self):
		_ = import_file(FILE_DIR +'/_json.json')
		self.assertEquals(type(_).__name__, 'DataFrame')