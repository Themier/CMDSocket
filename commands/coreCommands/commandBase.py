
from typing import Callable, Iterable
from socket import socket
import re
import constants

class CommandBase():
    '''
    '''

    inses = {}
    abbrDict = {}

    def __init__(self, id, Action, Gen, **d):
        '''
        '''
        self.id = id
        self.Action:Callable([dict, str, socket], int) = Action
        self.Gen:Callable([dict], dict) = Gen

        CommandBase.inses[self.id] = self

        abbr = d.get('abbr', None)
        if isinstance(abbr, Iterable) and not isinstance(abbr, str):
            for iabbr in abbr:
                CommandBase.abbrDict[str(iabbr)] = id
        elif abbr != None:
                CommandBase.abbrDict[str(abbr)] = id
        return


    @classmethod
    def GetAllCommandId(self):
        return list(self.inses.keys())


    @classmethod
    def GetCommandAbbr(self, id):
        return [iabbr for iabbr in self.abbrDict if self.abbrDict[iabbr]==id]

    
