
from typing import Callable
from socket import socket

class CommandBase():
    '''
    '''

    inses = {}

    def __init__(self, id, Action, Gen):
        '''
        '''
        self.id = id
        self.Action:Callable([dict, str, socket], int) = Action
        self.Gen:Callable([dict], dict) = Gen

        CommandBase.inses[self.id] = self
        return


    
