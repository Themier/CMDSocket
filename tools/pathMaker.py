
import os

class PathMaker:
    '''
    '''

    def __init__(self):
        pass


    @classmethod
    def make(self, path:str)->bool:
        '''
        '''
        if os.path.isdir(path):
            return True

        parpath = os.path.dirname(path)
        if not os.path.isdir(parpath):
            self.make(parpath)

        try:
            os.mkdir(path)
            return True
        except:
            return False