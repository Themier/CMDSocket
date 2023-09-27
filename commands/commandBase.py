

class CommandBase():
    '''
    '''

    inses = {}

    def __init__(self, id, Action):
        '''
        '''
        self.id = id
        self.Action = Action

        CommandBase.inses[self.id] = self
        return


    
