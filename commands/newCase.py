
import os
import constants
from commands import CommandBase
from commands.uploadFile import uploadFile, pathInHome
from tools import ChoiceBox
from tools import PathMaker
from tools import SingleFileChoicer

newCase_id = 'newCase'
newCase_latestCaseId = 'default'
newCase_latestInputFilePath = ''
newCase_latestProgramPath = ''
newCase_latestCaseDescription = 'no description'

caseFolder = r'lbmCase'
caseInputFileName = 'params.dat'
caseProgrameName = 'program.exe'
caseResultPathName = 'results'
caseDescFileName = 'desc.txt'

def newCase(cmd, customAddr, link):
    '''
    '''
    global caseFolder, caseInputFileName, caseProgrameName, caseResultPathName, caseDescFileName
    caseId = cmd.get('caseId','default')
    caseId = 'default' if caseId=='' else caseId
    casePath = os.path.join(constants.homePath, caseFolder, caseId)
    resultPath = os.path.join(casePath, caseResultPathName)

    newFileCMD = {'overLoad':True}
    newFileCMD.update(cmd)
    newFileCMD['fileFolder'] = casePath
    newFileCMD['fileName'] = cmd.get('inputFileName', caseInputFileName)
    newFileCMD['fileSize'] = cmd.get('inputFileSize', 0)
    newFileCMD['fileContent'] = cmd.get('inputFileContent', '')
    uploadFile(newFileCMD, customAddr, link)
    
    caseDesc = cmd.get('description', b'no description')
    if len(caseDesc) == 0:
        caseDesc = b'no description'
    newFileCMD['fileName'] = caseDescFileName
    newFileCMD['fileSize'] = len(caseDesc)
    newFileCMD['fileContent'] = caseDesc
    uploadFile(newFileCMD, customAddr, link)

    newFileCMD['fileName'] = cmd.get('inputFileName', caseProgrameName)
    newFileCMD['fileSize'] = cmd.get('programSize', 0)
    newFileCMD['fileContent'] = cmd.get('programContent')
    newFileCMD['contentMode'] = 'binary'
    uploadFile(newFileCMD, customAddr, link)

    if pathInHome(resultPath):
        PathMaker().make(resultPath)
    return

    
def genNewCase(d:dict={}):
    '''
    '''
    cmd = {'cmdId':newCase_id}
    cmd['caseId'] = d.get('caseId', newCase_latestCaseId)
    cmd['inputFilePath'] = d.get('inputFileContent', newCase_latestInputFilePath)
    cmd['programPath'] = d.get('programContent', newCase_latestProgramPath)
    cmd['description'] = d.get('description', newCase_latestCaseDescription)
    while True:
        cb = ChoiceBox()
        cb.newChoice('caseId', cmd['caseId'])
        cb.newChoice('inputFilePath', len(cmd['inputFilePath']))
        cb.newChoice('programPath', len(cmd['programPath']))
        cb.newChoice('description', cmd['description'])
        inp = cb.getChoice()
        if inp == 'caseId':
            cmd['caseId'] = input('new id: ')
        elif inp == 'inputFilePath':
            #import win32ui
            #dlg = win32ui.CreateFileDialog(2)
            ##dlg.SetOFNInitialDir('c:/')
            #dlg.DoModal()
            #filePath = dlg.GetPathName()
            filePath = SingleFileChoicer().getChoice(cmd['inputFilePath'])
            #fileName = os.path.basename(filePath)
            file = open(filePath, 'rb')
            fileContent = file.read()
            cmd['inputFileContent'] = fileContent
        elif inp == 'programPath':
            #import win32ui
            #dlg = win32ui.CreateFileDialog(2)
            ##dlg.SetOFNInitialDir('c:/')
            #dlg.DoModal()
            #filePath = dlg.GetPathName()
            filePath = SingleFileChoicer().getChoice(cmd['programPath'])
            #fileName = os.path.basename(filePath)
            file = open(filePath, 'rb')
            fileContent = file.read()
            cmd['programContent'] = fileContent
        elif inp == 'description':
            cmd['description'] = input('new description: ')
        elif inp == ChoiceBox.confirmId:
            newCase_latestCaseId = cmd['caseId']
            newCase_latestInputFilePath = cmd['inputFilePath']
            newCase_latestProgramPath = cmd['programPath']
            newCase_latestCaseDescription = cmd['description']

            filePath = cmd['inputFilePath']
            if os.path.isfile(filePath):
                cmd['inputFileName'] = os.path.basename(filePath)
                file = open(filePath, 'rb')
                cmd['inputFileContent'] = file.read()

            cmd['programSize'] = len(cmd['programContent'])
            cmd['inputFileSize'] = len(cmd['inputFileContent'])
            cmd['description'] = cmd['description'].encode('utf-8')
            return cmd


CommandBase(newCase_id, newCase, genNewCase)
