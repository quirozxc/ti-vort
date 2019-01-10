# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

from ..core.transformation import (addrownumbers, convert,
	movefield, rename, replace, fillleft, filldown, fillright)

from unittest import TestCase

def _tb():
	return [['foo', 'bar'],
			[ 'a' ,   1  ],
			[ 'b' ,   2  ]]

class TransformationTestCase(TestCase):
	def test_add_row_numbers(self):
		_t = addrownumbers(_tb())
		self.assertEquals([['row', 'foo', 'bar'],
		  				   [  1,    'a' ,   1  ],
						   [  2,    'b' ,   2  ]], _t.listoflists())

	def test_convert_format_table_column(self):
		_t = convert(_tb(), 'bar', float)
		self.assertEquals([['foo', 'bar'],
		  				   [ 'a' ,  1.0 ],
						   [ 'b' ,  2.0 ]], _t.listoflists())

	def test_movefield_table_column(self):
		_t = movefield(_tb(), 'bar', 0)
		self.assertEquals([['bar', 'foo'],
		  				   [  1  ,  'a' ],
						   [  2  ,  'b' ]], _t.listoflists())

	def test_rename_table_column(self):
		_t = rename(_tb(), 'foo', 'qui')
		self.assertEquals(('qui', 'bar'), _t.header())

	def test_replace_value_table_column(self):
		_t = replace(_tb(), 'foo', 'a', 'A')
		self.assertEquals([['foo', 'bar'],
		  				   [ 'A' ,   1  ],
						   [ 'b' ,   2  ]], _t.listoflists())

	def test_fill_left_table(self):
		_t = fillleft([['foo', 'bar'],
					   [ None,   1  ],
					   [ 'b' ,   2  ]])
		self.assertEquals([['foo', 'bar'],
		  				   [  1  ,   1  ],
						   [ 'b' ,   2  ]], _t.listoflists())

	def test_fill_down_table(self):
		_t = filldown([['foo', 'bar'],
					   [ 'a' ,   1  ],
					   [ 'b' ,  None]])
		self.assertEquals([['foo', 'bar'],
		  				   [ 'a' ,   1  ],
						   [ 'b' ,   1  ]], _t.listoflists())

	def test_fill_right_table(self):
		_t = fillright([['foo', 'bar'],
					   [ 'a' ,   1  ],
					   [ 'b' ,  None]])
		self.assertEquals([['foo', 'bar'],
		  				   [ 'a' ,   1  ],
						   [ 'b' ,  'b' ]], _t.listoflists())