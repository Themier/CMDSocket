
import os

class UserImformation(dict):
    '''
    '''

    def __init__(self, initValues:dict):
        super().__init__()
        self.update({
            'username':None
            ,'password':None
            })
        self.update(initValues)
        return



class Verify():
    '''
    登录验证
    '''

    athor = None

    def __init__(self):
        if Verify.athor == None:
            configPath = 'configs'
            if not os.path.exists(configPath):
                os.mkdir(configPath)

            filePath = os.path.join(configPath, 'athor.cfg')
            if not os.path.isfile(filePath):
                userImformation = UserImformation({'username':'tower','password':'tower^10'})
                Verify.athor = {userImformation['username'] : userImformation}
                Verify.UpdateArchive()
            else:
                file = open(filePath, 'r')
                Verify.athor = eval(file.read())
                file.close()

        return


    @classmethod
    def Verify(self, username:str, password:str):
        '''
        '''
        if username in self.athor and password == self.athor[username]['password']:
            return True

        return False


    @classmethod
    def AddUser(self, username:str, password:str):
        '''
        '''
        self.athor[username] = UserImformation({'username':username, 'password':password})

        self.UpdateArchive()
        return


    @classmethod
    def UpdateArchive(self):
        '''
        '''
        configPath = 'configs'
        filePath = os.path.join(configPath, 'athor.cfg')
        archive = open(filePath, 'w')
        archive.write(repr(self. athor))
        archive.close()

        return



Verify()
