
import os
from constants import *
from commands import CommandBase

def makePath(path:str):
    if os.path.isdir(path):
        return True

    parpath = os.path.abspath(os.path.join(path, os.pardir))
    if not os.path.isdir(parpath):
        makePath(parpath)

    try:
        os.mkdir(path)
        return True
    except:
        return False


def pathInHome(path:str):
    absHome = os.path.abspath(homePath)
    absPath = os.path.abspath(path)
    n = len(absHome)
    return absPath[:n] == absHome[:n]


def newFile(cmd, customAddr, link):
    '''
    '''
    fileFolder = cmd.get('fileFolder','./')
    fileName = cmd.get('fileName','unamed')
    fileSize = cmd.get('fileSize', 0)
    recvFileSize = len(cmd['fileContent'])
    contentMode = cmd.get('contentMode', 'text')
    overLoad = cmd.get('overLoad', False)
    completePercent = recvFileSize * 100.0 / fileSize
    complete = (fileSize == recvFileSize)

    if (not pathInHome(os.path.join(fileFolder, fileName))) or (not pathInHome(fileFolder)):
        reply='失败：路径超出了服务器'
        print(error)
        link.send(error.encode('utf-8'))
        return

    makePath(fileFolder)

    if not overLoad:
        while os.path.isfile(os.path.join(fileFolder, fileName)):
            fileName = 'new_'+fileName

    filePath = os.path.join(fileFolder, fileName)

    file = None
    if contentMode == 'text':
        file = open(filePath, 'w')
    else:
        file = open(filePath, 'wb')
    file.write(cmd['fileContent'])
    file.close()

    reply = '文件 {} 接收完成，完整度 {} / {} : {}%'.format(fileName, recvFileSize, fileSize, completePercent)
    print(reply)
    link.send(reply.encode('utf-8'))

    return


CommandBase('newFile', newFile)

