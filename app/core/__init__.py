# -*- coding: utf-8 -*-
# Author: Carlos Quiroz

class _DataFrame(object):
	def __init__(self): self._df = list()
	def __repr__(self): return self._df.__repr__()

	def append(self, df): self._df.append(df)

	def last(self): return self._df[-1]

	def pop(self): return self._df.pop()

	def clear(self): self._df = list()

	def size(self): return len(self._df)
		
	def isEmpty(self):
		if self._df == list():
			return True
		return False
