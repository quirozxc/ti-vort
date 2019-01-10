# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from re import search
from datetime import datetime

from petl.io import fromdataframe
from petl.util.vis import lookall as look
from pandas.plotting import table

from ..core._io import import_file, export_file

from ..settings import DISPLAY_LAYOUTS, ABOUT_MESSAGE

def _build(dbo, df, ui):
	_buildBoxs(dbo, df, ui)
	_connectActions(dbo, df, ui)
	_dfBox(df, ui)

def _buildBoxs(dbo, df, ui):
	_process = dbo.session.query(dbo.table.Process)
	_process_list = ['Seleccione'] + [str(process) for process in _process.all()]
	ui.util_setting_newProcessSelection_comboBox.addItems(_process_list)

	def _utilSettingBox(option_selected):
		_new_priority = 1
		if not option_selected == 'Seleccione':
			_process_id = int(search(r'\d+',
								search(r'<id = \d+>$', option_selected).group()).group())
			_process = dbo.session.query(dbo.table.Process).get(_process_id)
			if _process.etls:
				_new_priority = _process.etls[-1].priority +1
		ui.util_setting_newPriority_spinBox.setValue(_new_priority)
	_utilSettingBox('Seleccione')
	ui.util_setting_newProcessSelection_comboBox.activated[str].connect(_utilSettingBox)

def _connectActions(dbo, df, ui):
	def _util_createProcessAction():
		_process_name = ui.util_setting_newProcessName_lineEdit.text()
		if _process_name:
			dbo.session.add(dbo.table.Process(
				name = _process_name,
				creation_timestamp = datetime.now()))
			dbo.session.commit()

			def _util_updateProcessBox():
				_current_process = ui.process_processSelection_comboBox.currentText()
				_current_etl = ui.process_etlSelection_comboBox.currentText()

				_process = dbo.session.query(dbo.table.Process)
				_process_list = ['Seleccione'] + [str(process) for process in _process.all()]

				ui.process_processSelection_comboBox.clear()
				ui.util_setting_newProcessSelection_comboBox.clear()

				ui.process_processSelection_comboBox.addItems(_process_list)
				ui.util_setting_newProcessSelection_comboBox.addItems(_process_list)

				ui.process_processSelection_comboBox.setCurrentText(_current_process)
				ui.process_etlSelection_comboBox.setCurrentText(_current_etl)

			_util_updateProcessBox()
			ui.print(f'Nuevo proceso "{_process_name}" creado.')
		else: ui.print('No se puede crear un proceso nuevo sin nombre.')
	ui.util_setting_new_create_pushButton.clicked[bool].connect(_util_createProcessAction)

	def _util_createETLAction():
		_process_name = ui.util_setting_newProcessSelection_comboBox.currentText()
		_etl_name = ui.util_setting_newETLName_lineEdit.text()
		_etl_description = ui.util_setting_newETLDescription_plainTextEdit.toPlainText()
		if not _process_name == 'Seleccione' and _etl_name:
			_process_id = int(search(r'\d+',
								search(r'<id = \d+>$', _process_name).group()).group())
			_process = dbo.session.query(dbo.table.Process).get(_process_id)
			_etl_priorty = ui.util_setting_newPriority_spinBox.value()
			try:
				_etl = dbo.table.ETL(
					name        = _etl_name,
					description = _etl_description,
					priority    = _etl_priorty,
					creation_timestamp = datetime.now(), 
					extract_from = dbo.table.Connection(
										db_url = '<Requiere atención>',
										creation_timestamp = datetime.now()),
					insert_to    = dbo.table.Connection(
										db_url = '<Requiere atención>',
										creation_timestamp = datetime.now()),
					selecting = dbo.table.Query(
									sql_query = 'SELECT... <Requiere atención>',
									creation_timestamp = datetime.now()),
					updating  = dbo.table.Query(
									sql_query = 'UPDATE... <Requiere atención>',
									creation_timestamp = datetime.now()),
					inserting = dbo.table.Query(
									sql_query = 'INSERT INTO... <Requiere atención>',
									creation_timestamp = datetime.now()))
				_process.etls.append(_etl)
				dbo.session.commit()

				ui.process_clear_pushButton.click()
				ui.process_processSelection_comboBox.setCurrentText(str(_process))
				ui.process_etlSelection_comboBox.setCurrentText(str(_etl))
			except Exception as e:
				ui.print(f'Se ha generado un error de tipo "{type(e).__name__}" ' \
					'al intentar crear el nuevo ETL.')
				dbo.session.rollback()
			else: ui.print(f'Nuevo ETL "{_etl_name}" ' \
					   f'creado y asignado al proceso "{_process.name}"')
		else: ui.print(f'No se puede crear un nuevo ETL sin un proceso o nombre indicado.')
	ui.util_setting_new_apply_pushButton.clicked[bool].connect(_util_createETLAction)

	def _util_createClearAction():
		ui.util_setting_newProcessName_lineEdit.setText(str())
		ui.util_setting_newProcessSelection_comboBox.setCurrentText('Seleccione')
		ui.util_setting_newETLName_lineEdit.setText(str())
		ui.util_setting_newETLDescription_plainTextEdit.setPlainText(str())
		ui.util_setting_newPriority_spinBox.setValue(1)
	ui.util_setting_new_clear_pushButton.clicked[bool].connect(_util_createClearAction)

	def _importAction():
		_fileName, _ = QFileDialog.getOpenFileName(ui.vort_centralWidget,
			filter = 'Libro de Excel (*.xlsx);;' \
					 'Libro de Excel 97-2003 (*.xls);;' \
					 'Extensión .csv (*.csv);;' \
					 'Extensión .tsv (*.tsv);;' \
					 'Extensión .json (*.json)')
		if _fileName:
			_name = search(r'\w+.\w+$', _fileName).group()
			_df = import_file(_fileName)
			if type(_df).__name__ == 'DataFrame':
				df.append(_df); _dfBox(df, ui)
				ui.print(f'La carga de datos desde el archivo "{_name}" ' \
					'finalizó con éxito.')
			else:
				ui.print(f'Se ha generado un error de tipo "{type(_df).__name__}" ' \
					f'al intentar importar "{_name}".')
	ui.options_import_pushButton.clicked[bool].connect(_importAction)

	def _printAction():
		ui.display_plot.figure.clear()
		ax = ui.display_plot.figure.subplots()
		ui.display_plot.figure.tight_layout(rect = DISPLAY_LAYOUTS[1])
		
		table(ax, df.last().round(3).head(20), loc = 'upper center')
		
		dflen = len(df.last())
		if dflen > 20:
			ax.set_title(f'Tabla de Datos\n(primeras 20 filas de {dflen} en total)')
		else: ax.set_title(f'Tabla de Datos\n({dflen} filas en total)')
		ax.set_axis_off()
		
		ui.display_plot.draw()
		print(f'\n  Tabla completa de datos ({len(df.last())} filas). <VORT>')
		print(look(fromdataframe(df.last().round(3))))
		print([ dt.name for dt in df.last().dtypes.tolist()])
		print('\n\n  Descripción de estadística básica de la tabla. <VORT>')
		print(look(df.last().describe(include = 'all').round(3).astype(str).to_records()))
		ui.print('Visualización de la última tabla de datos.')
	ui.options_print_pushButton.clicked[bool].connect(_printAction)

	def _undoAction():
		df.pop(); _dfBox(df, ui)
		ui.print(f'Última tabla de datos desechada. <{df.size()} tabla(s) restante(s)>')
	ui.options_undo_pushButton.clicked[bool].connect(_undoAction)

	def _copyAction():
		df.last().to_clipboard()
		ui.print('Última tabla de datos copiada con éxito al portapapeles.')
	ui.options_copy_pushButton.clicked[bool].connect(_copyAction)

	def _exportAction():
		_fileName, _ = QFileDialog.getSaveFileName(ui.vort_centralWidget,
			filter = 'Libro de Excel (*.xlsx);;' \
					 'Libro de Excel 97-2003 (*.xls);;' \
					 'Extensión .csv (*.csv);;' \
					 'Extensión .tsv (*.tsv);;' \
					 'Extensión .json (*.json)')
		if _fileName:
			_ = export_file(_fileName, df.last())
			if not _:
				ui.print(f'Tabla de datos guardada en {_fileName}.')
			else:
				ui.print(f'Se ha generado un error de tipo "{type(_).__name__}" ' \
					'al intentar exportar.')
	ui.options_export_pushButton.clicked[bool].connect(_exportAction)

	def _clearAction():
		df.clear(); _dfBox(df, ui)
		ui.print('Conjunto de datos limpiado exitosamente.')
	ui.options_clear_pushButton.clicked[bool].connect(_clearAction)

	def _aboutAction():
		QMessageBox.information(ui.vort_centralWidget,
			'Acerca de Visualization of Object-Relational Transformed', ABOUT_MESSAGE)
	ui.options_about_pushButton.clicked[bool].connect(_aboutAction)

def _dfBox(df, ui):
	_columns = ['Seleccione']
	_active = None
	_uiObjects = [ ui.options_export_pushButton,
				   ui.options_data_label,
				   ui.options_print_pushButton,
				   ui.options_undo_pushButton,
				   ui.options_copy_pushButton,
				   ui.options_clear_pushButton, 

				   ui.util_transfTools_apply_pushButton,
				   ui.util_visualDesing_apply_pushButton,
				   ui.util_visualDesing_export_pushButton,

				   ui.util_regression_analyze_pushButton,
				   ui.util_classification_analyze_pushButton,
				   ui.util_clustering_analyze_pushButton, 

				   ui.util_integration_execute_pushButton, ]
	
	if not df.isEmpty():
		_columns += list(df.last().columns)
		_active = True
	else: _active = False
	
	for _uiObject in _uiObjects:
		_uiObject.setEnabled(_active)

	_uiComboBoxs = [ ui.util_transfTools_columnSelection_comboBox,

					 ui.util_regression_columnXSelection_comboBox,
					 ui.util_regression_columnYSelection_comboBox,

					 ui.util_classification_columnXSelection_comboBox,
					 ui.util_classification_columnYSelection_comboBox,

					 ui.util_clustering_columnXSelection_comboBox,
					 ui.util_clustering_columnYSelection_comboBox, ]
	for _uiCombo in _uiComboBoxs:
		_uiCombo.clear()
		_uiCombo.addItems(_columns)
