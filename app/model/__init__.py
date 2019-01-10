# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ._config import APP_DATABASE_URL
from . import models

def connect_database():
	engine = create_engine(APP_DATABASE_URL)

	_Session = sessionmaker(engine)
	session = _Session()

	class _Table(object):
		def __init__(self, models = models):
			self.Process = models.Process
			self.ETL = models.ETL
			self.Connection = models.Connection
			self.Query = models.Query
			self.Binnacle = models.Binnacle

	class _DB(object):
		def __init__(self, engine = engine, session = session,
				table = _Table(), _createDB = models.DeclarativeBase.metadata.create_all):
			self.engine = engine
			self.session = session
			self.table = table
			self._createDB = _createDB
		
		def create_(self):
			return self._createDB(self.engine)

	return _DB()