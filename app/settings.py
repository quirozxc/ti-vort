# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from os import path

from matplotlib import cm

""" App DataBase it powered by SQLAlchemy """
# dialect+driver://username:password@host:port/database
# Ex:
#	for PostgreSQL
#		driver: psycopg2 (default)
#		'postgresql://scott:tiger@localhost/DATABASE_NAME'
#	for MySQL
#		driver: mysql-python (default) -> mysqlclient
#		'mysql+mysqlclient://scott:tiger@localhost/DATABASE_NAME'
#	for Oracle
#		driver: cx_oracle (default)
#		'oracle://scott:tiger@127.0.0.1:1521/DATABASE_NAME'
#	for Microsoft SQL Server 
#		driver: pyodbc (default)
#		'mssql://scott:tiger@hostname:port/DATABASE_NAME'
#	for SQLite
#		driver sqlite3 (default)
#		'sqlite:///PATH/FILE_NAME'
#
APP_DATABASE_URL = 'postgresql://postgres:postgres@localhost/vort_db'

APP_TEST_DATABASE_URL = 'postgresql://postgres:postgres@localhost/vtest'

STATIC_DIR = path.dirname(path.abspath(__file__)) +'/ui/static'

TEMPLATE_DIR = path.dirname(path.abspath(__file__)) +'/ui/template'

URL_SAMPLES = { 'PostgreSQL': 'postgresql://scott:tiger@localhost/DATABASE_NAME',
				'MySQL': 'mysql+mysqlclient://scott:tiger@localhost/DATABASE_NAME',
				'Oracle': 'oracle://scott:tiger@127.0.0.1:1521/DATABASE_NAME',
				'Microsoft SQL Server': 'mssql://scott:tiger@hostname:port/DATABASE_NAME',
				'SQLite': 'sqlite:///PATH/FILE_NAME',
				'Firebird': 'firebird://user:password@host:port/path/to/db[?key=value&key=value...]', }

COLORS_MAP = { 'Naranjas': cm.Oranges,
			   'Azules': cm.Blues,
			   'Verdes': cm.Greens,
			   'Purpuras': cm.Purples,
			   'Rd-Yl-Bu': cm.RdYlBu,
			   'Pu-Bu-Gn': cm.PuBuGn,
			   'Spectral': cm.Spectral,
			   'Accent': cm.Accent,
			   'Cool-Warm': cm.coolwarm,
			   'Primavera': cm.spring,
			   'Verano': cm.summer,
			   'Viridis': cm.viridis, }

COLORS = { 'Azul': 'blue',
		   'Marrón': 'brown',
		   'Coral': 'coral',
		   'Dorado': 'gold',
		   'Plateado': 'silver',
		   'Indigo': 'indigo',
		   'Amarillo': 'yellow',
		   'Verde': 'green',
		   'Naranja': 'orange',
		   'Lima': 'lime',
		   'Celeste': 'skyblue',
		   'Rojo': 'red',
		   'Beige': 'beige',
		   'Púrpura': 'purple',
		   'Negro': 'black',
		   'Navy': 'navy', 
		   'Cyan': 'cyan', 
		   'Azul Oscuro': 'darkblue',
		   'Verde Oscuro': 'darkgreen',
		   'Rojo Oscuro':'darkred', }

# *** DON'T change the order of this list. ***
TRANSF_TOOLS = [ 'Añadir columna',
				 'Convertir columna',
				 'Mover una columna',
				 'Cambiar nombre',
				 'Redondear valores',
				 'Cambiar un valor',
				 'Completar valores', ]

PLOTS = { 'Línea': 'line',
		  'Área': 'area',
		  'Barras Verticales': 'bar',
		  'Barras Horizontales': 'barh',
		  'Cotizaciones': 'box', }

DISPLAY_LAYOUTS = [ (-0.081, -0.090, 1.042, 1.050),   # Presentation
					(-0.037, -0.400, 1.036, 0.936),   # Data table
					(0.020, 0.020, 1.036, 0.985),	  # General plots
					(-0.075, -0.078, 1.036, 0.984), ] # Mining plots

# *** For Marplotlib.pyplot.contourf in Mining - Classifier Method ***
CONTOURF_CLASSIFICATION_MINING_PADDING = 0.1
CONTOURF_CLASSIFICATION_MINING_MESH_STEP_SIZE = 0.01

ABOUT_MESSAGE = '<p>La finalidad de esta investigación fue la construcción ' \
				'de una herramienta que permite extraer información de ' \
				'diferentes fuentes, transformarlos e incorporarlos ' \
				'genéricamente en un único almacén de datos (proceso ETL). ' \
				'Una solución que presenta adicionalmente soporte para ' \
				'archivos en formatos MS Excel así como formatos planos: ' \
				'csv, tsv y json y con características de visualización y ' \
				'la implementación de algoritmos de minería de datos, todo ' \
				'esto en el lenguaje de programación Python.<\p>' \
				'<p>Esta herramienta consigue respaldar información dispersada en un ' \
				'único repositorio de datos, lo que asiente en un almacenamiento ' \
				'centralizado, la visualización así como un análisis de los ' \
				'datos, con el fin de tomar decisiones acertadas en el momento preciso.<\p>' \
				'<p>Para esta investigación se aplicó la metodología Roadmap ' \
				'dividida en justificación de la investigación, planificación ' \
				'del proyecto, diseño de la persistencia de datos, construcción ' \
				'del sistema e implementación y despliegue de la herramienta.<\p>' \
				'<p>Este esquema de investigación resultó en un sistema de computación ' \
				'que aborda la aún hoy en día existente problemática de la ' \
				'integración de datos desde fuentes variantes. Para mantener ' \
				'un almacén de datos actualizado e implementar técnicas de ' \
				'inteligencia de negocios primero es importante que dentro de ' \
				'la infraestructura de datos de una organización se halle establecida ' \
				'una herramienta de procesos ETL.<\p>'