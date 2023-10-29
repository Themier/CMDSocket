
'''
'''
import typing
from tools import IterableToStr

class ChoiceBox(dict):
	'''
	{
		'choice id' : ['choice description', 'choice shortcut 1', 'choice shortcut 2', ...]
		, ...
	}

	shortCutDict{
		'choice shortcut' : 'choice id'
	}
	'''

	confirmId = 'confirm'
	confirmShortCut = ''
	confirmDesc = ''
	cancelId = 'cancel'
	cancelShortCut = 'cc'
	cancelDesc = ''

	def __init__(self):
		super().__init__()
		self.shortCutDict = {}

		return


	def newChoice(self, id, **d):
		'''
		'''
		desc = d.get('desc', '')
		abbr = d.get('abbr', None)
		self[id] = [desc]
		if isinstance(abbr, typing.Iterable) and not isinstance(abbr, str):
			for item in abbr:
				self[id].append(str(item))
				self.shortCutDict[str(item)] = id
		elif abbr != None:
			self[id].append(str(abbr))
			self.shortCutDict[str(abbr)] = id
		return


	def getChoice(self, title='', **d):
		'''
		'''
		choiceDict = {}
		srtCtDict = {}
		choiceDict.update(self)
		srtCtDict.update(self.shortCutDict)
		if d.get('addConfirm', True):
			choiceDict[ChoiceBox.confirmId] = [ChoiceBox.confirmDesc, ChoiceBox.confirmShortCut]
			srtCtDict[ChoiceBox.confirmShortCut] = ChoiceBox.confirmId
		if d.get('addCancel', True):
			choiceDict[ChoiceBox.cancelId] = [ChoiceBox.cancelDesc, ChoiceBox.cancelShortCut]
			srtCtDict[ChoiceBox.cancelShortCut] = ChoiceBox.cancelId

		n = 0
		msg = '{}\n'.format(title)
		for choice in choiceDict.items():
			id = choice[0]
			desc = choice[1][0]
			scs = [str(n)]
			for sci in range(1, len(choice[1])):
				scs.append(choice[1][sci])
			srtCtDict[str(n)] = id
			scs = [isc for isc in scs if srtCtDict[isc] == id]
			scsStr = IterableToStr.Convert(scs, sep='/', converter=str)
			msg+='[{}] \t{}: \t{}\n'.format(scsStr, id, desc)
			n+=1
			
		inp = input(msg)
		if inp in choiceDict:
			return inp
		elif inp in srtCtDict:
			return srtCtDict[inp]
		else:
			return None


def singleTest():
	while True:
		cb = ChoiceBox()
		cb.newChoice('new id', abbr='i')
		cb.newChoice('new desc', abbr='d')
		cb.newChoice('new abbr', abbr=['a', 'b'])
		cb.newChoice('new test', abbr='cf')
		print(cb.getChoice())