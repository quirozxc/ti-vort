# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from unittest import TestCase
from os import path

from ..core import _DataFrame
from ..core.integration import execute_integration
from ..core._io import import_file, export_file

from ..settings import APP_TEST_DATABASE_URL

class Any():
	pass

FILE_DIR = path.dirname(path.abspath(__file__)) +'/_files'
DATA = import_file(FILE_DIR +'/_base.json')

class IntegrationTestCase(TestCase):
	def test_insert_to_database(self):
		connection = Any(); connection.db_url = APP_TEST_DATABASE_URL
		df = _DataFrame(); df.append(DATA)
		_ = execute_integration(
			connection,
			'',
			'INSERT INTO unittest_repo_table (name, lastname, age, amount, datestamp)' \
				"VALUES ('{name}', '{lastname}', {age}, {amount}, '{datestamp}')",
			df)
		self.assertEqual(_, None)

	def test_insert_to_xlsx_file(self):
		_ = export_file(FILE_DIR +'/_xlsx.xlsx', DATA)
		self.assertEqual(_, None)

	def test_insert_to_xls_file(self):
		_ = export_file(FILE_DIR +'/_xls.xls', DATA)
		#self.assertEqual(_, None)

	def test_insert_to_csv_file(self):
		_ = export_file(FILE_DIR +'/_csv.csv', DATA)
		self.assertEqual(_, None)

	def test_insert_to_tsv_file(self):
		_ = export_file(FILE_DIR +'/_tsv.tsv', DATA)
		self.assertEqual(_, None)

	def test_insert_to_json_file(self):
		_ = export_file(FILE_DIR +'/_json.json', DATA)
		self.assertEqual(_, None)
