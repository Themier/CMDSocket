
import socket
import sys
import constants
from commands import CommandBase

userImformation = {
    'username':'tower'
    ,'password':'tower^10'
    }

customer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    inp = input('指令 Id：')

    if inp in CommandBase.inses:
        cmd = CommandBase.inses[inp].Gen()
        if not cmd == None:
            customer.connect(('192.168.41.85', 8000))
            cmd.update(userImformation)
            cmd = repr(cmd)
            print(f'指令长度 {len(cmd)}')
            customer.send(cmd.encode('utf-8'))
            while True:
                reply = customer.recv(constants.cmdMaxSize).decode('utf-8')
                print(reply)
                if reply[-(len(constants.cmd_finish_words)):] == constants.cmd_finish_words:
                    customer.close()
                    break
    else:
        print('可用的指令：{}'.format(CommandBase.inses.keys()))

