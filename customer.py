
import socket
import sys
import constants
from commands import CommandBase

userImformation = {
    'username':'tower'
    ,'password':'tower^10'
    }


while True:
    inp = input('指令 Id：')

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
                print(reply)
                if reply[-(len(constants.cmd_finish_words)):] == constants.cmd_finish_words:
                    customer.close()
                    break
    else:
        print('可用的指令：{}'.format(CommandBase.inses.keys()))

