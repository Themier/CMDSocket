
import os
import re
from constants import *
from commands import CommandBase
from commands.uploadFile import makePath

uploadPrj_id = 'uploadProject'
uploadPrj_ignores = ['^[.]vs$', '^__pycache__$', '^.git$', '.*[.]cfg$']

def uploadProject(cmd, customAddr, link)->int:
    '''
    '''
    prjMap = cmd['prjMap']

    for item in prjMap:
        fp = os.path.join(prjPath, item)
        makePath(os.path.abspath(os.path.join(fp, os.pardir)))
        f = open(fp, 'wb')
        if len(prjMap[item]) > 0:
            f.write(prjMap[item])
        f.close()
    #CMD = {}
    #CMD['fileFolder'] = prjPath+'new'
    #CMD['overLoad'] = True
    #for item in prjMap:
    #    CMD['fileNameAndContent'] = [item, prjMap[item]]
    #    CMD = CommandBase.inses['uploadFile'].Gen(CMD)
    #    print(item)
    #    CommandBase.inses['uploadFile'].Action(CMD, customAddr, link)

    return


def __ignoreThis(val:str)->bool:
    '''
    '''
    for iig in uploadPrj_ignores:
        if re.match(iig, val):
            return True
    return False


def __getFolderItems(prjMap, root, now='./'):
    '''
    '''
    items = os.listdir(now)
    for item in items:
        if __ignoreThis(item):
            continue
        path = os.path.join(root, now, item)
        if os.path.isfile(path):
            file = open(path, 'rb')
            prjMap[os.path.join(now, item)] = file.read()
            file.close()
        elif os.path.isdir(path):
            __getFolderItems(prjMap, root, os.path.join(now, item))
    
    return


def genUploadProject(d:dict={})->dict:
    '''
    '''
    cmd = {'cmdId':uploadPrj_id}
    prjMap = {}
    __getFolderItems(prjMap, prjPath)
    cmd['prjMap'] = prjMap

    return cmd


CommandBase(uploadPrj_id, uploadProject, genUploadProject)

