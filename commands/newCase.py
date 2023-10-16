
import os
import constants
from commands import CommandBase
from commands.uploadFile import uploadFile, makePath, pathInHome
from tools import ChoiceBox

newCase_id = 'newCase'

def newCase(cmd, customAddr, link):
    '''
    '''
    caseId = cmd.get('caseId','default')
    caseId = 'default' if caseId=='' else caseId
    casePath = os.path.join(constants.caseFolder, caseId)
    resultPath = os.path.join(casePath, constants.caseResultPathName)
    descFilePath = os.path.join(casePath, constants.caseDescFileName)

    newFileCMD = {'overLoad':True}
    newFileCMD.update(cmd)
    newFileCMD['fileFolder'] = casePath
    newFileCMD['fileName'] = constants.caseInputFileName
    newFileCMD['fileSize'] = cmd.get('inputFileSize', 0)
    newFileCMD['fileContent'] = cmd.get('inputFileContent')
    uploadFile(newFileCMD, customAddr, link)
    
    caseDesc = cmd.get('description', 'no description')
    if len(caseDesc) == 0:
        caseDesc = 'no description' 
    caseDesc = caseDesc if caseDesc!='' else 'no description'
    caseDesc = caseDesc.encode('utf-8')
    newFileCMD['fileName'] = constants.caseDescFileName
    newFileCMD['fileSize'] = len(caseDesc)
    newFileCMD['fileContent'] = caseDesc
    uploadFile(newFileCMD, customAddr, link)

    newFileCMD['fileName'] = constants.caseProgrameName
    newFileCMD['fileSize'] = cmd.get('programSize', 0)
    newFileCMD['fileContent'] = cmd.get('programContent')
    newFileCMD['contentMode'] = 'binary'
    uploadFile(newFileCMD, customAddr, link)

    if pathInHome(resultPath):
        makePath(resultPath)
    return

    
def genNewCase(d:dict={}):
    '''
    '''
    cmd = {'cmdId':newCase_id}
    cmd['caseId'] = d.get('caseId', 'default')
    cmd['inputFileContent'] = d.get('inputFileContent', '')
    cmd['programContent'] = d.get('programContent', '')
    cmd['description'] = d.get('description', '')
    while True:
        cb = ChoiceBox()
        cb.newChoice('caseId', cmd['caseId'])
        cb.newChoice('inputFile', len(cmd['inputFileContent']))
        cb.newChoice('program', len(cmd['programContent']))
        cb.newChoice('description', cmd['description'])
        inp = cb.getChoice()
        if inp == 'caseId':
            cmd['caseId'] = input('new id')
        elif inp == 'inputFile':
            import win32ui
            dlg = win32ui.CreateFileDialog(2)
            #dlg.SetOFNInitialDir('c:/')
            dlg.DoModal()
            filePath = dlg.GetPathName()
            fileName = os.path.basename(filePath)
            file = open(filePath, 'rb')
            fileContent = file.read()
            cmd['inputFileContent'] = fileContent
        elif inp == 'program':
            import win32ui
            dlg = win32ui.CreateFileDialog(2)
            #dlg.SetOFNInitialDir('c:/')
            dlg.DoModal()
            filePath = dlg.GetPathName()
            fileName = os.path.basename(filePath)
            file = open(filePath, 'rb')
            fileContent = file.read()
            cmd['programContent'] = fileContent
        elif inp == 'description':
            cmd['description'] = input('new description')
        elif inp == ChoiceBox.confirmId:
            cmd['programSize'] = len(cmd['programContent'])
            cmd['inputFileSize'] = len(cmd['inputFileContent'])
            cmd['description'] = cmd['description'].encode('utf-8')
            return cmd


CommandBase(newCase_id, newCase, genNewCase)
