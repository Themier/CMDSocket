
import socket, getpass, time
from . import CommandBase
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
        cb.newChoice('用户名', desc=username)
        cb.newChoice('重新输入密码')
        cb.newChoice('显示密码')
        inp = cb.getChoice()
        if inp == '用户名':
            username = input('输入用户名: ')
        elif inp == '重新输入密码':
            password = getpass.getpass('输入密码(无回显): ')
        elif inp == '显示密码':
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
