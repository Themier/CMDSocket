
'''
    关键常量
    此处的量若被改变，可能会严重影响到本地或通信功能。
'''
import re


cmd_type = dict
streamBuilder = repr
streamParser = eval

cmdStreamBuildFormat = "{}{}"
cmdStreamBuilder = lambda cmdStr : cmdStreamBuildFormat.format(len(cmdStr), cmdStr)

cmdStreamParseSizeFormat = "^(\d+)\D+"
cmdStreamParseFormat = "^\d+(.+)"

#cmdStreamBeginFlag = '&CMDSKTBG&'
#cmdStreamEndFlag = '&CMDSKTED&'

cmd_finish_words = 'cmd_finish'


def BuildCommandStream(cmd:dict):
    '''
    '''
    cmdStr = streamBuilder(cmd)
    return cmdStreamBuilder(cmdStr)


def ParseCommandStreamSize(cmdStreamHead):
    p = re.compile(cmdStreamParseSizeFormat)
    m = p.match(cmdStreamHead)
    if m != None:
        return int(m[1])
    return None


def CheckCommandStream(cmdStream, size)->bool:
    p = re.compile(cmdStreamParseFormat)
    m = p.match(cmdStream)
    if m==None:
        return False
    return len(m[1]) == size

def ParseCommandStream(cmdStream):
    p = re.compile(cmdStreamParseFormat)
    m = p.match(cmdStream)
    if m != None:
        return eval(m[1])
    return None


