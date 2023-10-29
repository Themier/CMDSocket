
import socket, getpass, time
from commands import CommandBase
import constants
from tools import ChoiceBox
from config import ConfigIOer

setUser_id = '*setUser'
setUser_abbr = '*su'

def setUser(cmd, customAddr, link:socket.socket):
    ConfigIOer.writeSTDConfig(constants.latestUsernameConfigId, cmd.get('username'))
    ConfigIOer.writeSTDConfig(constants.latestPasswordConfigId, cmd.get('password'))
    return


def genSetUser(d:dict={}):
    global setUser_id
    cmd = {}
    cmd['cmdId'] = setUser_id

    username = d.get('username', ConfigIOer.getSTDConfig(constants.latestUsernameConfigId))
    password = d.get('password', ConfigIOer.getSTDConfig(constants.latestPasswordConfigId))
    
    cb = ChoiceBox()
    while True:
        cb.newChoice('username', desc=username)
        cb.newChoice('password')
        cb.newChoice('show password')
        inp = cb.getChoice()
        if inp == 'username':
            username = input('input username: ')
        elif inp == 'password':
            password = getpass.getpass('input password: ')
        elif inp == 'show password':
            print(password, end='\r')
            time.sleep(1.0)
            for i in range(len(password)):
                print('*', end='')
            print()
        elif inp == ChoiceBox.confirmId:
            break
        elif inp == ChoiceBox.cancelId:
            return None

    cmd['username'] = username
    cmd['password'] = password
    return cmd


CommandBase(setUser_id, setUser, genSetUser, abbr=setUser_abbr)
