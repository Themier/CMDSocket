
'''
'''

import os, sys, time
import constants
from commands import CommandBase
from tools import ChoiceBox

message_id = 'message'

def message(cmd, customAddr, link):
	'''
	'''
	messageFrom = cmd.get('messageFrom', 'anonymous')
	message = cmd.get('message', 'default message')
	print("get message from {} {} :\n{}".format(messageFrom, customAddr, message))
	reply = 'messageGet'
	link.send(reply.encode('utf-8'))
	return


def genMessage(d:dict={})->dict:
	cmd={}
	cmd['cmdId'] = message_id
	messageFrom = d.get('messageFrom', 'anonymous')
	message = d.get('message', 'default message')
	while True:
		cb = ChoiceBox()
		cb.newChoice('messageFrom', messageFrom)
		cb.newChoice('message', message)
		inp = cb.getChoice()
		if inp == 'messageFrom':
			messageFrom = input('where from?\n')
		elif inp == 'message':
			message = input('new message:\n')
		elif inp == ChoiceBox.confirmId or inp == ChoiceBox.cancelId:
			break
	cmd['messageFrom'] = messageFrom
	cmd['message'] = message

	return cmd


CommandBase(message_id, message, genMessage)

