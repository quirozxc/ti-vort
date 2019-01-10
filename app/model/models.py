# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from re import search

from sqlalchemy import Column, Sequence, Integer, String, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from ._config import DeclarativeBase


"""Process table"""
class Process(DeclarativeBase):
	__tablename__ = 'process'
	id = Column(Integer, Sequence('process_id_seq'), primary_key = True)
	name = Column(String(64), nullable = False)

	creation_timestamp = Column(DateTime, nullable = False)

	etls = relationship('ETL', order_by = 'ETL.priority', backref = backref('ETL.process'))

	def __repr__(self):
		return f'{self.name} <id = {self.id}>'

"""Connection table"""
class Connection(DeclarativeBase):
	__tablename__ = 'connection'
	id = Column(Integer, Sequence('connection_id_seq'), primary_key = True)
	db_url = Column(String(192), nullable = False)

	creation_timestamp = Column(DateTime, nullable = False)

	def __repr__(self):
		return f'{self.db_url} <id = {self.id}>'

"""Query table"""
class Query(DeclarativeBase):
	__tablename__ = 'query'
	id = Column(Integer, Sequence('query_id_seq'), primary_key = True)
	sql_query = Column(String(1024), nullable = False)

	creation_timestamp = Column(DateTime, nullable = False)

	def __repr__(self):
		return f'{self.sql_query} <id = {self.id}>'

"""ETL table"""
class ETL(DeclarativeBase):
	__tablename__ = 'etl'
	id = Column(Integer, Sequence('etl_id_seq'), primary_key = True)
	name = Column(String(64), nullable = False)
	description = Column(String(512))
	priority = Column(Integer, nullable = False)
	lastrun_date = Column(Date)

	process = Column(Integer, ForeignKey('process.id'))
	extract_connection = Column(Integer, ForeignKey('connection.id'))
	insert_connection = Column(Integer, ForeignKey('connection.id'))
	select_query = Column(Integer, ForeignKey('query.id'))
	update_query = Column(Integer, ForeignKey('query.id'))
	insert_query = Column(Integer, ForeignKey('query.id'))

	creation_timestamp = Column(DateTime, nullable = False)
	lastmod_timestamp = Column(DateTime)

	UniqueConstraint(process, priority)

	extract_from = relationship('Connection', foreign_keys = 'ETL.extract_connection',
							uselist = False, backref = backref('ETL.extract_connection'))
	insert_to = relationship('Connection', foreign_keys = 'ETL.insert_connection',
							uselist = False, backref = backref('ETL.insert_connection'))

	selecting = relationship('Query', foreign_keys = 'ETL.select_query',
							uselist = False, backref = backref('ETL.select_query'))
	updating = relationship('Query', foreign_keys = 'ETL.update_query',
							uselist = False, backref = backref('ETL.update_query'))
	inserting = relationship('Query', foreign_keys = 'ETL.insert_query',
							uselist = False, backref = backref('ETL.insert_query'))
	binnacle = relationship('Binnacle', order_by = 'Binnacle.execution_timestamp',
							backref = backref('Binnacle.etl'))
	def __repr__(self):
		return f'{self.name} <id = {self.id}>'

"""Binnacle table"""
class Binnacle(DeclarativeBase):
	__tablename__ = 'binnacle'
	id = Column(Integer, Sequence('binnacle_id_seq'), primary_key = True)
	execution_timestamp = Column(DateTime)
	processed_data_quantity = Column(Integer)

	etl = Column(Integer, ForeignKey('etl.id'))