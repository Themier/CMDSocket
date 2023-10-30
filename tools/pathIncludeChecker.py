
import os

class PathIncludeChecker:
    '''
    '''

    def __init__(self):
        pass

    
    @classmethod
    def IsInclude(self, path:str, targetPath:str)->bool:
        '''
        '''
        absPath = os.path.abspath(path)
        absTargetPath = os.path.abspath(targetPath)
        nPath = len(absPath)
        nTargetPath = len(absTargetPath)
        if nPath > nTargetPath:
            return False
        return absPath == absTargetPath[:nPath]