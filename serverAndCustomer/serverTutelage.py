
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
            print('\n等待指令中 ...\n')

            link, customAddr = self.server.accept()
            print('来自 {} 的访问, 等待指令...'.format(customAddr))

            try:
                latestRecvSize = 0
                lenBeginFlag = len(constants.cmdStreamBeginFlag)
                lenEndFlag = len(constants.cmdStreamEndFlag)
                checkBegin = False
                cmdStream=''
                cumulantEmptyRecvTimes = 0
                while not checkBegin:
                    recvStream = link.recv(constants.maxSizePerRecv).decode('utf-8')
                    if len(recvStream) == 0:
                        cumulantEmptyRecvTimes += 1
                        if cumulantEmptyRecvTimes > constants.maxTryRecvTimes:
                            raise '网络传输异常'
                        continue
                    latestRecvSize = len(recvStream)
                    cmdStream += recvStream
                    if len(cmdStream) < lenBeginFlag:
                        continue
                    if cmdStream[:lenBeginFlag] == constants.cmdStreamBeginFlag:
                        checkBegin = True
                    else:
                        raise "命令流起始符错误"

                checkEnd = False
                indexEndFlag = cmdStream.find(constants.cmdStreamEndFlag)
                if indexEndFlag >= 0:
                    checkEnd = True
                cumulantEmptyRecvTimes = 0
                while not checkEnd:
                    recvStream = link.recv(constants.maxSizePerRecv).decode('utf-8')
                    if len(recvStream) == 0:
                        cumulantEmptyRecvTimes += 1
                        if cumulantEmptyRecvTimes > constants.maxTryRecvTimes:
                            raise '网络传输异常或命令流终止符错误'
                        continue
                    cmdStream += recvStream
                    indexEndFlag = cmdStream.find(constants.cmdStreamEndFlag)
                    if indexEndFlag >= 0:
                        checkEnd = True

                cmdStream = cmdStream[lenBeginFlag:indexEndFlag]
                smdSize = len(cmdStream)
                print('收到指令, 长度 {}'.format(smdSize))

                try:
                    cmd = constants.cmd_parser(cmdStream)
                except Exception as error:
                    raise "命令流解析失败，{}".format(error)

                if not isinstance(cmd, constants.cmd_type):
                    raise "命令非法，合法的命令应当是 {}".format(constants.cmd_type)

                self.__GetCMD(cmd, customAddr, link)

            except Exception as result:
                repl = '发生错误 {}'.format(result)
                print(repl)
                link.send(repl.encode('utf-8'))

            link.send('cmd_finish'.encode('utf-8'))
            link.close()
