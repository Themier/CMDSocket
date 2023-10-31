
import os
import constants
from . import CommandBase
from tools import SingleFileChoicer
from tools import PathMaker
from tools import ChoiceBox
from tools import PathIncludeChecker
from config import ConfigIOer

uploadFile_id = 'uploadFile'
uploadFile_abbr = ['uf']
latestPathId = 'cmdArg_uploadFile_latestPath'
defaultFilePath = ''


def uploadFile(cmd, customAddr, link)->int:
    '''
    cmd:
        fileFolder: str 文件保存到该路径下
        fileName: str 文件名
        fileSize: str 原文件大小，用于判断文件传输是否完整
        fileContent: bytes 文件内容
        overLoad: bool 是否覆盖同名文件，如果为否，自动重命名
    '''
    fileFolder = cmd.get('fileFolder')
    fileName = cmd.get('fileName')
    fileSize = cmd.get('fileSize')
    recvFileSize = len(cmd['fileContent'])
    overLoad = cmd.get('overLoad', False)
    if fileSize != 0:
        completePercent = recvFileSize * 100.0 / fileSize
    else:
        reply='文件传输失败：文件大小为 0'
        print(reply)
        link.send(reply.encode('utf-8'))
        return
    complete = (fileSize == recvFileSize)
    
    if not (\
        PathIncludeChecker.IsInclude(constants.homePath, os.path.join(fileFolder, fileName)) \
        and PathIncludeChecker.IsInclude(constants.homePath, os.path.join(fileFolder)) \
        ):
        reply='文件传输失败：指定的路径超出了服务器权限 {}'.format(os.path.join(fileFolder, fileName))
        print(reply)
        link.send(reply.encode('utf-8'))
        return
    filePath = os.path.abspath(os.path.join(fileFolder, fileName))
    fileFolder = os.path.dirname(filePath)
    PathMaker().make(fileFolder)

    if not overLoad:
        while os.path.isfile(os.path.join(fileFolder, fileName)):
            fileName = 'new_'+fileName
            filePath = os.path.abspath(os.path.join(fileFolder, fileName))

    file = open(filePath, 'wb')
    file.write(cmd['fileContent'])
    file.close()

    reply = '文件 {} 接收完成，完整度 {} / {} : {}%\n'.format(fileName, recvFileSize, fileSize, completePercent)
    print(reply)
    link.send(reply.encode('utf-8'))

    return 0 if complete else 1


def genUploadFile(d:dict={})->dict:
    '''
    cmd:
        fileFolder: str 文件上传到服务器Home的该路径下
        filePath: str 本地文件所在的路径
        overLoad: bool 是否覆盖同名文件，如果为否，自动重命名
    '''
    global uploadFile_id, latestPathId, defaultFilePath
    cmd = {'cmdId':uploadFile_id}

    fileFolder = d.get('fileFolder', 'recvFiles')
    overLoad = d.get('overLoad', False)
    filePath = d.get('filePath', ConfigIOer.getSTDConfig(latestPathId, defaultFilePath))

    while True:
        cb = ChoiceBox()
        #file
        fileExists = 'exists' if os.path.isfile(filePath) else 'NOT exists'
        cb.newChoice('文件路径', desc='[{}]{}'.format(fileExists, filePath))
        inp = cb.getChoice()
        if inp == '文件路径':
            filePath = SingleFileChoicer().getChoice(filePath)
        elif inp == ChoiceBox.confirmId:
            ConfigIOer.writeSTDConfig(latestPathId, filePath)
            fileName = os.path.basename(filePath)
            file = open(filePath, 'rb')
            fileContent = file.read()
            file.close()
            fileSize = len(fileContent)
            break
        elif inp == ChoiceBox.cancelId:
            return None
        
    cmd.update({'fileName':fileName, 'fileFolder':fileFolder, 'fileContent':fileContent, 'fileSize':fileSize, 'overLoad':overLoad})
    return cmd


CommandBase(uploadFile_id, uploadFile, genUploadFile, abbr=uploadFile_abbr)

