# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from PyQt5.QtWidgets import QFileDialog

from ..core.visualization import draw_figure

from ..settings import COLORS_MAP, PLOTS, DISPLAY_LAYOUTS

def _build(dbo, df, ui):
	_buildBoxs(dbo, df, ui)
	_connectActions(dbo, df, ui)

def _buildBoxs(dbo, df, ui):
	_colors_map = ['Seleccione'] +list(COLORS_MAP.keys())
	ui.util_visualDesing_colorsSelection_comboBox.addItems(_colors_map)

	_plots = ['Seleccione'] +list(PLOTS.keys())
	ui.util_visualDesing_plotSelection_comboBox.addItems(_plots)

	def _build_utilVisualDesingBox(option_selected):
		_active = True
		if option_selected == 'Cotizaciones':
			_active = False
		ui.util_visualDesing_contrast_label.setEnabled(_active)
		ui.util_visualDesing_contrast_horizontalSlider.setEnabled(_active)
		if ui.util_visualDesing_includePoints_radioButton.isChecked():
			ui.util_visualDesing_includePoints_radioButton.click()
		ui.util_visualDesing_includePoints_radioButton.setEnabled(_active)
	ui.util_visualDesing_plotSelection_comboBox.activated[str].connect(_build_utilVisualDesingBox)

def _connectActions(dbo, df, ui):
	def _util_visualClearAction():
		ui.util_visualDesing_plotSelection_comboBox.setCurrentText('Seleccione')
		ui.util_visualDesing_colorsSelection_comboBox.setCurrentText('Seleccione')
		ui.util_visualDesing_contrast_horizontalSlider.setValue(5)
		if ui.util_visualDesing_stacked_checkBox.isChecked():
			ui.util_visualDesing_stacked_checkBox.click()
		ui.util_visualDesing_includeX_lineEdit.setText(str())
		ui.util_visualDesing_includeY_lineEdit.setText(str())
		if ui.util_visualDesing_includePoints_radioButton.isChecked():
			ui.util_visualDesing_includePoints_radioButton.click()
		if ui.util_visualDesing_includeGrid_radioButton.isChecked():
			ui.util_visualDesing_includeGrid_radioButton.click()
		if ui.util_visualDesing_includeLegend_radioButton.isChecked():
			ui.util_visualDesing_includeLegend_radioButton.click()
	ui.util_visualDesing_clear_pushButton.clicked[bool].connect(_util_visualClearAction)

	def _util_visualExportAction():
		_fileName, _ = QFileDialog.getSaveFileName(ui.vort_centralWidget,
			filter = 'Extensión .png (*.png);;' \
					 'Extensión .pdf (*.pdf);;' \
					 'Extensión .ps (*.ps);;' \
					 'Extensión .eps (*.eps);;' \
					 'Extensión .svg (*.svg)')
		if _fileName:
			ui.display_plot.figure.savefig(_fileName)
			ui.print(f'Gráfica guardada en {_fileName}')
	ui.util_visualDesing_export_pushButton.clicked[bool].connect(_util_visualExportAction)

	def _util_visualApplyAction():
		if not ui.util_visualDesing_plotSelection_comboBox.currentText() == 'Seleccione':
			ui.display_plot.figure.clear()
			_ax = ui.display_plot.figure.subplots()
			ui.display_plot.figure.tight_layout(rect = DISPLAY_LAYOUTS[2])

			_ = draw_figure(df, _ax,
				kind 	= ui.util_visualDesing_plotSelection_comboBox.currentText(),
				color 	= ui.util_visualDesing_colorsSelection_comboBox.currentText(),
				alpha 	= ui.util_visualDesing_contrast_horizontalSlider.value() / 10,
				stacked = ui.util_visualDesing_stacked_checkBox.isChecked(),
				point 	= ui.util_visualDesing_includePoints_radioButton.isChecked(),
				grid 	= ui.util_visualDesing_includeGrid_radioButton.isChecked(),
				legend  = ui.util_visualDesing_includeLegend_radioButton.isChecked())

			_ax.set_title(ui.util_visualDesing_plotSelection_comboBox.currentText())
			_ax.set_xlabel(ui.util_visualDesing_includeX_lineEdit.text())
			_ax.set_ylabel(ui.util_visualDesing_includeY_lineEdit.text())

			if not _:
				ui.display_plot.draw()
				ui.print('Última tabla de datos graficada ' \
					f'con "{ui.util_visualDesing_plotSelection_comboBox.currentText()}".')
			else: ui.print(f'Error de tipo "{type(_).__name__}" al intentar construir la gráfica.')
	ui.util_visualDesing_apply_pushButton.clicked[bool].connect(_util_visualApplyAction)