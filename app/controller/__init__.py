# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from ..core import _DataFrame

from .process import _build as process_
from .extraction import _build as extraction_
from .transformation import _build as transformation_
from .integration import _build as integration_
from .visualization import _build as visualization_
from .mining import _build as mining_
from .complement import _build as complement_

def play_artisan(dbo, ui):
	df = _DataFrame()

	modules = [ process_,
				extraction_,
				transformation_,
				integration_,
				visualization_,
				mining_,
				complement_, ]
	for module in modules:
		module(dbo, df, ui)

	ui.print('La aplicación está lista para usar. ' \
		'Para información adicional presione "Acerca de ..."')