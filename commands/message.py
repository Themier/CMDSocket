
'''
'''

import os, sys, time
import constants
from commands import CommandBase
from tools import ChoiceBox
from config import ConfigIOer

message_id = 'message'
message_abbr = ['msg']

latestMessageFromId = 'cmdArg_message_latestMessageFrom'
latestMessageContentId = 'cmdArg_message_latestContent'
defaultMessageFrom = 'anonymous'
defaultMessageContent = 'hello from anonymous'

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
	global message_id, latestMessageFromId, defaultMessageFrom, latestMessageContentId, defaultMessageContent
	cmd={}
	cmd['cmdId'] = message_id
	messageFrom = d.get('messageFrom', ConfigIOer().getSTDConfig(latestMessageFromId, defaultMessageFrom))
	message = d.get('message', ConfigIOer().getSTDConfig(latestMessageContentId, defaultMessageContent))
	while True:
		cb = ChoiceBox()
		cb.newChoice('messageFrom', desc=messageFrom)
		cb.newChoice('message', desc=message)
		inp = cb.getChoice()
		if inp == 'messageFrom':
			messageFrom = input('where from?\n')
		elif inp == 'message':
			message = input('new message:\n')
		elif inp == ChoiceBox.confirmId or inp == ChoiceBox.cancelId:
			break

	ConfigIOer().writeSTDConfig(latestMessageFromId, messageFrom)
	ConfigIOer().writeSTDConfig(latestMessageContentId, message)
	cmd['messageFrom'] = messageFrom
	cmd['message'] = message
	return cmd


CommandBase(message_id, message, genMessage, abbr=message_abbr)

