
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
	print("从 {} ({}) 收到了消息 :\n{}".format(messageFrom, customAddr, message))
	reply = '消息已接收'
	link.send(reply.encode('utf-8'))
	return


def genMessage(d:dict={})->dict:
	global message_id, latestMessageFromId, defaultMessageFrom, latestMessageContentId, defaultMessageContent
	cmd={}
	cmd['cmdId'] = message_id
	messageFrom = d.get('签名', ConfigIOer().getSTDConfig(latestMessageFromId, defaultMessageFrom))
	message = d.get('消息', ConfigIOer().getSTDConfig(latestMessageContentId, defaultMessageContent))
	while True:
		cb = ChoiceBox()
		cb.newChoice('签名', desc=messageFrom)
		cb.newChoice('消息内容', desc=message)
		inp = cb.getChoice()
		if inp == '签名':
			messageFrom = input('输入签名?\n')
		elif inp == '消息内容':
			message = input('输入内容:\n')
		elif inp == ChoiceBox.cancelId:
			return None
		elif inp == ChoiceBox.confirmId:
			break

	ConfigIOer().writeSTDConfig(latestMessageFromId, messageFrom)
	ConfigIOer().writeSTDConfig(latestMessageContentId, message)
	cmd['messageFrom'] = messageFrom
	cmd['message'] = message
	return cmd


CommandBase(message_id, message, genMessage, abbr=message_abbr)

