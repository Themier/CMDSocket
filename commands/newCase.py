
import os
import constants
from commands import CommandBase
from commands.uploadFile import uploadFile, makePath, pathInHome

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
    caseDesc = caseDesc if caseDesc!='' else 'no description'
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
        inp = input('\n[i]caseId {}\n[if]inputFileSize {}\n[p]programSize {}\n[d]description {}\n[cf] confirm\n'.format(
            cmd['caseId'], len(cmd['inputFileContent']), len(cmd['programContent']), cmd['description']))
        if inp == 'i':
            cmd['caseId'] = input('new id')
        elif inp == 'if':
            import win32ui
            dlg = win32ui.CreateFileDialog(2)
            #dlg.SetOFNInitialDir('c:/')
            dlg.DoModal()
            filePath = dlg.GetPathName()
            fileName = os.path.basename(filePath)
            file = open(filePath, 'rb')
            fileContent = file.read()
            cmd['inputFileContent'] = fileContent
        elif inp == 'p':
            import win32ui
            dlg = win32ui.CreateFileDialog(2)
            #dlg.SetOFNInitialDir('c:/')
            dlg.DoModal()
            filePath = dlg.GetPathName()
            fileName = os.path.basename(filePath)
            file = open(filePath, 'rb')
            fileContent = file.read()
            cmd['programContent'] = fileContent
        elif inp == 'd':
            cmd['description'] = input('new description')
        elif inp =='confirm':
            cmd['programSize'] = len(cmd['programContent'])
            cmd['inputFileSize'] = len(cmd['inputFileContent'])
            cmd['description'] = cmd['description'].encode('utf-8')
            return cmd


CommandBase(newCase_id, newCase, genNewCase)
