# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from re import search
from datetime import date, datetime, timedelta

from ._io import connect_database, execute_query

def execute_etl(etl, lastrun_date):
	_btime = datetime.now()
	_df, _s, _u, _i, _pdq =  None, None, 'Sin Información', 'Sin Información', 0
	_extract_dbo = connect_database(etl.extract_from.db_url)

	if type(_extract_dbo).__name__ == '_DB':
		_f = search(r'{fecha}', etl.selecting.sql_query)
		if not _f: lastrun_date = date.today() -timedelta(days = 1)

		for day in range((date.today() -lastrun_date).days):
			_df = execute_query(_extract_dbo,
				etl.selecting.sql_query.format(fecha = lastrun_date +timedelta(days = day)))
			if type(_df).__name__ == 'DataFrame':
				_insert_dbo = connect_database(etl.insert_to.db_url)
				if type(_insert_dbo).__name__ == '_DB':
					if etl.updating.sql_query:
						_u = execute_query(_insert_dbo, etl.updating.sql_query, _df)
					_i = execute_query(_insert_dbo, etl.inserting.sql_query, _df)
					if not _i:
						_pdq += len(_df)
					_insert_dbo.session.close()
				else: _i = type(_insert_dbo).__name__
				_s = None
			else: _s = type(_df).__name__ + ' - Posible: Retorno de tabla sin resultados'

			if not _f: break
		else:
			if not 'day' in locals(): _s = 'No se puede ejecutar un ETL con fecha de día de hoy'
			
		_extract_dbo.session.close()
	else: _s = type(_extract_dbo).__name__
	return { 'select': _s, 'update': _u, 'insert': _i, 'pdq': _pdq, 'time': (datetime.now() -_btime).total_seconds() }