# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

import traceback

from datetime import date, timedelta
from random import random, choice, randint

from colorama import init, Fore, Style

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Date, Float

from app.settings import APP_TEST_DATABASE_URL

DeclarativeBase = declarative_base()

class TableToExtract_WD(DeclarativeBase):
	__tablename__ = 'test_extract_wd_table'

	id 	      = Column(Integer, primary_key = True)
	name      = Column(String(64))
	lastname  = Column(String(64))
	age       = Column(Integer)
	amount    = Column(Float)
	datestamp = Column(Date)

class TableToExtract_WOD(DeclarativeBase):
	__tablename__ = 'test_extract_wod_table'

	id 	      = Column(Integer, primary_key = True)
	name      = Column(String(64))
	lastname  = Column(String(64))
	age       = Column(Integer)
	amount    = Column(Float)
	datestamp = Column(Date)

class TableToExtract_DC(DeclarativeBase):
	__tablename__ = 'test_extract_dc_table'

	id     = Column(Integer, primary_key = True)
	letter = Column(String(1))
	date   = Column(Date)

class TableToInsert(DeclarativeBase):
	__tablename__ = 'test_repo_table'

	id 	      = Column(Integer, primary_key = True)
	name      = Column(String(64))
	lastname  = Column(String(64))
	age       = Column(Integer)
	amount    = Column(Float)
	datestamp = Column(Date)

class TableToInsert_DC(DeclarativeBase):
	__tablename__ = 'test_repo_dc_table'
	id     = Column(Integer, primary_key = True)
	letter = Column(String(1))
	date   = Column(Date)
	freq   = Column(Integer)

class TableToUnittest(DeclarativeBase):
	__tablename__ = 'unittest_repo_table'

	id 	      = Column(Integer, primary_key = True)
	name      = Column(String(64))
	lastname  = Column(String(64))
	age       = Column(Integer)
	amount    = Column(Float)
	datestamp = Column(Date)

data = {'names': [ 'Jon', 'Arya', 'Daenerys', 'Khal', 'Gregor', 'Cersei', 'Tyrion', ],
		'lastname': [ 'Snow', 'Lannister', 'Targaryen', 'Bolton', 'Stark', 'Drogo', 'Baratheon', ],
		'age': [ randint(18, 40) for age in range(7) ],
		'date': [ date.today() +timedelta(days = day) for day in range(-3, 3) ], }

def _create_test_database(dim = 49, date_pop = -1):
	engine = create_engine(APP_TEST_DATABASE_URL)

	_Session = sessionmaker(engine)
	session = _Session()

	DeclarativeBase.metadata.create_all(engine)
	
	wodate = data['date'].pop(date_pop)

	wd_data = list()
	for i in range(dim):
		wd_data.append(TableToExtract_WD(
			name = choice(data['names']),
			lastname = choice(data['lastname']),
			age = choice(data['age']),
			amount = random() * 10,
			datestamp = choice(data['date'])))
		
	wod_data = list()
	for i in range(30):
		wod_data.append(TableToExtract_WOD(
			name = choice(data['names']),
			lastname = choice(data['lastname']),
			age = choice(data['age']),
			amount = random() * 10,
			datestamp = wodate))

	_letter = list('ABCDE')

	dc_data = list()
	for i in range(dim):
		dc_data.append(TableToExtract_DC(
			letter = choice(_letter),
			date = choice(data['date'])))

	session.add_all(wd_data); session.add_all(wod_data); session.add_all(dc_data)
	
	session.commit()
	session.close()

def create_test_database():
	init() # Init Colorama
	GREEN = Fore.GREEN; RED = Fore.RED; BRIGHT = Style.BRIGHT; RESET = Style.RESET_ALL
	print('\nTest dataset for VORT')
	print(f'Loading it... ', end = '')
	
	try:
		_create_test_database()
	except Exception as e:
		print(f'{RED}{BRIGHT}Error', '\n\n', e, '\n')
		traceback.print_exc()
	else:
		print(f'{GREEN}{BRIGHT}Done')
	finally:
		print(f'{RESET}', end = '')

if __name__ == '__main__':
	create_test_database()