# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from re import search

from .complement import _dfBox
from ..core.extraction import execute_extraction

def _build(dbo, df, ui):
	_buildBoxs(dbo, df, ui)
	_connectActions(dbo, df, ui)

def _buildBoxs(dbo, df, ui):
	_connection = dbo.session.query(dbo.table.Connection)
	_connection_list = ['Seleccione'] + [str(connection) for connection in _connection.all()]
	ui.util_extraction_connectionSelection_comboBox.addItems(_connection_list)

	_query = dbo.session.query(dbo.table.Query)
	_query_sqlSelect = ['Seleccione']
	for query in _query.all():
		if search(r'\w+', str(query)).group().title() == 'Select':
			_query_sqlSelect.append(str(query))
	ui.util_extraction_sqlSelect_querySelection_comboBox.addItems(_query_sqlSelect)

	def _build_utilSelectExtractionBox(option_selected):
		_sql_query = str()
		if not option_selected == 'Seleccione':
			_query_id = int(search(r'\d+',
								search(r'<id = \d+>$', option_selected).group()).group())
			_query = dbo.session.query(dbo.table.Query).get(_query_id)
			_sql_query = _query.sql_query
		ui.util_extraction_sqlSelect_selectQuery_plainTextEdit.setPlainText(_sql_query)
	_build_utilSelectExtractionBox('Seleccione')
	ui.util_extraction_sqlSelect_querySelection_comboBox.activated[str].connect(_build_utilSelectExtractionBox)

def _connectActions(dbo, df, ui):
	def _util_extractClearAction():
		ui.util_extraction_connectionSelection_comboBox.setCurrentText('Seleccione')
		ui.util_extraction_sqlSelect_querySelection_comboBox.setCurrentText('Seleccione')
		ui.util_extraction_sqlSelect_selectQuery_plainTextEdit.setPlainText(str())
	ui.util_extraction_clear_pushButton.clicked[bool].connect(_util_extractClearAction)

	def _util_extractExecuteAction():
		_connection_selected = ui.util_extraction_connectionSelection_comboBox.currentText()
		if not _connection_selected == 'Seleccione':
			_sql_select = ui.util_extraction_sqlSelect_selectQuery_plainTextEdit.toPlainText()
			if _sql_select:
				_connection_id = int(search(r'\d+',
										search(r'<id = \d+>$', _connection_selected).group()).group())
				_connection = dbo.session.query(dbo.table.Connection).get(_connection_id)

				_ = execute_extraction(_connection, _sql_select, df)
				if not _:
					_dfBox(df, ui)
					ui.print('La extracción de datos finalizó con éxito. ' \
							f'(tabla de datos con {len(df.last())} fila(s) generada(s))')
				else: ui.print(f'Error de tipo "{_}" al intentar ejecutar la extracción de datos')
			else: ui.print('No es posible ejecutar la extracción de datos con la configuración actual.')
		else: ui.print('No es posible ejecutar la extracción de datos con la configuración actual.')
	ui.util_extraction_execute_pushButton.clicked[bool].connect(_util_extractExecuteAction)