
import os
import constants
from verify import UserImformation



class Verify():
    '''
    登录验证
    '''

    athor = None
    athorFilePath = None

    def __init__(self):
        if Verify.athor == None:
            Verify.athor = {}

            configPath = os.path.join(constants.homePath, constants.configFolder)
            if not os.path.exists(configPath):
                os.mkdir(configPath)
                
            Verify.athorFilePath = os.path.join(configPath, constants.athorFileName + constants.configFileSuffix)
            if not os.path.isfile(Verify.athorFilePath):
                userImformation = UserImformation({'username':'tower','password':'tower^10'})
                Verify.athor.update({userImformation['username'] : userImformation})
                Verify.UpdateArchive()
            else:
                file = open(Verify.athorFilePath, 'r')
                dict = eval(file.read())
                for username in dict:
                    Verify.athor[username] = UserImformation(dict[username])
                file.close()

        return


    @classmethod
    def Verify(self, username:str, password:str):
        '''
        '''
        if username in self.athor:
            if self.athor[username].Verify(password):
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
        archive = open(Verify.athorFilePath, 'w')
        archive.write(repr(self. athor))
        archive.close()

        return


def singleTest():
    Verify()
    print(Verify.Verify('tower', '???'))


Verify()
