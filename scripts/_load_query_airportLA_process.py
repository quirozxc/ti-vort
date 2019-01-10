# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

import traceback

from datetime import datetime

from colorama import init, Fore, Style

from app.model import connect_database
from app.settings import APP_TEST_DATABASE_URL

def _load_query_airportLA_process():
	dbo = connect_database()
	processes = list()
	processes.append(dbo.table.Process(
		name = 'Los Angeles Airport International - Process',
		creation_timestamp = datetime.now()))

	processes[0].etls.append(dbo.table.ETL(
		name = 'Los Angeles Airport International - ETL #1',
		description = 'Primer proceso ETL para demostración/test del aeropuerto (carrier - passenger)',
		priority = 1,
		creation_timestamp = datetime.now(),
		extract_from = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp =  datetime.now()),
		insert_to = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp = datetime.now()),
		selecting = dbo.table.Query(
			sql_query = "",
			creation_timestamp = datetime.now()),
		updating = dbo.table.Query(
			sql_query = '',
			creation_timestamp = datetime.now()),
		inserting = dbo.table.Query(
			sql_query = "INSERT INTO airport_la_passenger_carrier_table (report_period, "  \
						"arrival_departure, domestic_international, flight_type, passenger_count) " \
						"VALUES ('{ReportPeriod}', '{Arrival_Departure}', '{Domestic_International}', '{FlightType}', {Passenger_Count})",
			creation_timestamp = datetime.now())))

	processes[0].etls.append(dbo.table.ETL(
		name = 'Los Angeles Airport International - ETL #2',
		description = 'Segundo proceso ETL para demostración/test del aeropuerto (terminal - passenger)',
		priority = 2,
		creation_timestamp = datetime.now(),
		extract_from = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp =  datetime.now()),
		insert_to = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp = datetime.now()),
		selecting = dbo.table.Query(
			sql_query = "",
			creation_timestamp = datetime.now()),
		updating = dbo.table.Query(
			sql_query = '',
			creation_timestamp = datetime.now()),
		inserting = dbo.table.Query(
			sql_query = "INSERT INTO airport_la_passenger_terminal_table (report_period, "  \
						"terminal, arrival_departure, domestic_international, passenger_count) " \
						"VALUES ('{ReportPeriod}', '{Terminal}', '{Arrival_Departure}', '{Domestic_International}', {Passenger_Count})",
			creation_timestamp = datetime.now())))

	processes[0].etls.append(dbo.table.ETL(
		name = 'Los Angeles Airport International - ETL #3',
		description = 'Tercer proceso ETL para demostración/test del aeropuerto (terminal - passenger)',
		priority = 3,
		creation_timestamp = datetime.now(),
		extract_from = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp =  datetime.now()),
		insert_to = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp = datetime.now()),
		selecting = dbo.table.Query(
			sql_query = "SELECT report_period, arrival_departure, domestic_international, COUNT(*), SUM(passenger_count) " \
						"FROM airport_la_passenger_terminal_table " \
						"WHERE report_period = '{fecha}' " \
						"GROUP BY (report_period, arrival_departure, domestic_international)",
			creation_timestamp = datetime.now()),
		updating = dbo.table.Query(
			sql_query = '',
			creation_timestamp = datetime.now()),
		inserting = dbo.table.Query(
			sql_query = "INSERT INTO airport_repo_passenger_terminal_count_table (date_calendar, " \
						"arrival_departure, domestic_international, counting, passenger_count) " \
						"VALUES ('{report_period}', '{arrival_departure}', '{domestic_international}', '{count}', '{sum}')",
			creation_timestamp = datetime.now())))

	processes[0].etls.append(dbo.table.ETL(
		name = 'Los Angeles Airport International - ETL #4',
		description = 'Cuarto proceso ETL para demostración/test del aeropuerto (terminal - passenger)',
		priority = 4,
		creation_timestamp = datetime.now(),
		extract_from = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp =  datetime.now()),
		insert_to = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp = datetime.now()),
		selecting = dbo.table.Query(
			sql_query = "SELECT report_period, terminal, domestic_international, SUM(passenger_count) " \
						"FROM airport_la_passenger_terminal_table " \
						"WHERE report_period = '{fecha}' AND domestic_international = 'International' " \
						"GROUP BY (report_period, terminal, domestic_international)",
			creation_timestamp = datetime.now()),
		updating = dbo.table.Query(
			sql_query = '',
			creation_timestamp = datetime.now()),
		inserting = dbo.table.Query(
			sql_query = "INSERT INTO airport_repo_passenger_terminal_sum_table (date_calendar, terminal, " \
						"domestic_international, passenger_count) " \
						"VALUES ('{report_period}', '{terminal}', '{domestic_international}', '{sum}')",
			creation_timestamp = datetime.now())))

	processes[0].etls.append(dbo.table.ETL(
		name = 'Los Angeles Airport International - ETL #5',
		description = 'Quinto proceso ETL para demostración/test del aeropuerto (carrier - passenger)',
		priority = 5,
		creation_timestamp = datetime.now(),
		extract_from = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp =  datetime.now()),
		insert_to = dbo.table.Connection(
			db_url = APP_TEST_DATABASE_URL,
			creation_timestamp = datetime.now()),
		selecting = dbo.table.Query(
			sql_query = "SELECT report_period, flight_type, SUM(passenger_count) " \
						"FROM airport_la_passenger_carrier_table " \
						"WHERE report_period = '{fecha}' " \
						"GROUP BY (report_period, flight_type)",
			creation_timestamp = datetime.now()),
		updating = dbo.table.Query(
			sql_query = '',
			creation_timestamp = datetime.now()),
		inserting = dbo.table.Query(
			sql_query = "INSERT INTO airport_repo_passenger_carrier_sum_table (date_calendar, " \
						"flight_type, passenger_count) VALUES ('{report_period}', '{flight_type}', '{sum}')",
			creation_timestamp = datetime.now())))

	dbo.session.add_all(processes)
	dbo.session.commit()
	dbo.session.close()

def load_query_airportLA_process():
	init() # Init Colorama
	GREEN = Fore.GREEN; RED = Fore.RED; BRIGHT = Style.BRIGHT; RESET = Style.RESET_ALL
	print('\nTest Airport ETL for VORT')
	print(f'Loading it... ', end = '')
	
	try:
		_load_query_airportLA_process()
	except Exception as e:
		print(f'{RED}{BRIGHT}Error', '\n\n', e, '\n')
		traceback.print_exc()
	else:
		print(f'{GREEN}{BRIGHT}Done')
	finally:
		print(f'{RESET}', end = '')

if __name__ == '__main__':
	load_query_airportLA_process()