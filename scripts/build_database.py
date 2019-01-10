# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

import traceback

from colorama import init, Fore, Style

from app.model import connect_database

def build_database():
	init() # Init Colorama
	GREEN = Fore.GREEN; RED = Fore.RED; BRIGHT = Style.BRIGHT; RESET = Style.RESET_ALL
	print('\nDatabase for VORT')
	print(f'Making it... ', end = '')
	
	try:
		dbo = connect_database()
		dbo.create_()
	except Exception as e:
		print(f'{RED}{BRIGHT}Error', '\n\n', e, '\n')
		traceback.print_exc()
	else:
		print(f'{GREEN}{BRIGHT}Done')
	finally:
		print(f'{RESET}', end = '')
		dbo.session.close()

if __name__ == '__main__':
	build_database()