
from typing import Callable, Iterable
from socket import socket
import re
import constants


class CommandBase():
    '''
    inses: 所有完成初始化的 CommandBase 实例的字典
    {
        "command_id" : command_instance
        , ...
    }

    abbrDict: 命令缩写与命令 id 的对照表，后覆盖前
    {
        "command_abbreviation" : "command_id"
    }
    '''

    inses = {}
    abbrDict = {}

    def __init__(self, id, Action, Gen, **d):
        '''
        id:
        Action： 命令的行为，从第一个参数获取命令参数，第二个参数为命令发起者的ip地址，第三个参数为套接字
        Gen：生成命令流的方法，从第一个参数获取默认参数
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

    
