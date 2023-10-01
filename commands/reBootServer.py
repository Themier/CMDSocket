
'''
'''

import os, sys, time
import constants
from commands import CommandBase

reBootServer_id = 'reBootServer'

def reBootServer(cmd, customAddr, link):
	'''
	'''
	path = os.path.join(constants.prjPath, 'server.py')
	link.send(constants.cmd_finish_words.encode('utf-8'))
	time.sleep(0.5)
	constants.server.close()
	os.system('python {}'.format(path))
	sys.exit(0)


def genReBootServer(d:dict={})->dict:
	cmd={}
	cmd['cmdId'] = reBootServer_id

	return cmd


CommandBase(reBootServer_id, reBootServer, genReBootServer)

