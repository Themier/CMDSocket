
from socket import socket
from verify.verify import Verify
from commands import *

import constants

class ServerTutelage():
    '''
    '''

    ins = None

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
            repl = '身份验证失败：{}'.format(username)
            print(repl)
            link.send(repl.encode('utf-8'))


    def Tutelage(self):
        '''
        '''
        while True:
            print('\n等待指令中 ...\n')

            link, customAddr = self.server.accept()
            print('来自 {} 的访问, 接收指令...'.format(customAddr))

            try:
                cmdBufferFile = open('cmdBuffer', 'w')
                cumulantEmptyRecvTimes = 0
                cmdSize = None
                #cmdStream=''
                while cmdSize == None:
                    recvStream = link.recv(constants.maxSizePerRecv).decode('utf-8')
                    if len(recvStream) == 0:
                        cumulantEmptyRecvTimes += 1
                        if cumulantEmptyRecvTimes > constants.maxTryRecvTimes:
                            raise Exception('网络传输异常或命令格式错误')
                        continue
                    #cmdStream += recvStream
                    cmdBufferFile.write(recvStream)
                    cmdBufferFile.flush()
                    cmdBufferFileRead = open('cmdBuffer', 'r')
                    cmdSize = constants.ParseCommandStreamSize(cmdBufferFileRead.read())
                    cmdBufferFileRead.close()
                print('收到指令, 长度 {}\n正在接收 ......'.format(cmdSize))
                cmdBufferFileRead = open('cmdBuffer', 'r')
                nowSize = constants.CountCommandStreamRealSize(cmdBufferFileRead.read())
                cmdBufferFileRead.close()

                while nowSize < cmdSize:
                    recvStream = link.recv(constants.maxSizePerRecv).decode('utf-8')
                    if len(recvStream) == 0:
                        cumulantEmptyRecvTimes += 1
                        if cumulantEmptyRecvTimes > constants.maxTryRecvTimes:
                            raise Exception('网络传输异常或命令流终止符错误')
                        continue
                    #cmdStream += recvStream
                    nowSize += len(recvStream)
                    cmdBufferFile.write(recvStream)
                    #nowLen = constants.CountCommandStreamRealSize(cmdStream)
                    print('接收进度 {:03.3f} %'.format(100.0*nowSize/cmdSize), end='\r')

                try:
                    cmdBufferFile.flush()
                    cmdBufferFileRead = open('cmdBuffer', 'r')
                    cmd = constants.ParseCommandStream(cmdBufferFileRead.read())
                    cmdBufferFileRead.close()
                    cmdBufferFile.close()
                except Exception as error:
                    raise Exception("命令流解析失败，{}".format(error))

                if not isinstance(cmd, constants.cmd_type):
                    raise Exception("命令非法，合法的命令应当是 {}".format(constants.cmd_type))

                self.__GetCMD(cmd, customAddr, link)

            except Exception as result:
                repl = '发生错误 {}'.format(result)
                print(repl)
                link.send(repl.encode('utf-8'))

            link.send(constants.cmd_finish_words.encode('utf-8'))
            link.close()
