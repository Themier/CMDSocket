
import os
from constants import *
from commands import CommandBase
from commands.newFile import newFile, makePath, pathInHome

def newCase(cmd, customAddr, link):
    '''
    '''
    caseId = cmd.get('caseId','default')
    caseId = 'default' if caseId=='' else caseId
    casePath = os.path.join(caseFolder, caseId)
    resultPath = os.path.join(casePath, caseResultPathName)
    descFilePath = os.path.join(casePath, caseDescFileName)
    
    if not pathInHome(casePath):
        link.send('失败：路径超出了服务器'.encode('utf-8'))
        return

    newFileCMD = {}
    newFileCMD.update(cmd)
    newFileCMD['fileFolder'] = casePath
    newFileCMD['fileName'] = caseInputFileName
    newFileCMD['fileSize'] = cmd.get('inputFileSize', 0)
    newFileCMD['fileContent'] = cmd.get('inputFileContent')
    newFile(newFileCMD, customAddr, link)
    
    caseDesc = cmd.get('description', 'no description')
    caseDesc = caseDesc if caseDesc!='' else 'no description'
    newFileCMD['fileName'] = caseDescFileName
    newFileCMD['fileSize'] = len(caseDesc)
    newFileCMD['fileContent'] = caseDesc
    newFile(newFileCMD, customAddr, link)

    newFileCMD['fileName'] = caseProgrameName
    newFileCMD['fileSize'] = cmd.get('programSize', 0)
    newFileCMD['fileContent'] = cmd.get('programContent')
    newFileCMD['contentMode'] = 'binary'
    newFile(newFileCMD, customAddr, link)

    makePath(resultPath)
    
    #if not os.path.exists(caseFolder):
    #    os.mkdir(caseFolder)
    #if not os.path.exists(casePath):
    #    os.mkdir(casePath)
    #else:
    #    print('算例 {} 已存在, 进行覆盖'.format(caseId))
    #if not os.path.exists(resultPath):
    #    os.mkdir(resultPath)
    #print('接收新算例...\n目标路径: {}'.format(casePath))

    #f= open(descFilePath, 'w')
    #f.write(caseDesc)
    #f.close()

    #inputFileSize = cmd.get('inputFileSize', 0)
    #recvInputFileSize = len(cmd['inputFileContent'])
    #recvInputPercent = recvInputFileSize*100.0/inputFileSize
    #programSize = cmd.get('programSize', 0)
    #recvProgramSize = len(cmd['programContent'])
    #recvProgramPercent = recvProgramSize*100.0/programSize
    #inputFile = open(os.path.join(casePath, caseInputFileName), 'w')
    #inputFile.write(cmd['inputFileContent'])
    #inputFile.close()
    #program = open(os.path.join(casePath, caseProgrameName), 'wb')
    #program.write(cmd['programContent'])
    #program.close()
    #print('算例 {} 接收完成\n算例输入文件完整度 {}/{}: {}%\n算例程序完整度 {}/{}: {}%'.format( \
    #    caseId, recvInputFileSize, inputFileSize, recvInputPercent, recvProgramSize, programSize, recvProgramPercent))

    #if recvProgramPercent==100 and recvInputPercent == 100:
    #    link.send('ok'.encode('utf-8'))
    #else:
    #    link.send('文件不完整'.encode('utf-8'))
    return


CommandBase('newCase', newCase)
