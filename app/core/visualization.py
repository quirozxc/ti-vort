# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from matplotlib.cm import Greys_r

from ..settings import COLORS_MAP, PLOTS

def draw_figure(df, ax, **args):
	try:
		if not args.get('kind') == 'Cotizaciones':
			df.last().plot(
				ax 		 = ax,
				kind 	 = PLOTS.get(args.get('kind')),
				colormap = COLORS_MAP.get(args.get('color')),
				stacked  = args.get('stacked'),
				alpha 	 = args.get('alpha'),
				grid 	 = args.get('grid'),
				legend 	 = args.get('legend'))
		else:
			df.last().plot(
				ax 		 = ax,
				kind 	 = PLOTS.get(args.get('kind')),
				colormap = COLORS_MAP.get(args.get('color')),
				stacked  = args.get('stacked'),
				grid 	 = args.get('grid'),
				legend 	 = args.get('legend'))
		
		if args.get('point'):
			if args.get('stacked'):
				for column, color in zip(df.last().columns, range(0, 256, int(256/df.last().columns.size))):
					ax.scatter(
						x 	   = df.last().index,
						y 	   = df.last().cumsum(axis = 'columns')[column],
						marker = 'x',
						color  = Greys_r(color))
			else:
				for column, color in zip(df.last().columns, range(0, 256, int(256/df.last().columns.size))):
					ax.scatter(
						x 	   = df.last().index,
						y 	   = df.last()[column],
						marker = 'x',
						color  = Greys_r(color))
	except Exception as e:
		return e