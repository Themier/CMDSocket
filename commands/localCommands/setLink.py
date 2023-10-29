
import socket
from commands import CommandBase
import constants
from tools import ChoiceBox
from config import ConfigIOer

setLink_id = '*setLink'
setLink_abbr = '*sl'

def setLink(cmd, customAddr, link:socket.socket):
    ConfigIOer.writeSTDConfig(constants.latestLinkIPConfigId, cmd.get('ip'))
    ConfigIOer.writeSTDConfig(constants.latestLinkPortConfigId, cmd.get('port'))
    return


def genSetLink(d:dict={}):
    global setLink_id
    cmd = {}
    cmd['cmdId'] = setLink_id

    ip = d.get('ip', ConfigIOer.getSTDConfig(constants.latestLinkIPConfigId))
    port = d.get('port', ConfigIOer.getSTDConfig(constants.latestLinkPortConfigId))
    
    cb = ChoiceBox()
    while True:
        cb.newChoice('ip', desc=ip)
        cb.newChoice('port', desc=port)
        inp = cb.getChoice()
        if inp == 'ip':
            ip = input('input ip: ')
        elif inp == 'port':
            port = input('input port: ')
        elif inp == ChoiceBox.confirmId:
            break
        elif inp == ChoiceBox.cancelId:
            return None

    cmd['ip'] = ip
    cmd['port'] = port
    return cmd


CommandBase(setLink_id, setLink, genSetLink, abbr=setLink_abbr)