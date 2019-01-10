# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

import sys, unittest
from optparse import OptionParser, OptionGroup

import warnings
warnings.filterwarnings('ignore')

def main():
	parser = OptionParser(description = 'Visualization of Object-Relational Transformed')
	parser.add_option(
		'-r', '--run',
		action = 'store_true',
		help = 'Ejecuta la aplicación')

	g = OptionGroup(parser, title = 'Opciones previas')
	g.add_option(
		'-b', '--build_db',
		action = 'store_true',
		help = 'Construye la DB de la aplicación')
	parser.add_option_group(g)
	
	g = OptionGroup(parser, title = 'Opciones de testing')
	g.add_option(
		'-t', '--test',
		action = 'store_true',
		help = 'Ejecuta el conjunto de unittest de la aplicación')
	g.add_option(
		'-d', '--create_td',
		action = 'store_true',
		help = 'Crea los datos para el demo inicial')
	g.add_option(
		'-p', '--load_tp',
		action = 'store_true',
		help = 'Carga el proceso ETL para el demo inicial')

	g.add_option(
		'-a', '--create_airport_tb',
		action = 'store_true',
		help = 'Crea las tablas para el demo del aeropuerto de LA')
	g.add_option(
		'-l', '--load_airport_tp',
		action = 'store_true',
		help = 'Carga el proceso para el demo del aeropuerto de LA')
	parser.add_option_group(g)

	opts, args = parser.parse_args()

	if opts.run:
		from app import vort
		vort(sys.argv)

	if opts.test:
		from app.test import test_runner
		test_runner()

	if opts.build_db:
		from scripts.build_database import build_database
		build_database()
	if opts.create_td:
		from scripts._create_test_data import create_test_database
		create_test_database()
	if opts.load_tp:
		from scripts._load_test_processETL import load_etl_test
		load_etl_test()

	if opts.create_airport_tb:
		from scripts._create_airportLA_tables import create_airportLA_data
		create_airportLA_data()
	if opts.load_airport_tp:
		from scripts._load_query_airportLA_process import load_query_airportLA_process
		load_query_airportLA_process()

if __name__ == '__main__':
	if len(sys.argv) == 1:
		sys.argv.append('--help')
	main()