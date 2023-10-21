
'''
'''
import os

class DriverGeter():
	'''
	'''

	def __init__(self):
		pass


	def GetAll(self):
		'''
		'''
		all = []
		for n in range(ord('a'), ord('z')+1):
			cn = chr(n)
			p = cn+":/"
			if os.path.exists(p):
				all.append(p)
		return all


def singleTest():
	print(DriverGeter().GetAll())
