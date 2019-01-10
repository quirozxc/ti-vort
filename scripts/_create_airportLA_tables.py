# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

import traceback

from colorama import init, Fore, Style

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Date, Float

from app.settings import APP_TEST_DATABASE_URL

DeclarativeBase = declarative_base()

class AirportLAPassengerCarrier(DeclarativeBase):
	__tablename__ = 'airport_la_passenger_carrier_table'

	id						= Column(Integer, primary_key = True)
	report_period  			= Column(Date)
	arrival_departure       = Column(String(64))
	domestic_international  = Column(String(64))
	flight_type 				= Column(String(64))
	passenger_count 		= Column(Integer)

class AirportLAPassengerTerminal(DeclarativeBase):
	__tablename__ = 'airport_la_passenger_terminal_table'

	id 	      				= Column(Integer, primary_key = True)
	report_period  			= Column(Date)
	terminal       			= Column(String(64))
	arrival_departure    	= Column(String(64))
	domestic_international 	= Column(String(64))
	passenger_count 		= Column(Integer)

class AirportRepoPassengerTerminalCount(DeclarativeBase):
	__tablename__ = 'airport_repo_passenger_terminal_count_table'

	id 						= Column(Integer, primary_key = True)
	date_calendar 			= Column(Date)
	arrival_departure 		= Column(String(64))
	domestic_international  = Column(String(64))
	counting 				= Column(Integer)
	passenger_count 		= Column(Integer)

class AirportRepoPassengerTerminalSum(DeclarativeBase):
	__tablename__ = 'airport_repo_passenger_terminal_sum_table'

	id 						= Column(Integer, primary_key = True)
	date_calendar 			= Column(Date)
	terminal 				= Column(String(64))
	domestic_international  = Column(String(64))
	passenger_count 		= Column(Integer)

class AirportRepoPassangerCarrierSum(DeclarativeBase):
	__tablename__ = 'airport_repo_passenger_carrier_sum_table'

	id = Column(Integer, primary_key = True)
	date_calendar = Column(Date)
	flight_type = Column(String(64))
	passenger_count = Column(String(64))

def _create_airportLA_data(dim = 49, date_pop = -1):
	engine = create_engine(APP_TEST_DATABASE_URL)

	_Session = sessionmaker(engine)
	session = _Session()

	DeclarativeBase.metadata.create_all(engine)
	
	session.commit()
	session.close()

def create_airportLA_data():
	init() # Init Colorama
	GREEN = Fore.GREEN; RED = Fore.RED; BRIGHT = Style.BRIGHT; RESET = Style.RESET_ALL
	print('\nCreate tables to Airport LA dataset for VORT')
	print(f'Loading it... ', end = '')
	
	try:
		_create_airportLA_data()
	except Exception as e:
		print(f'{RED}{BRIGHT}Error', '\n\n', e, '\n')
		traceback.print_exc()
	else:
		print(f'{GREEN}{BRIGHT}Done')
	finally:
		print(f'{RESET}', end = '')

if __name__ == '__main__':
	create_airportLA_data()