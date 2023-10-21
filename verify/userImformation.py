

class UserImformation(dict):
    '''
    '''
    anonymousId = 'anonymous'

    def __init__(self, initValues:dict):
        super().__init__()
        self.update({
            'username':UserImformation.anonymousId
            ,'password':''
            })
        self.update(initValues)
        return


    def IsAnonymous(self):
        '''
        自身是否为匿名用户
        '''
        return self['username'] == UserImformation.anonymousId


    def Verify(self, password):
        '''
        验证密码
        '''
        if self.IsAnonymous():
            return True
        return password == self['password']


    def ChangePassword(self, oldPassword, newPassword):
        '''
        改变密码
        '''
        if self.IsAnonymous():
            return
        if self.Verify(oldPassword):
            self['password'] = newPassword