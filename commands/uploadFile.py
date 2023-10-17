
import os
import constants
from commands import CommandBase

uploadFile_id = 'uploadFile'

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
    absHome = os.path.abspath(constants.homePath)
    absPath = os.path.abspath(path)
    n = len(absHome)
    return absPath[:n] == absHome[:n]


def uploadFile(cmd, customAddr, link)->int:
    '''
    '''
    fileFolder = cmd.get('fileFolder','recvFiles')
    fileName = cmd.get('fileName','unamed')
    fileSize = cmd.get('fileSize', 0)
    recvFileSize = len(cmd['fileContent'])
    overLoad = cmd.get('overLoad', False)
    if fileSize != 0:
        completePercent = recvFileSize * 100.0 / fileSize
    else:
        completePercent = 100.0
    complete = (fileSize == recvFileSize)
    
    if not (pathInHome(os.path.join(fileFolder, fileName)) and pathInHome(fileFolder)):
        reply='文件传输失败：指定的路径超出了服务器权限 {}'.format(os.path.join(fileFolder, fileName))
        print(reply)
        link.send(reply.encode('utf-8'))
        return
    
    filePath = os.path.abspath(os.path.join(fileFolder, fileName))
    fileFolder = os.path.abspath(os.path.join(filePath, os.pardir))
    makePath(fileFolder)

    if not overLoad:
        while os.path.isfile(os.path.join(fileFolder, fileName)):
            fileName = 'new_'+fileName
            filePath = os.path.abspath(os.path.join(fileFolder, fileName))

    file = open(filePath, 'wb')
    file.write(cmd['fileContent'])
    file.close()

    reply = '文件 {} 接收完成，完整度 {} / {} : {}%'.format(fileName, recvFileSize, fileSize, completePercent)
    print(reply)
    link.send(reply.encode('utf-8'))

    return 0 if complete else 1


def genUploadFile(d:dict={})->dict:
    '''
    d:
        fileFolder: str 上传到服务器的哪个文件
        fileNameAndContent: list[fileName:str, fileContent:bstr] 文件名和内容
        filePath: str 本地文件路径, 在不指定 fileNameAndContent 时生效
        overLoad: bool 是否覆盖同名文件，如果为否，自动重命名
    '''
    cmd = {'cmdId':uploadFile_id}
    fileFolder = d.get('fileFolder', 'recvFiles')
    fileNameAndContent = d.get('fileNameAndContent', None)
    overLoad = d.get('overLoad', False)
    filePath = None
    fileName = None
    fileContent = None
    if fileNameAndContent == None:
        filePath = d.get('filePath', None)
        if filePath == None:
            #import win32ui
            #dlg = win32ui.CreateFileDialog(2)
            #dlg.SetOFNInitialDir('c:/')
            #dlg.DoModal()
            #filePath = dlg.GetPathName()
            filePath = input('文件路径：')
        if not os.path.isfile(filePath):
            print('找不到文件： {}'.format(filePath))
            return None
        fileName = os.path.basename(filePath)
        file = open(filePath, 'rb')
        fileContent = file.read()
    else:
        fileName = fileNameAndContent[0]
        fileContent = fileNameAndContent[1]
    fileSize = len(fileContent)
    cmd.update({'fileName':fileName, 'fileFolder':fileFolder, 'fileContent':fileContent, 'fileSize':fileSize, 'overLoad':overLoad})

    return cmd


CommandBase(uploadFile_id, uploadFile, genUploadFile)

