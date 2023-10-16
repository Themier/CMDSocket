
import socket
import sys
import constants
from commands import CommandBase
from tools import ChoiceBox

userImformation = {
    'username':'tower'
    ,'password':'tower^10'
    }

cmds = list(CommandBase.inses.keys())
cb = ChoiceBox()
for item in cmds:
    cb.newChoice(item, '')

while True:
    inp = cb.getChoice('指令 Id：', addConfirm=False, addCancel=False)

    try:
        if inp in CommandBase.inses:
            cmd = CommandBase.inses[inp].Gen()
            if not cmd == None:
                customer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                customer.connect(('192.168.41.67', 8000))
                cmd.update(userImformation)
                cmdList = [0, cmd]
                while cmdList[0] != len(repr(cmdList)):
                    cmdList[0] = len(repr(cmdList))
                print(f'指令长度 {cmdList[0]}')
                cmdList = repr(cmdList)
                customer.send(cmdList.encode('utf-8'))
                while True:
                    reply = customer.recv(constants.cmdMaxSize).decode('utf-8')
                    print('服务器回复：{}'.format(reply))
                    if reply[-(len(constants.cmd_finish_words)):] == constants.cmd_finish_words:
                        customer.close()
                        break
        else:
            print('可用的指令：{}'.format(CommandBase.inses.keys()))

    except Exception as error:
        print('发生错误: \n{}'.format(error))

