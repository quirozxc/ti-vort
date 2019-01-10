# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from ._io import connect_database, execute_query

def execute_integration(connection, sql_update, sql_insert, df):
	_ = None
	_dbo = connect_database(connection.db_url)
	if type(_dbo).__name__ == '_DB':
		_u = None
		if sql_update: _u = execute_query(_dbo, sql_update, df.last())
		_i = execute_query(_dbo, sql_insert, df.last())
		if _u or _i: _ = f'{type(_u).__name__} y {type(_i).__name__}'
		_dbo.session.close()
	else: _ = type(_dbo).__name__
	return _