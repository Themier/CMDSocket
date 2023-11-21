
from fatal_constants import *

##
# hand input ##
local_name = 'desktop'

minPort = 8000
maxPort = 20000

maxConnection = 3

maxSizePerRecv = 10*1024*1024

maxTryRecvTimes = 500

configFolder = r'configs'
configFileSuffix = '.cfg'
athorFileName = 'athor'
stdConfigFileName = 'config'
cmdBufferConfigFileName = 'cmdBuffer'

latestLinkIPConfigId = 'localArg_latestLinkIP'
latestLinkPortConfigId = 'localArg_latestLinkPort'
latestUsernameConfigId = 'localArg_latestUsername'
latestPasswordConfigId = 'localArg_latestPassword'

##
# hand input over ##


##
# auto generate ##
import os
prjPath = os.path.abspath(os.path.dirname(__file__))
homePath = os.path.abspath(os.path.join(prjPath, os.pardir, 'fileServer'))

homePath = os.path.abspath(homePath)

server = None



