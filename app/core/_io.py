# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

import traceback

from re import search
from random import choice

from colorama import init, Fore, Style
init() # Init Colorama
RED = Fore.RED; BRIGHT = Style.BRIGHT; RESET = Style.RESET_ALL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pandas import DataFrame

from petl.io import fromxlsx, fromxls, fromcsv, fromtsv, fromjson, fromdicts, fromdataframe
from petl.io import toxlsx, toxls, tocsv, totsv, tojson

def connect_database(connection):
	try:
		engine = create_engine(connection)

		_Session = sessionmaker(engine)
		session = _Session()

		class _DB(object):
			def __init__(self, engine = engine, session = session):
				self.engine = engine
				self.session = session
		return _DB()
	except Exception as e:

		# print(f'{RED}{BRIGHT}Error', '\n\n', e, '\n')
		# traceback.print_exc()
		# print(f'{RESET}', end = '')

		return e

def execute_query(dbo, sql_query, df = DataFrame()):
	# DATA UPDATING & INSERTION
	if not df.empty:
		try:
			_tb = fromdataframe(df)
			_rows = _tb.dicts()
			for row in _rows:
				dbo.session.execute(sql_query.format(**row))
			dbo.session.commit()
		except Exception as e:
			dbo.session.rollback()

			print('\r{0}'.format(choice(['+·+', '·+·'])), end = '')

			# print(f'{RED}{BRIGHT}Error', '\n\n', e, '\n')
			# traceback.print_exc()
			# print(f'{RESET}', end = '')

			return e
	# DATA SELECTION
	else:
		try:
			_result = dbo.session.execute(sql_query)
			_tb = fromdicts(_result.fetchall())
			_df = _tb.todataframe()
			if not _df.empty:
				return _df
			raise NotImplementedError
		except Exception as e:

			print('\r{0}'.format(choice(['+·+', '·+·'])), end = '')

			# print(f'{RED}{BRIGHT}Error', '\n\n', e, '\n')
			# traceback.print_exc()
			# print(f'{RESET}', end = '')

			return e

def import_file(fileName):
	try:
		from_ = { 'xlsx': fromxlsx, 'xls': fromxls, 'csv': fromcsv, 'tsv': fromtsv, 'json': fromjson, }
		_ext = search(r'\w+$', fileName).group()
		_fd = from_.get(_ext)(fileName).todataframe()
		if len(_fd) < 1:
			raise NotImplementedError
		return _fd
	except Exception as e:

		# print(f'{RED}{BRIGHT}Error', '\n\n', e, '\n')
		# traceback.print_exc()
		# print(f'{RESET}', end = '')

		return e

def export_file(fileName, df):
	try:
		to_ = { 'xlsx': toxlsx, 'xls': toxls, 'csv': tocsv, 'tsv': totsv, 'json': tojson, }
		_ext = search(r'\w+$', fileName).group()
		if _ext == 'json':
			to_.get(_ext)(fromdataframe(df), fileName, default = str)
		elif _ext == 'xls':
			to_.get(_ext)(fromdataframe(df), fileName, sheet = 1)
		else: to_.get(_ext)(fromdataframe(df), fileName)
	except Exception as e:

		# print(f'{RED}{BRIGHT}Error', '\n\n', e, '\n')
		# traceback.print_exc()
		# print(f'{RESET}', end = '')

		return e