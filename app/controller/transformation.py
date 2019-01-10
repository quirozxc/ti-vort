# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from petl.io import fromdataframe

from ..core.transformation import addrownumbers
from ..core.transformation import convert
from ..core.transformation import movefield
from ..core.transformation import rename
from ..core.transformation import replace
from ..core.transformation import fillleft, filldown, fillright

from ..settings import TRANSF_TOOLS

def _build(dbo, df, ui):
	_buildBoxs(dbo, df, ui)
	_connectActions(dbo, df, ui)

def _buildBoxs(dbo, df, ui):
	_transf_tools = ['Seleccione'] +TRANSF_TOOLS

	ui.util_transfTools_toolSelection_comboBox.addItems(_transf_tools)

	def _build_utilTransfToolsBox(option_selected):
		_t, _f = True, False
		_uiObjects = [ ui.util_transfTools_columnSelection_comboBox,
					   ui.util_transfTools_index_groupBox,
					   ui.util_transfTools_values_groupBox,
					   ui.util_transfTools_order_groupBox,
					   ui.util_transfTools_format_groupBox,
					   ui.util_transfTools_columnName_lineEdit,
					   ui.util_transfTools_position_label,
					   ui.util_transfTools_position_spinBox,
					   ui.util_transfTools_decimals_label,
					   ui.util_transfTools_decimals_spinBox, ]
		_transfTool_uiShifts = { TRANSF_TOOLS[0]: [_f, _t, _f, _f, _f, _t, _f, _f, _f, _f,],   # Añadir columna
								 TRANSF_TOOLS[1]: [_t, _f, _f, _f, _t, _f, _f, _f, _f, _f,],   # Convertir columna
								 TRANSF_TOOLS[2]: [_t, _f, _f, _f, _f, _f, _t, _t, _f, _f,],   # Mover una columna
								 TRANSF_TOOLS[3]: [_t, _f, _f, _f, _f, _t, _f, _f, _f, _f,],   # Cambiar nombre
								 TRANSF_TOOLS[4]: [_f, _f, _f, _f, _f, _f, _f, _f, _t, _t,],   # Redondear valores
								 TRANSF_TOOLS[5]: [_t, _f, _t, _f, _f, _f, _f, _f, _f, _f,],   # Cambiar un valor
								 TRANSF_TOOLS[6]: [_f, _f, _f, _t, _f, _f, _f, _f, _f, _f,], } # Completar valores
		if not option_selected == 'Seleccione':
			for uiObject, uiShift in zip(_uiObjects, _transfTool_uiShifts.get(option_selected)):
				uiObject.setEnabled(uiShift)
		else:
			for uiObject in _uiObjects:
				uiObject.setEnabled(_f)
	_build_utilTransfToolsBox('Seleccione')
	ui.util_transfTools_toolSelection_comboBox.activated[str].connect(_build_utilTransfToolsBox)

def _connectActions(dbo, df, ui):
	def _util_transfClearAction():
		ui.util_transfTools_toolSelection_comboBox.setCurrentText('Seleccione')
		ui.util_transfTools_columnSelection_comboBox.setCurrentText('Seleccione')

		ui.util_transfTools_columnName_lineEdit.setText(str())

		ui.util_transfTools_indexStart_spinBox.setValue(0)
		ui.util_transfTools_indexStep_spinBox.setValue(0)

		ui.util_transfTools_valuesExistent_lineEdit.setText(str())
		ui.util_transfTools_valuesReplacement_lineEdit.setText(str())

		ui.util_transfTools_position_spinBox.setValue(1)
		ui.util_transfTools_decimals_spinBox.setValue(1)

		ui.util_transfTools_orderLeft_radioButton.click()
		ui.util_transfTools_formatDecimal_radioButton.click()

		_uiObjects = [ ui.util_transfTools_columnSelection_comboBox,
					   ui.util_transfTools_index_groupBox,
					   ui.util_transfTools_values_groupBox,
					   ui.util_transfTools_order_groupBox,
					   ui.util_transfTools_format_groupBox,
					   ui.util_transfTools_columnName_lineEdit,
					   ui.util_transfTools_position_label,
					   ui.util_transfTools_position_spinBox,
					   ui.util_transfTools_decimals_label,
					   ui.util_transfTools_decimals_spinBox, ]
		for _uiObject in _uiObjects: _uiObject.setEnabled(False)
	ui.util_transfTools_clear_pushButton.clicked[bool].connect(_util_transfClearAction)

	def _util_transfApplyAction():
		_tTool = ui.util_transfTools_toolSelection_comboBox.currentText()

		if _tTool == TRANSF_TOOLS[0]: # Añadir columna
			_start = ui.util_transfTools_indexStart_spinBox.value()
			_step = ui.util_transfTools_indexStep_spinBox.value()
			_cName = ui.util_transfTools_columnName_lineEdit.text()
			_tb = fromdataframe(df.last())

			if not _cName: _cName = 'Nueva Col'
			_ = addrownumbers(_tb, start = _start, step = _step, field = _cName)
			
			df.append(_.todataframe())
			ui.print(f'La nueva columna nombrada "{_cName}" ha sido añadida a la tabla de datos.')

		if _tTool == TRANSF_TOOLS[1]: # Convertir columna
			if not ui.util_transfTools_columnSelection_comboBox.currentText() == 'Seleccione':
				_cSelect = ui.util_transfTools_columnSelection_comboBox.currentText()
				_tb = fromdataframe(df.last())
				_ = None

				if ui.util_transfTools_formatDecimal_radioButton.isChecked():
					_ = convert(_tb, _cSelect, float)
				else: _ = convert(_tb, _cSelect, str)

				df.append(_.todataframe())
				ui.print(f'La columna "{_cSelect}" de la tabla de datos ha sido formateada.')

		if _tTool == TRANSF_TOOLS[2]: # Mover una columna
			if not ui.util_transfTools_columnSelection_comboBox.currentText() == 'Seleccione':
				_cSelect = ui.util_transfTools_columnSelection_comboBox.currentText()
				_position = ui.util_transfTools_position_spinBox.value()
				_tb = fromdataframe(df.last())

				_ = movefield(_tb, _cSelect, _position)

				df.append(_.todataframe())
				ui.print(f'La columna "{_cSelect}" de la tabla de datos ha sido reubicada.')
		
		if _tTool == TRANSF_TOOLS[3]: # Cambiar nombre
			if not ui.util_transfTools_columnSelection_comboBox.currentText() == 'Seleccione':
				_cSelect = ui.util_transfTools_columnSelection_comboBox.currentText()
				_cName = ui.util_transfTools_columnName_lineEdit.text()
				_tb = fromdataframe(df.last())

				_ = rename(_tb, _cSelect, _cName)

				df.append(_.todataframe())
				ui.print(f'La columna "{_cSelect}" de la tabla de datos ha sido renombrada a "{_cName}".')

		if _tTool == TRANSF_TOOLS[4]: # Redondear valores
			_decimals = ui.util_transfTools_decimals_spinBox.value()

			df.append(round(df.last(), _decimals))

			ui.print(f'La tabla de datos ha sido redondeada.')

		if _tTool == TRANSF_TOOLS[5]: # Cambiar un valor
			if not ui.util_transfTools_columnSelection_comboBox.currentText() == 'Seleccione':
				_cSelect = ui.util_transfTools_columnSelection_comboBox.currentText()
				_vExistent = ui.util_transfTools_valuesExistent_lineEdit.text()
				_vReplacement = ui.util_transfTools_valuesReplacement_lineEdit.text()
				_tb = fromdataframe(df.last())

				_ = replace(_tb, _cSelect, _vExistent, _vReplacement)

				df.append(_.todataframe())
				ui.print(f'El valor "{_vExistent}" de la columna "{_cSelect}" ha sido reemplazado por "{_vReplacement}".')

		if _tTool == TRANSF_TOOLS[6]: # Completar valores
			_tb = fromdataframe(df.last())
			_ = None

			if ui.util_transfTools_orderLeft_radioButton.isChecked(): _ = fillleft(_tb)
			elif ui.util_transfTools_orderDown_radioButton.isChecked(): _ = filldown(_tb)
			else: _ = fillright(_tb)

			df.append(_.todataframe())
			ui.print(f'La tabla de datos ha sido rellenada.')
	ui.util_transfTools_apply_pushButton.clicked[bool].connect(_util_transfApplyAction)