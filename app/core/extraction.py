# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from ._io import connect_database, execute_query

def execute_extraction(connection, sql_select, df):
	_ = None
	_dbo = connect_database(connection.db_url)
	if type(_dbo).__name__ == '_DB':
		_df = execute_query(_dbo, sql_select)
		if type(_df).__name__ == 'DataFrame': df.append(_df)
		else: _ = type(_df).__name__
		_dbo.session.close()
	else: _ = type(_dbo).__name__
	return _