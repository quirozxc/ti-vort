# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

import traceback

from datetime import datetime

from colorama import init, Fore, Style

from app.model import connect_database
from app.settings import APP_TEST_DATABASE_URL

def _load_etl_test():
	dbo = connect_database()
	processes = list()
	processes.append(dbo.table.Process(
		name = 'Quiroz\'s First Process - Test',
		creation_timestamp = datetime.now()))

	processes[0].etls.append(dbo.table.ETL(
		name = 'Quiroz\'s First ETL - Test',
		description = 'Primer proceso ETL para demostración/test inicial',
		priority = 1,
		creation_timestamp = datetime.now(),
		extract_from = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp =  datetime.now()),
		insert_to = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp = datetime.now()),
		selecting = dbo.table.Query(
			sql_query = "SELECT name, lastname, age, amount, datestamp " \
						"FROM test_extract_wd_table WHERE datestamp = '{fecha}'",
			creation_timestamp = datetime.now()),
		updating = dbo.table.Query(
			sql_query = '',
			creation_timestamp = datetime.now()),
		inserting = dbo.table.Query(
			sql_query = "INSERT INTO test_repo_table (name, lastname, age, amount, datestamp) " \
						"VALUES ('{name}', '{lastname}', {age}, {amount}, '{datestamp}')",
			creation_timestamp = datetime.now())))

	processes[0].etls.append(dbo.table.ETL(
		name = 'Quiroz\'s Second ETL - Test',
		description = 'Segundo proceso ETL para demostración/test inicial',
		priority = 2,
		creation_timestamp = datetime.now(),
		extract_from = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp =  datetime.now()),
		insert_to = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp = datetime.now()),
		selecting = dbo.table.Query(
			sql_query = "SELECT letter, date, COUNT(*) FROM test_extract_dc_table " \
						"WHERE date = '{fecha}' GROUP BY (letter, date)",
			creation_timestamp = datetime.now()),
		updating = dbo.table.Query(
			sql_query = '',
			creation_timestamp = datetime.now()),
		inserting = dbo.table.Query(
			sql_query = "INSERT INTO test_repo_dc_table (letter, date, freq) " \
						"VALUES ('{letter}', '{date}', {count})",
			creation_timestamp = datetime.now())))

	processes.append(dbo.table.Process(
		name = 'Quiroz\'s Second Process - Test',
		creation_timestamp = datetime.now()))

	processes[1].etls.append(dbo.table.ETL(
		name = 'Quiroz\'s Third ETL - Test',
		description = 'Tercer proceso ETL para demostración/test inicial con archivos',
		priority = 1,
		creation_timestamp = datetime.now(),
		extract_from = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp =  datetime.now()),
		insert_to = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp = datetime.now()),
		selecting = dbo.table.Query(
			sql_query = "SELECT name, lastname, age, amount, datestamp " \
						"FROM test_extract_wd_table",
			creation_timestamp = datetime.now()),
		updating = dbo.table.Query(
			sql_query = '',
			creation_timestamp = datetime.now()),
		inserting = dbo.table.Query(
			sql_query = '',
			creation_timestamp = datetime.now())))

	dbo.session.add_all(processes)
	dbo.session.commit()
	dbo.session.close()

def load_etl_test():
	init() # Init Colorama
	GREEN = Fore.GREEN; RED = Fore.RED; BRIGHT = Style.BRIGHT; RESET = Style.RESET_ALL
	print('\nTest ETL process for VORT')
	print(f'Loading it... ', end = '')
	
	try:
		_load_etl_test()
	except Exception as e:
		print(f'{RED}{BRIGHT}Error', '\n\n', e, '\n')
		traceback.print_exc()
	else:
		print(f'{GREEN}{BRIGHT}Done')
	finally:
		print(f'{RESET}', end = '')

if __name__ == '__main__':
	load_etl_test()