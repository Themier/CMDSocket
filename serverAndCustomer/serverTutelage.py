
from socket import socket
from verify.verify import Verify
from commands import *

import constants

class ServerTutelage():
    '''
    '''


    def __init__(self, server:socket):
        self.server = server

        return


    def __ParseCMD(self, cmd, customAddr, link):
        '''
        '''
        cmdId = cmd.get('cmdId')
        print('指令 : {}'.format(cmdId))
        if cmdId in CommandBase.inses:
            CommandBase.inses[cmdId].Action(cmd, customAddr, link)
        else:
            print('这啥玩意？？')

        return


    def __GetCMD(self, cmd, customAddr, link):
        '''
        '''
        username = cmd.get('username', '')
        password = cmd.get('password', '')
        if Verify.Verify(username, password):
            print('用户 {} 身份验证通过'.format(username))
            self.__ParseCMD(cmd, customAddr, link)
        else:
            print('身份验证失败：{} - {}'.format(username, password))


    def Tutelage(self):
        '''
        '''
        while True:
            print('\n监听中 ...\n')

            link, customAddr = self.server.accept()
            print('来自 {} 的访问, 等待指令...'.format(customAddr))

            try:
                cmdList = link.recv(constants.cmdMaxSize).decode('utf-8')
                bracePosition = cmdList.find('[')
                dotPosition = cmdList.find(',')
                while bracePosition  < 0 or dotPosition < 0:
                    cmdList += link.recv(constants.cmdMaxSize).decode('utf-8')
                    bracePosition = cmdList.find('[')
                    dotPosition = cmdList.find(',')
                cmdSize = cmdList[bracePosition+1: dotPosition]
                cmdSize = int(cmdSize)

                while len(cmdList) < cmdSize:
                    cmdList += link.recv(constants.cmdMaxSize).decode('utf-8')
                if len(cmdList) > cmdSize:
                    cmdList = cmdList[:cmdSize]

                print('收到指令, 长度 {}'.format(len(cmdList)))
                cmdList = eval(cmdList)

                cmd = cmdList[1]
                self.__GetCMD(cmd, customAddr, link)
            except Exception as result:
                repl = '发生错误 {}'.format(result)
                print(repl)
                link.send(repl.encode('utf-8'))

            link.send('cmd_finish'.encode('utf-8'))
            link.close()
