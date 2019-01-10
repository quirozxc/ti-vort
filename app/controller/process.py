# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from re import search
from datetime import date, datetime
from PyQt5.QtWidgets import QFileDialog
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from colorama import Fore, Style
GREEN = Fore.GREEN; RED = Fore.RED; YELLOW = Fore.YELLOW; CYAN = Fore.CYAN
BRIGHT = Style.BRIGHT; RESET = Style.RESET_ALL

from ..core.etl import execute_etl

from ..settings import URL_SAMPLES, TEMPLATE_DIR

def _build(dbo, df, ui):
	_buildBoxs(dbo, df, ui)
	_connectActions(dbo, df, ui)

def _buildBoxs(dbo, df, ui):
	_process = dbo.session.query(dbo.table.Process)
	_process_list = ['Seleccione'] + [str(process) for process in _process.all()]

	ui.process_processSelection_comboBox.addItems(_process_list)

	def _build_ETLBox(option_selected):
		_description, _priority, _lastrun, _extract_from, _insert_to, _select, _update, _insert = (
			str(), int(), None, str(), str(), str(), str(), str(),); _active = False
		if option_selected and not option_selected == 'Seleccione':
			_etl_id = int(search(r'\d+',
							search(r'<id = \d+>$', option_selected).group()).group())
			_etl = dbo.session.query(dbo.table.ETL).get(_etl_id)
			_description, _priority = _etl.description, _etl.priority
		
			_lastrun = _etl.lastrun_date
			
			_extract_from, _insert_to = _etl.extract_from.db_url, _etl.insert_to.db_url
			
			_select, _update, _insert = (
				_etl.selecting.sql_query, _etl.updating.sql_query, _etl.inserting.sql_query)
			
			_active = True
		ui.process_etlExecute_pushButton.setEnabled(_active)
		ui.process_saveChanges_pushButton.setEnabled(_active)
		
		ui.process_etlDescription_plainTextEdit.setPlainText(_description)
		ui.process_priority_spinBox.setValue(_priority)

		if _lastrun: ui.process_etlLastRun_dateEdit.setDate(_lastrun)
		else: ui.process_etlLastRun_dateEdit.setDate(date.min)
		
		ui.process_dbExtraction_url_plainTextEdit.setPlainText(_extract_from)
		ui.process_dbInsertion_url_plainTextEdit.setPlainText(_insert_to)
		
		ui.process_sqlSelect_selectQuery_plainTextEdit.setPlainText(_select)
		ui.process_sqlUpdate_updateQuery_plainTextEdit.setPlainText(_update)
		ui.process_sqlInsert_insertQuery_plainTextEdit.setPlainText(_insert)
	_build_ETLBox('Seleccione')
	ui.process_etlSelection_comboBox.currentTextChanged[str].connect(_build_ETLBox)

	def _build_processBox(option_selected):
		_etl_list = ['Seleccione']; _active = False
		ui.process_etlSelection_comboBox.clear()
		if option_selected and not option_selected == 'Seleccione':
			_process_id = int(search(r'\d+',
								search(r'<id = \d+>$', option_selected).group()).group())
			_process = dbo.session.query(dbo.table.Process).get(_process_id)
			_etl_list += [str(etl) for etl in _process.etls]
			_active = True
		ui.process_etl_label.setEnabled(_active)
		
		ui.process_etlSelection_comboBox.setEnabled(_active)
		ui.process_etlSelection_comboBox.addItems(_etl_list)
		
		ui.process_processExecute_pushButton.setEnabled(_active)
		ui.process_dispatch_pushButton.setEnabled(_active)
		_build_ETLBox('Seleccione')
	_build_processBox('Seleccione')
	ui.process_processSelection_comboBox.currentTextChanged[str].connect(_build_processBox)

	def _build_dbExtractBox_(option_selected):
		_db_url = str()
		if not option_selected == 'Seleccione':
			_connection_id = int(search(r'\d+',
									search(r'<id = \d+>$', option_selected).group()).group())
			_connection = dbo.session.query(dbo.table.Connection).get(_connection_id)
			_db_url = _connection.db_url
		ui.process_dbExtraction_url_plainTextEdit.setPlainText(_db_url)
	ui.process_dbExtraction_connectionSelection_comboBox.activated[str].connect(_build_dbExtractBox_)

	def _build_dbExtractBox(active):
		_connection_list = ['Seleccione']
		if active:
			_connection = dbo.session.query(dbo.table.Connection)
			_connection_list += [str(connection) for connection in _connection.all()]
		ui.process_dbExtraction_connectionSelection_comboBox.setEnabled(active)
		ui.process_dbExtraction_connectionSelection_comboBox.clear()
		ui.process_dbExtraction_connectionSelection_comboBox.addItems(_connection_list)
	_build_dbExtractBox(False)
	ui.process_dbExtraction_connectionSaved_checkBox.clicked[bool].connect(_build_dbExtractBox)

	def _build_dbInsertBox_(option_selected):
		_db_url = str()
		if not option_selected == 'Seleccione':
			_connection_id = int(search(r'\d+',
									search(r'<id = \d+>$', option_selected).group()).group())
			_connection = dbo.session.query(dbo.table.Connection).get(_connection_id)
			_db_url = _connection.db_url
		ui.process_dbInsertion_url_plainTextEdit.setPlainText(_db_url)
	ui.process_dbInsertion_connectionSelection_comboBox.activated[str].connect(_build_dbInsertBox_)

	def _build_dbInsertBox(active):
		_connection_list = ['Seleccione']
		if active:
			_connection = dbo.session.query(dbo.table.Connection)
			_connection_list += [str(connection) for connection in _connection.all()]
		ui.process_dbInsertion_connectionSelection_comboBox.setEnabled(active)
		ui.process_dbInsertion_connectionSelection_comboBox.clear()
		ui.process_dbInsertion_connectionSelection_comboBox.addItems(_connection_list)
	_build_dbInsertBox(False)
	ui.process_dbInsertion_connectionSaved_checkBox.clicked[bool].connect(_build_dbInsertBox)

	def _build_selectBox_(option_selected):
		_sql_query = str()
		if not option_selected == 'Seleccione':
			_query_id = int(search(r'\d+',
								search(r'<id = \d+>$', option_selected).group()).group())
			_query = dbo.session.query(dbo.table.Query).get(_query_id)
			_sql_query = _query.sql_query
		ui.process_sqlSelect_selectQuery_plainTextEdit.setPlainText(_sql_query)
	ui.process_sqlSelect_querySelection_comboBox.activated[str].connect(_build_selectBox_)

	def _build_selectBox(active):
		_query_list = ['Seleccione']
		if active:
			_query = dbo.session.query(dbo.table.Query)
			for query in _query.all():
				if search(r'\w+', str(query)).group().title() == 'Select':
					_query_list.append(str(query))
		ui.process_sqlSelect_querySelection_comboBox.setEnabled(active)
		ui.process_sqlSelect_querySelection_comboBox.clear()
		ui.process_sqlSelect_querySelection_comboBox.addItems(_query_list)
	_build_selectBox(False)
	ui.process_sqlSelect_checkBox.clicked[bool].connect(_build_selectBox)

	def _build_updateBox_(option_selected):
		_sql_query = str()
		if not option_selected == 'Seleccione':
			_query_id = int(search(r'\d+',
								search(r'<id = \d+>$', option_selected).group()).group())
			_query = dbo.session.query(dbo.table.Query).get(_query_id)
			_sql_query = _query.sql_query
		ui.process_sqlUpdate_updateQuery_plainTextEdit.setPlainText(_sql_query)
	ui.process_sqlUpdate_querySelection_comboBox.activated[str].connect(_build_updateBox_)

	def _build_updateBox(active):
		_query_list = ['Seleccione']
		if active:
			_query = dbo.session.query(dbo.table.Query)
			for query in _query.all():
				if search(r'\w+', str(query)).group().title() == 'Update':
					_query_list.append(str(query))
		ui.process_sqlUpdate_querySelection_comboBox.setEnabled(active)
		ui.process_sqlUpdate_querySelection_comboBox.clear()
		ui.process_sqlUpdate_querySelection_comboBox.addItems(_query_list)
	_build_updateBox(False)
	ui.process_sqlUpdate_checkBox.clicked[bool].connect(_build_updateBox)

	def _build_insertBox_(option_selected):
		_sql_query = str()
		if not option_selected == 'Seleccione':
			_query_id = int(search(r'\d+',
								search(r'<id = \d+>$', option_selected).group()).group())
			_query = dbo.session.query(dbo.table.Query).get(_query_id)
			_sql_query = _query.sql_query
		ui.process_sqlInsert_insertQuery_plainTextEdit.setPlainText(_sql_query)
	ui.process_sqlInsert_querySelection_comboBox.activated[str].connect(_build_insertBox_)

	def _build_insertBox(active):
		_query_list = ['Seleccione']
		if active:
			_query = dbo.session.query(dbo.table.Query)
			for query in _query.all():
				if search(r'\w+', str(query)).group().title() == 'Insert':
					_query_list.append(str(query))
		ui.process_sqlInsert_querySelection_comboBox.setEnabled(active)
		ui.process_sqlInsert_querySelection_comboBox.clear()
		ui.process_sqlInsert_querySelection_comboBox.addItems(_query_list)
	_build_insertBox(False)
	ui.process_sqlInsert_checkBox.clicked[bool].connect(_build_insertBox)

	_samples_url = ['Seleccione'] +list(URL_SAMPLES.keys())
	ui.process_dbExtraction_sampleSelection_comboBox.addItems(_samples_url)
	ui.process_dbInsertion_sampleSelection_comboBox.addItems(_samples_url)

	def _build_dbExtractSampleBox(option_selected):
		_active = False
		if not option_selected == 'Seleccione':
			ui.process_dbExtraction_url_plainTextEdit.setPlainText(URL_SAMPLES.get(option_selected))
			if option_selected == 'SQLite': _active = True
		ui.process_dbExtraction_sqlite3_label.setEnabled(_active)
		ui.process_dbExtraction_sqlite3File_lineEdit.setEnabled(_active)
		ui.process_dbExtraction_sqlite3File_lineEdit.setText(str())
		ui.process_dbExtraction_sqlite3Explore_pushButton.setEnabled(_active)
	_build_dbExtractSampleBox('Seleccione')
	ui.process_dbExtraction_sampleSelection_comboBox.activated[str].connect(_build_dbExtractSampleBox)
	
	def _build_dbInsertSampleBox(option_selected):
		_active = False
		if not option_selected == 'Seleccione':
			ui.process_dbInsertion_url_plainTextEdit.setPlainText(URL_SAMPLES.get(option_selected))
			if option_selected == 'SQLite': _active = True
		ui.process_dbInsertion_sqlite3_label.setEnabled(_active)
		ui.process_dbInsertion_sqlite3File_lineEdit.setEnabled(_active)
		ui.process_dbInsertion_sqlite3File_lineEdit.setText(str())
		ui.process_dbInsertion_sqlite3Explore_pushButton.setEnabled(_active)
	_build_dbInsertSampleBox('Seleccione')
	ui.process_dbInsertion_sampleSelection_comboBox.activated[str].connect(_build_dbInsertSampleBox)

def _connectActions(dbo, df, ui):
	def _processExecuteAction():
		_process_selected = ui.process_processSelection_comboBox.currentText()
		_process_id = int(search(r'\d+',
								search(r'<id = \d+>$', _process_selected).group()).group())
		_process = dbo.session.query(dbo.table.Process).get(_process_id)

		print(f'\nEjecución del Proceso (conjunto de ETLs) {CYAN}{BRIGHT}"{_process.name}"{RESET}...')
		for etl in _process.etls:
			_ = execute_etl(etl, ui.process_etlLastRun_dateEdit.date().toPyDate())
			if _.get('pdq'):
				etl.lastrun_date = date.today()
				etl.binnacle.append(dbo.table.Binnacle(
								execution_timestamp		= datetime.now(),
								processed_data_quantity = _.get('pdq')))
				dbo.session.commit()
			_print_etl(etl.name,
						_.get('select'), _.get('update'), _.get('insert'),
						_.get('pdq'), _.get('time'))
		# ui.process_etlLastRun_dateEdit.setDate(etl.lastrun_date)
		print(f'Conjunto de ETLs (proceso {CYAN}{BRIGHT}"{_process.name}"{RESET}) terminado.\n')

		ui.print(f'La ejecución del proceso (conjunto de ETLs) "{_process.name}" ha concluido.')
	ui.process_processExecute_pushButton.clicked[bool].connect(_processExecuteAction)

	def _etlExecuteAction():
		_etl_selected = ui.process_etlSelection_comboBox.currentText()
		_etl_id = int(search(r'\d+',
						search(r'<id = \d+>$', _etl_selected).group()).group())
		_etl = dbo.session.query(dbo.table.ETL).get(_etl_id)

		_ = execute_etl(_etl, ui.process_etlLastRun_dateEdit.date().toPyDate())
		if _.get('pdq'):
			_etl.lastrun_date = date.today()
			_etl.binnacle.append(dbo.table.Binnacle(
							execution_timestamp		= datetime.now(),
							processed_data_quantity = _.get('pdq')))
			dbo.session.commit()
		_print_etl(_etl.name,
					_.get('select'), _.get('update'), _.get('insert'),
					_.get('pdq'), _.get('time'))
		# ui.process_etlLastRun_dateEdit.setDate(_etl.lastrun_date)
		ui.print(f'La ejecución del ETL "{_etl.name}" ha concluido.')
	ui.process_etlExecute_pushButton.clicked[bool].connect(_etlExecuteAction)

	def _dbExtrac_sqlite3ExploreAction():
		_fileName, _ = QFileDialog.getOpenFileName(ui.vort_centralWidget,
			filter = 'BBDD con extensión .sqlite3 (*.sqlite3);;' \
					 'BBDD con extensión .sqlite (*.sqlite);;' \
					 'SQLite con extensión .bin (*.bin);;' \
					 'SQLite con extensión .data (*.data)')
		if _fileName:
			ui.process_dbExtraction_sqlite3File_lineEdit.setText(_fileName)
			ui.process_dbExtraction_url_plainTextEdit.setPlainText(r'sqlite:///' +_fileName)
	ui.process_dbExtraction_sqlite3Explore_pushButton.clicked[bool].connect(_dbExtrac_sqlite3ExploreAction)

	def _dbInsert_sqlite3ExploreAction():
		_fileName, _ = QFileDialog.getOpenFileName(ui.vort_centralWidget,
			filter = 'BBDD con extensión .sqlite3 (*.sqlite3);;' \
					 'BBDD con extensión .sqlite (*.sqlite);;' \
					 'SQLite con extensión .bin (*.bin);;' \
					 'SQLite con extensión .data (*.data)')
		if _fileName:
			ui.process_dbInsertion_sqlite3File_lineEdit.setText(_fileName)
			ui.process_dbInsertion_url_plainTextEdit.setPlainText(r'sqlite:///' +_fileName)
	ui.process_dbInsertion_sqlite3Explore_pushButton.clicked[bool].connect(_dbInsert_sqlite3ExploreAction)

	def _dispatchAction():
		_fileName, _ = QFileDialog.getSaveFileName(ui.vort_centralWidget,
			filter = 'Extensión .pdf (*.pdf);;' \
					 'Extensión .html (*.html)')
		if _fileName:
			_process_selected = ui.process_processSelection_comboBox.currentText()
			_etl_selected = ui.process_etlSelection_comboBox.currentText()
			
			_html_out = None	
			_ext = search(r'\w+$', _fileName).group()
			if _etl_selected == 'Seleccione':
				_process_id = int(search(r'\d+',
									search(r'<id = \d+>$', _process_selected).group()).group())
				_process = dbo.session.query(dbo.table.Process).get(_process_id)
				_template = _make_template('_dossier_process.html')
				_html_out = _template.render({'process': _process})
			else:
				_etl_id = int(search(r'\d+',
									search(r'<id = \d+>$', _etl_selected).group()).group())
				_etl = dbo.session.query(dbo.table.ETL).get(_etl_id)
				_template = _make_template('_dossier_etl.html')
				_html_out = _template.render({'etl': _etl})

			if _ext == 'html':
				_f = open(_fileName, 'w'); _f.write(_html_out); _f.close()
			else: HTML(string = _html_out).write_pdf(_fileName)

			ui.print(f'Los datos han sido guardados en {_fileName}.')
	ui.process_dispatch_pushButton.clicked[bool].connect(_dispatchAction)

	def _processClearAction():
		ui.process_processSelection_comboBox.setCurrentText('Seleccione')
		ui.process_etlSelection_comboBox.setCurrentText('Seleccione')
		ui.process_etlSelection_comboBox.setEnabled(False)

		ui.process_processExecute_pushButton.setEnabled(False)
		ui.process_etlExecute_pushButton.setEnabled(False)
		ui.process_saveChanges_pushButton.setEnabled(False)

		ui.process_etlDescription_plainTextEdit.setPlainText(str())
		ui.process_priority_spinBox.setValue(1)

		ui.process_dbExtraction_sampleSelection_comboBox.setCurrentText('Seleccione')
		ui.process_dbExtraction_url_plainTextEdit.setPlainText(str())
		if ui.process_dbExtraction_connectionSaved_checkBox.isChecked():
			ui.process_dbExtraction_connectionSaved_checkBox.click()
		ui.process_dbExtraction_sqlite3_label.setEnabled(False)
		ui.process_dbExtraction_sqlite3File_lineEdit.setEnabled(False)
		ui.process_dbExtraction_sqlite3File_lineEdit.setText(str())
		ui.process_dbExtraction_sqlite3Explore_pushButton.setEnabled(False)

		ui.process_dbInsertion_sampleSelection_comboBox.setCurrentText('Seleccione')
		ui.process_dbInsertion_url_plainTextEdit.setPlainText(str())
		if ui.process_dbInsertion_connectionSaved_checkBox.isChecked():
			ui.process_dbInsertion_connectionSaved_checkBox.click()
		ui.process_dbInsertion_sqlite3_label.setEnabled(False)
		ui.process_dbInsertion_sqlite3File_lineEdit.setEnabled(False)
		ui.process_dbInsertion_sqlite3File_lineEdit.setText(str())
		ui.process_dbInsertion_sqlite3Explore_pushButton.setEnabled(False)

		if ui.process_sqlSelect_checkBox.isChecked():
			ui.process_sqlSelect_checkBox.click()
		ui.process_sqlSelect_selectQuery_plainTextEdit.setPlainText(str())

		if ui.process_sqlUpdate_checkBox.isChecked():
			ui.process_sqlUpdate_checkBox.click()
		ui.process_sqlUpdate_updateQuery_plainTextEdit.setPlainText(str())

		if ui.process_sqlInsert_checkBox.isChecked():
			ui.process_sqlInsert_checkBox.click()
		ui.process_sqlInsert_insertQuery_plainTextEdit.setPlainText(str())
	ui.process_clear_pushButton.clicked[bool].connect(_processClearAction)

	def _process_saveChangesAction():
		_etl_description = ui.process_etlDescription_plainTextEdit.toPlainText()
		_etl_priority	 = ui.process_priority_spinBox.value()

		_etl_lastrun	 = ui.process_etlLastRun_dateEdit.date().toPyDate()

		_etl_extract_from = ui.process_dbExtraction_url_plainTextEdit.toPlainText()
		_etl_insert_to	  = ui.process_dbInsertion_url_plainTextEdit.toPlainText()
		
		_etl_selecting = ui.process_sqlSelect_selectQuery_plainTextEdit.toPlainText()
		_etl_updating  = ui.process_sqlUpdate_updateQuery_plainTextEdit.toPlainText()
		_etl_inserting = ui.process_sqlInsert_insertQuery_plainTextEdit.toPlainText()

		_process_selected = ui.process_processSelection_comboBox.currentText()
		
		_etl_selected	  = ui.process_etlSelection_comboBox.currentText()
		_etl_id 		  = int(search(r'\d+',
									search(r'<id = \d+>$', _etl_selected).group()).group())
		_etl = dbo.session.query(dbo.table.ETL).get(_etl_id)

		_etl.description 	   = _etl_description
		_etl.priority 		   = _etl_priority
		
		_etl.lastrun_date 	   = _etl_lastrun

		_etl.lastmod_timestamp = datetime.now()

		_etl.extract_from.db_url = _etl_extract_from
		if ui.process_dbExtraction_connectionSaved_checkBox.isChecked():
			_connection_selected = ui.process_dbExtraction_connectionSelection_comboBox.currentText()
			if not _connection_selected == 'Seleccione':
				_connection_id = int(search(r'\d+',
										search(r'<id = \d+>$', _connection_selected).group()).group())
				_connection = dbo.session.query(dbo.table.Connection).get(_connection_id)
				dbo.session.delete(_etl.extract_from)
				_etl.extract_from = _connection

		_etl.insert_to.db_url = _etl_insert_to
		if ui.process_dbInsertion_connectionSaved_checkBox.isChecked():
			_connection_selected = ui.process_dbInsertion_connectionSelection_comboBox.currentText()
			if not _connection_selected == 'Seleccione':
				_connection_id = int(search(r'\d+',
										search(r'<id = \d+>$', _connection_selected).group()).group())
				_connection = dbo.session.query(dbo.table.Connection).get(_connection_id)
				dbo.session.delete(_etl.insert_to)
				_etl.insert_to = _connection

		_etl.selecting.sql_query = _etl_selecting
		if ui.process_sqlSelect_checkBox.isChecked():
			_query_selected = ui.process_sqlSelect_querySelection_comboBox.currentText()
			if not _query_selected == 'Seleccione':
				_query_id = int(search(r'\d+',
								search(r'<id = \d+>$', _query_selected).group()).group())
				_query = dbo.session.query(dbo.table.Query).get(_query_id)
				dbo.session.delete(_etl.selecting)
				_etl.selecting = _query

		_etl.updating.sql_query = _etl_updating
		if ui.process_sqlUpdate_checkBox.isChecked():
			_query_selected = ui.process_sqlUpdate_querySelection_comboBox.currentText()
			if not _query_selected == 'Seleccione':
				_query_id = int(search(r'\d+',
								search(r'<id = \d+>$', _query_selected).group()).group())
				_query = dbo.session.query(dbo.table.Query).get(_query_id)
				dbo.session.delete(_etl.updating)
				_etl.updating = _query

		_etl.inserting.sql_query = _etl_inserting
		if ui.process_sqlInsert_checkBox.isChecked():
			_query_selected = ui.process_sqlInsert_querySelection_comboBox.currentText()
			if not _query_selected == 'Seleccione':
				_query_id = int(search(r'\d+',
								search(r'<id = \d+>$', _query_selected).group()).group())
				_query = dbo.session.query(dbo.table.Query).get(_query_id)
				dbo.session.delete(_etl.inserting)
				_etl.inserting = _query
		try:
			dbo.session.commit()
		except:
			ui.print(f'Se ha generado un error de tipo "{type(e).__name__}".')
			dbo.session.rollback()
		else:
			_update_uiBoxs(dbo, ui)
			ui.process_processSelection_comboBox.setCurrentText(_process_selected)
			ui.process_etlSelection_comboBox.setCurrentText(_etl_selected)

			ui.print(f'Los cambios en el ETL "{_etl.name}" han sido guardados.')
	ui.process_saveChanges_pushButton.clicked[bool].connect(_process_saveChangesAction)

def _print_etl(etl_name, s, u, i, pdq, time):
	print(f'\n\nEjecución del ETL {YELLOW}{BRIGHT}"{etl_name}"{RESET}')
	if not s: print(f'  Selecting: {GREEN}{BRIGHT}Done{RESET}')
	else: print(f'  Selecting: {RED}{BRIGHT}{s}{RESET}')

	if not u: print(f'  Updating: {GREEN}{BRIGHT}Done{RESET}')
	else: print(f'  Updating: {RED}{BRIGHT}{u}{RESET}')

	if not i: print(f'  Inserting: {GREEN}{BRIGHT}Done{RESET}')
	else: print(f'  Inserting: {RED}{BRIGHT}{i}{RESET}')

	if pdq: print(f'{pdq} fila(s) procesada(s) en {time} segundos')
	print()

def _make_template(template_name):
	_env = Environment(loader = FileSystemLoader(TEMPLATE_DIR))

	def _dtformat(dt, f = r'%a %d %b %Y - %I:%M:%S %p'):
		if dt:
			return dt.strftime(f)
	_env.filters['dtformat'] = _dtformat

	return _env.get_template(template_name)

def _update_uiBoxs(dbo, ui):
	_process = dbo.session.query(dbo.table.Process)
	_process_list = ['Seleccione'] + [str(process) for process in _process.all()]
	_uiObjects = [ ui.util_setting_newProcessSelection_comboBox,
				   ui.process_processSelection_comboBox, ]
	for uiObject in _uiObjects:
		uiObject.clear(); uiObject.addItems(_process_list)

	_connection = dbo.session.query(dbo.table.Connection)
	_connection_list = ['Seleccione'] + [str(connection) for connection in _connection.all()]
	
	_uiObjects = [ ui.process_dbExtraction_connectionSelection_comboBox,
				   ui.process_dbInsertion_connectionSelection_comboBox,
				   ui.util_extraction_connectionSelection_comboBox,
				   ui.util_integration_connectionSelection_comboBox, ]
	for uiObject in _uiObjects:
		uiObject.clear(); uiObject.addItems(_connection_list)

	_query = dbo.session.query(dbo.table.Query)
	_query_sqlSelect, _query_sqlUpdate, _query_sqlInsert = (
		['Seleccione'], ['Seleccione'], ['Seleccione'],)
	
	for query in _query.all():
		if search(r'\w+', str(query)).group().title() == 'Select':
			_query_sqlSelect.append(str(query))
		elif search(r'\w+', str(query)).group().title() == 'Update':
			_query_sqlUpdate.append(str(query))
		elif search(r'\w+', str(query)).group().title() == 'Insert':
			_query_sqlInsert.append(str(query))
		else: None

	_uiObjects = [ ui.util_extraction_sqlSelect_querySelection_comboBox,
				   ui.process_sqlSelect_querySelection_comboBox, ]
	for uiObject in _uiObjects:
		uiObject.clear(); uiObject.addItems(_query_sqlSelect)

	_uiObjects = [ ui.util_integration_sqlUpdate_querySelection_comboBox,
				   ui.process_sqlUpdate_querySelection_comboBox, ]
	for uiObject in _uiObjects:
		uiObject.clear(); uiObject.addItems(_query_sqlUpdate)

	_uiObjects = [ ui.util_integration_sqlInsert_querySelection_comboBox,
				   ui.process_sqlInsert_querySelection_comboBox, ]
	for uiObject in _uiObjects:
		uiObject.clear(); uiObject.addItems(_query_sqlInsert)