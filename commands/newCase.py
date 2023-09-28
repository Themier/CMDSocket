
import os
import constants
from commands import CommandBase
from commands.uploadFile import uploadFile, makePath, pathInHome

def newCase(cmd, customAddr, link):
    '''
    '''
    caseId = cmd.get('caseId','default')
    caseId = 'default' if caseId=='' else caseId
    casePath = os.path.join(constants.caseFolder, caseId)
    resultPath = os.path.join(casePath, constants.caseResultPathName)
    descFilePath = os.path.join(casePath, constants.caseDescFileName)
    
    if not pathInHome(casePath):
        link.send('失败：路径超出了服务器'.encode('utf-8'))
        return

    newFileCMD = {}
    newFileCMD.update(cmd)
    newFileCMD['fileFolder'] = casePath
    newFileCMD['fileName'] = constants.caseInputFileName
    newFileCMD['fileSize'] = cmd.get('inputFileSize', 0)
    newFileCMD['fileContent'] = cmd.get('inputFileContent')
    newFile(newFileCMD, customAddr, link)
    
    caseDesc = cmd.get('description', 'no description')
    caseDesc = caseDesc if caseDesc!='' else 'no description'
    newFileCMD['fileName'] = constants.caseDescFileName
    newFileCMD['fileSize'] = len(caseDesc)
    newFileCMD['fileContent'] = caseDesc
    newFile(newFileCMD, customAddr, link)

    newFileCMD['fileName'] = constants.caseProgrameName
    newFileCMD['fileSize'] = cmd.get('programSize', 0)
    newFileCMD['fileContent'] = cmd.get('programContent')
    newFileCMD['contentMode'] = 'binary'
    newFile(newFileCMD, customAddr, link)

    makePath(resultPath)
    return


CommandBase('newCase', newCase, None)
