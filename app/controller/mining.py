# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from ..core.mining import analyze_regression, analyze_classification, analyze_clustering

from ..settings import COLORS_MAP, COLORS, DISPLAY_LAYOUTS

def _build(dbo, df, ui):
	_buildBoxs(dbo, df, ui)
	_connectActions(dbo, df, ui)

def _buildBoxs(dbo, df, ui):
	_colorsMap_uiObjects = [ ui.util_classification_colorsContourSelection_comboBox,
							 ui.util_clustering_colorsClusterSelection_comboBox,
							 ui.util_clustering_colorsCenterSelection_comboBox, ]
	_colors_map = ['Seleccione'] +list(COLORS_MAP.keys())
	for uiObject in _colorsMap_uiObjects:
		uiObject.addItems(_colors_map)

	_colors_uiObjects = [ ui.util_regression_colorsPointSelection_comboBox,
						  ui.util_regression_colorsStraightLineSelection_comboBox,
						  ui.util_classification_colorsInlierSelection_comboBox,
						  ui.util_classification_colorsOutlierSelection_comboBox, ]
	_colors = ['Seleccione'] +list(COLORS.keys())
	for uiObject in _colors_uiObjects:
		uiObject.addItems(_colors)

def _connectActions(dbo, df, ui):
	def _util_regressionClearAction():
		ui.util_regression_columnXSelection_comboBox.setCurrentText('Seleccione')
		ui.util_regression_columnYSelection_comboBox.setCurrentText('Seleccione')
		ui.util_regression_colorsPointSelection_comboBox.setCurrentText('Seleccione')
		ui.util_regression_colorsStraightLineSelection_comboBox.setCurrentText('Seleccione')
		if not ui.util_regression_includeMetrics_checkBox.isChecked():
			ui.util_regression_includeMetrics_checkBox.click()
	ui.util_regression_clear_pushButton.clicked[bool].connect(_util_regressionClearAction)

	def _util_regressionAnalyzeAction():
		if not ui.util_regression_columnXSelection_comboBox.currentText() == 'Seleccione' and \
			not ui.util_regression_columnYSelection_comboBox.currentText() == 'Seleccione':
			_X = df.last().get(ui.util_regression_columnXSelection_comboBox.currentText())
			_y = df.last().get(ui.util_regression_columnYSelection_comboBox.currentText())
			
			_cPoint = COLORS.get(ui.util_regression_colorsPointSelection_comboBox.currentText())
			_cSLine = COLORS.get(ui.util_regression_colorsStraightLineSelection_comboBox.currentText())
			
			_metrics = ui.util_regression_includeMetrics_checkBox.isChecked()
			
			if not _X.dtype == object and not _y.dtype == object:
				ui.print('Procesando...')
				ui.display_plot.figure.clear()
				_ax = ui.display_plot.figure.subplots()
				ui.display_plot.figure.tight_layout(rect = DISPLAY_LAYOUTS[3])
				
				
				_ = analyze_regression(_X, _y, _ax, _cPoint, _cSLine, _metrics)
				if not _:
					ui.display_plot.draw()
					ui.print('Aplicado el algoritmo de Regresión Lineal a columnas de la última tabla.')
				else: ui.print(f'Error de tipo "{type(_).__name__}" al intentar analizar los datos.')
			else:
				ui.print('No es posible realizar la minería ' \
					'usando Regresión con la configuración actual.')
		else:
			ui.print('No es posible realizar la minería ' \
				'usando Regresión con la configuración actual.')
	ui.util_regression_analyze_pushButton.clicked[bool].connect(_util_regressionAnalyzeAction)

	def _util_classificationClearAction():
		ui.util_classification_columnXSelection_comboBox.setCurrentText('Seleccione')
		ui.util_classification_columnYSelection_comboBox.setCurrentText('Seleccione')

		ui.util_classification_gamma_horizontalSlider.setValue(5)

		ui.util_classification_colorsContourSelection_comboBox.setCurrentText('Seleccione')
		ui.util_classification_colorsInlierSelection_comboBox.setCurrentText('Seleccione')
		ui.util_classification_colorsOutlierSelection_comboBox.setCurrentText('Seleccione')

		if not ui.util_classification_includeMetrics_checkBox.isChecked():
			ui.util_classification_includeMetrics_checkBox.click()
	ui.util_classification_clear_pushButton.clicked[bool].connect(_util_classificationClearAction)

	def _util_classificationAnalyzeAction():
		if not ui.util_classification_columnXSelection_comboBox.currentText() == 'Seleccione' and \
			not ui.util_classification_columnYSelection_comboBox.currentText() == 'Seleccione':
			_X = df.last().get(ui.util_classification_columnXSelection_comboBox.currentText())
			_y = df.last().get(ui.util_classification_columnYSelection_comboBox.currentText())
			
			_cContourf = COLORS_MAP.get(ui.util_classification_colorsContourSelection_comboBox.currentText())
			
			_cInlier = COLORS.get(ui.util_classification_colorsInlierSelection_comboBox.currentText())
			_cOutlier = COLORS.get(ui.util_classification_colorsOutlierSelection_comboBox.currentText())

			_gamma = ui.util_classification_gamma_horizontalSlider.value()
			
			_metrics = ui.util_classification_includeMetrics_checkBox.isChecked()
			
			if not _X.dtype == object and not _y.dtype == object and _cOutlier and _cInlier and _cOutlier:
				ui.print('Procesando...')
				ui.display_plot.figure.clear()
				_ax = ui.display_plot.figure.subplots()
				ui.display_plot.figure.tight_layout(rect = DISPLAY_LAYOUTS[3])

				_ = analyze_classification(_X, _y, _ax, _cContourf, _cInlier, _cOutlier, _gamma, _metrics)
				if not _:
					ui.display_plot.draw()
					ui.print('Aplicado el algoritmo SVM a columnas de la última tabla.')
				else: ui.print(f'Error de tipo "{type(_).__name__}" al intentar analizar los datos.')
			else: ui.print('No es posible realizar minería usando SVM con la configuración actual.')
		else: ui.print('No es posible realizar minería usando SVM con la configuración actual.')
	ui.util_classification_analyze_pushButton.clicked[bool].connect(_util_classificationAnalyzeAction)

	def _util_clusteringClearAction():
		ui.util_clustering_columnXSelection_comboBox.setCurrentText('Seleccione')
		ui.util_clustering_columnYSelection_comboBox.setCurrentText('Seleccione')
		
		ui.util_clustering_nClusters_spinBox.setValue(2)

		ui.util_clustering_colorsClusterSelection_comboBox.setCurrentText('Seleccione')
		ui.util_clustering_colorsCenterSelection_comboBox.setCurrentText('Seleccione')

		if not ui.util_clustering_includeMetrics_checkBox.isChecked():
			ui.util_clustering_includeMetrics_checkBox.click()
	ui.util_clustering_clear_pushButton.clicked[bool].connect(_util_clusteringClearAction)

	def _util_clusteringAnalyzeAction():
		if not ui.util_clustering_columnXSelection_comboBox.currentText() == 'Seleccione' and \
			not ui.util_clustering_columnYSelection_comboBox.currentText() == 'Seleccione':
			_X = df.last().get(ui.util_clustering_columnXSelection_comboBox.currentText())
			_y = df.last().get(ui.util_clustering_columnYSelection_comboBox.currentText())
			
			_nClusters = ui.util_clustering_nClusters_spinBox.value()
			
			_cClusters = COLORS_MAP.get(ui.util_clustering_colorsClusterSelection_comboBox.currentText())
			_cCenters = COLORS_MAP.get(ui.util_clustering_colorsCenterSelection_comboBox.currentText())

			_metrics = ui.util_clustering_includeMetrics_checkBox.isChecked()
			
			if not _X.dtype == object and not _y.dtype == object:
				ui.print('Procesando...')
				ui.display_plot.figure.clear()
				_ax = ui.display_plot.figure.subplots()
				ui.display_plot.figure.tight_layout(rect = DISPLAY_LAYOUTS[3])

				_ = analyze_clustering(_X, _y, _ax, _nClusters, _cClusters, _cCenters, _metrics)
				if not _:
					ui.display_plot.draw()
					ui.print('Aplicado el algoritmo K-Means a columnas de la última tabla.')
				else: ui.print(f'Error de tipo "{type(_).__name__}" al intentar analizar los datos.')
			else: ui.print('No es posible realizar minería usando K-Means con la configuración actual.')
		else: ui.print('No es posible realizar minería usando K-Means con la configuración actual.')
	ui.util_clustering_analyze_pushButton.clicked[bool].connect(_util_clusteringAnalyzeAction)
