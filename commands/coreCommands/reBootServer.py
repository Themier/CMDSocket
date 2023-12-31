
'''
'''

import os, sys, time, socket
import constants
from . import CommandBase
from tools import ChoiceBox

reBootServer_id = 'reBootServer'
reBootServer_abbr = ['rbs']

def reBootServer(cmd, customAddr, link:socket.socket):
	'''
	'''
	link.send(constants.cmd_finish_words.encode('utf-8'))
	time.sleep(0.5)
	link.close()
	constants.server.close()
	print('服务器已关闭')
	#os.chdir(constants.prjPath)
	res = os.system('start cmd /C "cd {} && python server.py"'.format(constants.prjPath))
	if res!=0:
		print('服务器重启失败')
	else:
		sys.exit(res)


def genReBootServer(d:dict={})->dict:
	cmd={}
	cmd['cmdId'] = reBootServer_id
	while True:
		inp = ChoiceBox().getChoice('重启目标服务器?')
		if inp == ChoiceBox.cancelId:
			return None
		elif inp == ChoiceBox.confirmId:
			break


	return cmd


CommandBase(reBootServer_id, reBootServer, genReBootServer, abbr=reBootServer_abbr)

