
'''
'''
import os
from tools import ChoiceBox
from tools import DriverGeter
import constants

class SingleFileChoicer():
	'''
	'''

	def __init__(self):

		return


	def getChoice(self, path:str='')->str:
		if os.path.exists(path):
			path = os.path.abspath(path)
		if os.path.isfile(path):
			path = os.path.dirname(path)
		drivers = DriverGeter().GetAll()
		while True:
			if os.path.isfile(path):
				cb = ChoiceBox()
				c = cb.getChoice('{}'.format(path))
				if c == ChoiceBox.confirmId:
					return path
				elif c == ChoiceBox.cancelId:
					path = os.path.dirname(path)

			elif os.path.isdir(path):
				cb = ChoiceBox()
				cb.newChoice('..')
				allItems = os.listdir(path)
				for item in allItems:
					cb.newChoice(item)
				c = cb.getChoice('{}'.format(path), addConfirm=False, addCancel=False)
				if c == '..':
					if os.path.abspath(path) in drivers:
						path = ''
					else:
						path = os.path.dirname(path)
				elif c in allItems:
					path = os.path.join(path, c)

			else:
				cb = ChoiceBox()
				for item in drivers:
					cb.newChoice(item)
				c = cb.getChoice(addConfirm=False, addCancel=False)
				path = c


def singleTest():
	sfc = SingleFileChoicer()
	print(sfc.getChoice())
