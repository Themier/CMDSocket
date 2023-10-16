
'''
'''

class ChoiceBox(dict):
	'''
	{
		'choice name' : 'choice description'
		, ...
	}
	'''

	confirmId = 'cf'
	confirmDesc = 'confirm'
	cancelId = 'cc'
	cancelDesc = 'cancel'

	def __init__(self, choiceMap:dict={}):
		super().__init__()
		self.update(choiceMap)

		return

	def newChoice(self, id, desc):
		'''
		'''
		self[id] = desc
		return


	def getChoice(self, title='', **d):
		'''
		'''
		addConfirm = d.get('addConfirm', True)
		addCancel = d.get('addCancel', True)
		choiceMap = {}
		choiceMap.update(self)
		if addConfirm:
			choiceMap.update({ChoiceBox.confirmId:ChoiceBox.confirmDesc})
		if addCancel:
			choiceMap.update({ChoiceBox.cancelId:ChoiceBox.cancelDesc})
		choices = list(map(lambda item:(item[0], item[1]), choiceMap.items()))
		str = '{}\n'.format(title)
		n = 1
		for item in choices:
			str += '[{}]{}: {}\n'.format(n, item[0], item[1])
			n+=1
		inp = ''
		while True:
			inp = input(str)
			try:
				inp = int(inp)
				if inp < len(choices)+1 and inp > 0:
					break
			except:
				pass

		return choices[inp-1][0]


if __name__ == '__main__':
	cb = ChoiceBox([('all', 'all'),('box', 'box'),('cylinder', 'cy'), ('cc', '???')])
	print(cb.getChoice())