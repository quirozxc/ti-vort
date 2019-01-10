# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

import traceback

from colorama import init, Fore, Style

from .ui import make_ui
from .model import connect_database
from .controller import play_artisan

def vort(argv):
	init() # Init Colorama
	GREEN = Fore.GREEN; RED = Fore.RED; BRIGHT = Style.BRIGHT; RESET = Style.RESET_ALL
	try:
		print('\nVisualization of Object-Relational Transformed')
		print(f'\nMaking App\'s base... ', end = '')
		app, window, ui = make_ui(argv)
		print(f'{GREEN}{BRIGHT}Done{RESET}')
		
		print(f'Connecting DB... ', end = '')
		dbo = connect_database()
		print(f'{GREEN}{BRIGHT}Done{RESET}')
		
		print(f'Packing UI... ', end = '')
		play_artisan(dbo, ui)
		print(f'{GREEN}{BRIGHT}Done{RESET}', end = '\n\n')
		
		def _closeSafety(event):
			print(f'\nDesconnecting DB... ', end = '')
			dbo.session.close()
			print(f'{GREEN}{BRIGHT}Done')
			event.accept()
		window.closeEvent = _closeSafety
		ui.closeEvent = window.closeEvent
		
	except Exception as e:
		print(f'{RED}{BRIGHT}Error', '\n\n', e, '\n')
		traceback.print_exc()
	else:
		window.show()
		app.exec_()
	finally:
		print(f'{RESET}', end = '')
		exit()