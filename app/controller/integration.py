# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from re import search

from ..core.integration import execute_integration

def _build(dbo, df, ui):
	_buildBoxs(dbo, df, ui)
	_connectActions(dbo, df, ui)

def _buildBoxs(dbo, df, ui):
	_connection = dbo.session.query(dbo.table.Connection)
	_connection_list = ['Seleccione'] + [str(connection) for connection in _connection.all()]
	ui.util_integration_connectionSelection_comboBox.addItems(_connection_list)

	_query = dbo.session.query(dbo.table.Query)
	_query_sqlUpdate, _query_sqlInsert = (['Seleccione'], ['Seleccione'],)
	for query in _query.all():
		if search(r'\w+', str(query)).group().title() == 'Update':
			_query_sqlUpdate.append(str(query))
		elif search(r'\w+', str(query)).group().title() == 'Insert':
			_query_sqlInsert.append(str(query))
		else: None
	ui.util_integration_sqlUpdate_querySelection_comboBox.addItems(_query_sqlUpdate)
	ui.util_integration_sqlInsert_querySelection_comboBox.addItems(_query_sqlInsert)

	def _build_utilUpdateIntegrationBox(option_selected):
		_sql_query = str()
		if not option_selected == 'Seleccione':
			_query_id = int(search(r'\d+',
								search(r'<id = \d+>$', option_selected).group()).group())
			_query = dbo.session.query(dbo.table.Query).get(_query_id)
			_sql_query = _query.sql_query
		ui.util_integration_sqlUpdate_updateQuery_plainTextEdit.setPlainText(_sql_query)
	_build_utilUpdateIntegrationBox('Seleccione')
	ui.util_integration_sqlUpdate_querySelection_comboBox.activated[str].connect(_build_utilUpdateIntegrationBox)

	def _build_utilInsertIntegrationBox(option_selected):
		_sql_query = str()
		if not option_selected == 'Seleccione':
			_query_id = int(search(r'\d+',
								search(r'<id = \d+>$', option_selected).group()).group())
			_query = dbo.session.query(dbo.table.Query).get(_query_id)
			_sql_query = _query.sql_query
		ui.util_integration_sqlInsert_insertQuery_plainTextEdit.setPlainText(_sql_query)
	_build_utilInsertIntegrationBox('Seleccione')
	ui.util_integration_sqlInsert_querySelection_comboBox.activated[str].connect(_build_utilInsertIntegrationBox)

def _connectActions(dbo, df, ui):
	def _util_integrationClearAction():
		ui.util_integration_connectionSelection_comboBox.setCurrentText('Seleccione')

		ui.util_integration_sqlUpdate_querySelection_comboBox.setCurrentText('Seleccione')
		ui.util_integration_sqlUpdate_updateQuery_plainTextEdit.setPlainText(str())

		ui.util_integration_sqlInsert_querySelection_comboBox.setCurrentText('Seleccione')
		ui.util_integration_sqlInsert_insertQuery_plainTextEdit.setPlainText(str())
	ui.util_integration_clear_pushButton.clicked[bool].connect(_util_integrationClearAction)

	def _util_integrationExecuteAction():
		_connection_selected = ui.util_integration_connectionSelection_comboBox.currentText()
		if not _connection_selected == 'Seleccione':
			_sql_insert = ui.util_integration_sqlInsert_insertQuery_plainTextEdit.toPlainText()
			if _sql_insert:
				_connection_id = int(search(r'\d+',
										search(r'<id = \d+>$', _connection_selected).group()).group())
				_sql_update = ui.util_integration_sqlUpdate_updateQuery_plainTextEdit.toPlainText()
				_connection = dbo.session.query(dbo.table.Connection).get(_connection_id)

				_ = execute_integration(_connection, _sql_update, _sql_insert, df)
				if not _:
					ui.print('La inserción de datos finalizó con éxito. ' \
						f'(tabla de datos con {len(df.last())} fila(s) procesada(s))')
				else: ui.print(f'Error conjunto de tipo: "{_}"')
			else: ui.print('No es posible realizar la inserción de datos con la configuración actual.')
		else: ui.print('No es posible realizar la inserción de datos con la configuración actual.')
	ui.util_integration_execute_pushButton.clicked[bool].connect(_util_integrationExecuteAction)