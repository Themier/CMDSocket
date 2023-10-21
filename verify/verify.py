
import os
import constants
from verify import UserImformation



class Verify():
    '''
    登录验证
    '''

    athor = None

    def __init__(self):
        if Verify.athor == None:
            Verify.athor = {}
            configPath = constants.configFolder
            if not os.path.exists(configPath):
                os.mkdir(configPath)

            filePath = os.path.join(configPath, constants.athorFileName + constants.configFileSuffix)
            if not os.path.isfile(filePath):
                userImformation = UserImformation({'username':'tower','password':'tower^10'})
                Verify.athor.update({userImformation['username'] : userImformation})
                Verify.UpdateArchive()
            else:
                file = open(filePath, 'r')
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
        configPath = constants.configFolder
        filePath = os.path.join(configPath, constants.athorFileName + constants.configFileSuffix)
        archive = open(filePath, 'w')
        archive.write(repr(self. athor))
        archive.close()

        return


def singleTest():
    Verify()
    print(Verify.Verify('tower', '???'))


Verify()
