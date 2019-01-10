# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from sklearn.linear_model import LinearRegression
from sklearn.svm import OneClassSVM
from sklearn.cluster import KMeans

from sklearn.preprocessing import StandardScaler

from sklearn.metrics.regression import r2_score, explained_variance_score, mean_squared_error, mean_absolute_error
from sklearn.metrics.classification import accuracy_score, f1_score, hamming_loss
from sklearn.metrics.cluster import entropy, silhouette_score, calinski_harabaz_score

from matplotlib.colors import ListedColormap, to_rgba
from numpy import meshgrid, arange, c_ , ones_like
from petl.util.vis import lookall as look

from ..settings import CONTOURF_CLASSIFICATION_MINING_PADDING
from ..settings import CONTOURF_CLASSIFICATION_MINING_MESH_STEP_SIZE

def analyze_regression(X, y, ax, cPoint, cSLine, metrics):
	try:
		_X = StandardScaler().fit_transform(X.values.reshape(-1, 1))
		_y = StandardScaler().fit_transform(y.values.reshape(-1, 1))

		_linear = LinearRegression().fit(_X, _y)
		_predict = _linear.predict(_X)
		ax.scatter(_X, _y, color = cPoint, marker = '.', alpha = .6, label = 'Dispersión')
		_pn, _px = _X.tolist().index(_X.min()), _X.tolist().index(_X.max())
		ax.plot((_X.min(), _X.max()), (_predict[_pn], _predict[_px]), color = cSLine, label = 'Recta de Regresión')

		ax.set_title('Regresión Lineal')
		ax.set_xticks(()); ax.set_yticks(())
		ax.legend()

		if metrics: _print_regressionMetrics(_linear, _X, _y, _predict)
	except Exception as e:
		return e

def analyze_classification(X, y, ax, cContourf, cInlier, cOutlier, gamma, metrics):
	try:
		_X = StandardScaler().fit_transform(X.values.reshape(-1, 1))
		_y = StandardScaler().fit_transform(y.values.reshape(-1, 1))

		_padding = CONTOURF_CLASSIFICATION_MINING_PADDING
		_mesh_sted_size = CONTOURF_CLASSIFICATION_MINING_MESH_STEP_SIZE
		_X_min, _X_max = _X.min() - _padding, _X.max() + _padding
		_y_min, _y_max = _y.min() - _padding, _y.max() + _padding
		_mapx, _mapy = meshgrid(arange(_X_min, _X_max, _mesh_sted_size),
			arange(_y_min, _y_max, _mesh_sted_size))

		if gamma == 0: gamma = 'auto'

		_classifier = OneClassSVM(kernel = 'rbf', gamma = gamma,
			random_state = 0).fit(c_[_X, _y])

		_Z = _classifier.decision_function(c_[_mapx.ravel(), _mapy.ravel()])
		_predict = _classifier.predict(c_[_X, _y])

		ax.contourf(_mapx, _mapy, _Z.reshape(_mapx.shape), cmap = cContourf, alpha = .7)
		_sub_XIn, _sub_XOut = list(), list()
		_sub_yIn, _sub_yOut = list(), list()
		for i in range(_predict.size):
			if _predict[i] == 1:
				_sub_XIn.append(_X[i]); _sub_yIn.append(_y[i])
			else:
				_sub_XOut.append(_X[i]); _sub_yOut.append(_y[i])
		ax.scatter(_sub_XIn, _sub_yIn, c = cInlier, marker = '.', alpha = .6, label = 'Inliers')
		ax.scatter(_sub_XOut, _sub_yOut, c = cOutlier, marker = '.', alpha = .6, label = 'OutLiers')

		ax.set_title('SVM')
		ax.set_xticks(()); ax.set_yticks(())
		ax.legend()

		if metrics: _print_classificationMetrics(_classifier, _predict)
	except Exception as e:
		return e

def analyze_clustering(X, y, ax, nClusters, cClusters, cCenters, metrics):
	try:
		_X = StandardScaler().fit_transform(X.values.reshape(-1, 1))
		_y = StandardScaler().fit_transform(y.values.reshape(-1, 1))

		_kMean = KMeans(n_clusters = nClusters, random_state = 0).fit(c_[_X, _y])

		ax.scatter(_X, _y, c = _kMean.labels_.reshape(-1, 1), cmap = cClusters, marker = '.', alpha = .6)
		for _center, _color in zip(_kMean.cluster_centers_,
			range(0, 256, int( 256/(_kMean.cluster_centers_.size /2) ))):
			if cCenters:
				ax.scatter(_center[0], _center[1], color = cCenters(_color +128),
					marker = 'x')
			else:
				ax.scatter(_center[0], _center[1], marker = 'x')

		ax.set_title('K-Means')
		ax.set_xticks(()); ax.set_yticks(())
		ax.legend(('Grupos', 'Centros'))
		if cClusters and cCenters:
			_leg = ax.get_legend()
			_leg.legendHandles[0].set_color(cClusters(192))
			_leg.legendHandles[1].set_color(cCenters(192))

		if metrics: _print_clusteringMetrics(_kMean, c_[_X, _y])
	except Exception as e:
		return e

def _print_regressionMetrics(_linear, _X, _y, _predict):
	metrics = [['Regresión Lineal', 'Datos obtenidos'],
			   ['Coeficiente', _linear.coef_],
			   ['Interceptación', _linear.intercept_],
			   ['Calificación (score)', _linear.score(_X, _y)],
			   ['Variance Score', r2_score(_y, _predict)],
			   ['Explained Variance Score', explained_variance_score(_y, _predict)],
			   ['Mean Squared Error', mean_squared_error(_y, _predict)],
			   ['Mean Absolute Error', mean_absolute_error(_y, _predict)], ]
	
	print('\nMinería de Datos - Regresión Lineal - <VORT>', '\n')
	print(_linear, '\n')
	print(look(metrics))

def _print_classificationMetrics(_classifier, _predict):
	metrics = [['Clasificación SVM', 'Datos obtenidos'],
			   ['Interceptación', _classifier.intercept_],
			   ['Accuracy Score', accuracy_score(ones_like(_predict), _predict)],
			   ['F1 Score', f1_score(ones_like(_predict), _predict)],
			   ['Hamming Loss', hamming_loss(ones_like(_predict), _predict)], ]

	print('\nMinería de Datos - Clasificación SVM - <VORT>', '\n')
	print(_classifier, '\n')
	print(look(metrics))

def _print_clusteringMetrics(_kMean, _X):
	metrics = [['Clustering K-Means', 'Datos obtenidos'],
			   ['Inercia', _kMean.inertia_],
			   ['Entropy', entropy(_kMean.labels_)],
			   ['Silhouette Score', silhouette_score(_X, _kMean.labels_, random_state = 0)],
			   ['Calinski-Harabaz Score', calinski_harabaz_score(_X, _kMean.labels_)], ]

	print('\nMinería de Datos - Clustering K-Means - <VORT>', '\n')
	print(_kMean, '\n')
	print(look(metrics))