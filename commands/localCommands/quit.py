
import sys
from commands import CommandBase

quit_id = '*quit'
quit_abbr = '*qt'

def quit(cmd, customAddr, link):
    sys.exit(0)

    return


def genQuit(d:dict={}):
    global quit_id
    cmd = {}
    cmd['cmdId'] = quit_id

    return cmd


CommandBase(quit_id, quit, genQuit, abbr=quit_abbr)
