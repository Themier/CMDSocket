
import os
import constants
from commands import CommandBase
from commands.uploadFile import uploadFile, pathInHome
from tools import ChoiceBox
from tools import PathMaker
from tools import SingleFileChoicer
from config import ConfigIOer

newCase_id = 'newCase'
newCase_abbr = ['nc']
caseFolder = r'lbmCase'
caseDescFileName = 'case_describe.txt'

latestCaseIdId = 'cmdArg_newCase_latestCaseId'
latestInputFilePathId = 'cmdArg_newCase_latestInputFilePath'
latestProgramPathId = 'cmdArg_newCase_latestProgramPath'
latestCaseOutputFolderId = 'cmdArg_newCase_latestCaseResultFolder'
latestCaseDescriptionId = 'cmdArg_newCase_latestCaseDescription'
defaultCaseId = 'default'
defaultInputFilePath = ''
defaultProgramPath = ''
defaultCaseOutputFolder = ''
defaultCaseDescription = 'no description'

def newCase(cmd, customAddr, link):
    '''
    '''
    global caseFolder, caseDescFileName
    caseId = cmd.get('caseId')
    caseId = 'default' if caseId=='' else caseId
    casePath = os.path.join(constants.homePath, caseFolder, caseId)
    outputFolder = cmd.get('outputFolder')
    outputPath = os.path.join(casePath, outputFolder)

    newFileCMD = {'overLoad':True}
    newFileCMD.update(cmd)
    newFileCMD['fileFolder'] = casePath
    caseDesc = cmd.get('description')

    newFileCMD['fileName'] = cmd.get('inputFileName')
    newFileCMD['fileSize'] = cmd.get('inputFileSize')
    newFileCMD['fileContent'] = cmd.get('inputFileContent')
    uploadFile(newFileCMD, customAddr, link)
    
    newFileCMD['fileName'] = caseDescFileName
    newFileCMD['fileSize'] = len(caseDesc)
    newFileCMD['fileContent'] = caseDesc
    uploadFile(newFileCMD, customAddr, link)

    newFileCMD['fileName'] = cmd.get('programName')
    newFileCMD['fileSize'] = cmd.get('programSize')
    newFileCMD['fileContent'] = cmd.get('programContent')
    uploadFile(newFileCMD, customAddr, link)

    if pathInHome(outputPath):
        PathMaker().make(outputPath)

    repl = '算例 {} 接收完成'.format(caseId)
    print(repl)
    link.send(repl.encode('utf-8'))
    return

    
def genNewCase(d:dict={}):
    '''
    '''
    global latestCaseIdId, latestInputFilePathId, latestProgramPathId, latestCaseOutputFolderId, latestCaseDescriptionId
    global defaultCaseId, defaultInputFilePath, defaultProgramPath, defaultCaseOutputFolder, defaultCaseDescription
    cmd = {'cmdId':newCase_id}

    cmd['caseId'] = d.get('caseId', ConfigIOer().getSTDConfig(latestCaseIdId, defaultCaseId))
    cmd['inputFilePath'] = d.get('inputFilePath', ConfigIOer().getSTDConfig(latestInputFilePathId, defaultInputFilePath))
    cmd['programPath'] = d.get('programPath', ConfigIOer().getSTDConfig(latestProgramPathId, defaultProgramPath))
    cmd['outputFolder'] = d.get('outputFolder', ConfigIOer().getSTDConfig(latestCaseOutputFolderId, defaultCaseOutputFolder))
    cmd['description'] = d.get('description', ConfigIOer().getSTDConfig(latestCaseDescriptionId, defaultCaseDescription))
    while True:
        cb = ChoiceBox()
        cb.newChoice('算例名称', desc=cmd['caseId'])
        inputFileExist = 'exist' if os.path.isfile(cmd['inputFilePath']) else 'NOT exist'
        cb.newChoice('算例输入文件', desc='[{}]{}'.format(inputFileExist, cmd['inputFilePath']))
        programExist = 'exist' if os.path.isfile(cmd['programPath']) else 'NOT exist'
        cb.newChoice('程序', desc='[{}]{}'.format(programExist, cmd['programPath']))
        cb.newChoice('输出路径名', desc=cmd['outputFolder'])
        cb.newChoice('算例描述', desc=cmd['description'])
        inp = cb.getChoice()
        if inp == '算例名称':
            cmd['caseId'] = input('算例名称: ')
        elif inp == '算例输入文件':
            filePath = SingleFileChoicer().getChoice(cmd['inputFilePath'])
            cmd['inputFilePath'] = filePath
        elif inp == '程序':
            filePath = SingleFileChoicer().getChoice(cmd['programPath'])
            cmd['programPath'] = filePath
        elif inp == '输出路径名':
            cmd['outputFolder'] = input('输出路径名: ')
        elif inp == '算例描述':
            cmd['description'] = input('输入算例描述: ')
        elif inp == ChoiceBox.cancelId:
            return None
        elif inp == ChoiceBox.confirmId:
            ConfigIOer().writeSTDConfig(latestCaseIdId, cmd['caseId'])
            ConfigIOer().writeSTDConfig(latestInputFilePathId, cmd['inputFilePath'])
            ConfigIOer().writeSTDConfig(latestProgramPathId, cmd['programPath'])
            ConfigIOer().writeSTDConfig(latestCaseOutputFolderId, cmd['outputFolder'])
            ConfigIOer().writeSTDConfig(latestCaseDescriptionId, cmd['description'])
            
            cmd['inputFileContent'] = ''
            if os.path.isfile(cmd['inputFilePath']):
                file = open(cmd['inputFilePath'], 'rb')
                cmd['inputFileContent'] = file.read()
            cmd['programContent'] = ''
            if os.path.isfile(cmd['programPath']):
                file = open(cmd['programPath'], 'rb')
                cmd['programContent'] = file.read()
            cmd['inputFileName'] = os.path.basename(cmd['inputFilePath'])
            cmd['programName'] = os.path.basename(cmd['programPath'])
            cmd['programSize'] = len(cmd['programContent'])
            cmd['inputFileSize'] = len(cmd['inputFileContent'])
            cmd['description'] = cmd['description'].encode('utf-8')
            return cmd


CommandBase(newCase_id, newCase, genNewCase, abbr=newCase_abbr)
