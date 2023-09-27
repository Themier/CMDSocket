
import os
from constants import *
from commands import CommandBase
from commands.newFile import newFile, makePath, pathInHome


def uploadProject(cmd, customAddr, link):
    '''
    '''
    projectPath = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
    
    prjMap = cmd['prjMap']
    CMD = {}
    CMD['fileFolder'] = projectPath
    for item in prjMap:
        CDM['fileName'] = item
        CMD['fileSize'] = prjMap[item]['fileSize']
        CMD['fileContent'] = prjMap[item]['fileContent']
        CMD['contentMode'] = 'text'
        CMD['overLoad'] = True
        newFile(CMD, customAddr, link)

    return


CommandBase('uploadProject', uploadProject)

uploadProject({}, '', None)
