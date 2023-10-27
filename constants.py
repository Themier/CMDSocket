
from fatal_constants import *

##
# hand input ##
local_name = 'desktop'

minPort = 8000
maxPort = 60000

maxConnection = 3

maxSizePerRecv = 10*1024

maxTryRecvTimes = 500

configFolder = r'configs'
configFileSuffix = '.cfg'
athorFileName = 'athor'
stdConfigFileName = 'config'

##
# hand input over ##


##
# auto generate ##
import os
prjPath = os.path.abspath(os.path.dirname(__file__))
homePath = os.path.abspath(os.path.join(prjPath, os.pardir, 'fileServer'))

homePath = os.path.abspath(homePath)
#caseFolder = os.path.abspath(os.path.join(homePath, caseFolder))
#caseInputFileName = os.path.abspath(os.path.join(homePath, caseInputFileName))
#caseProgrameName = os.path.abspath(os.path.join(homePath, caseProgrameName))
#caseResultPathName = os.path.abspath(os.path.join(homePath, caseResultPathName))
#caseDescFileName = os.path.abspath(os.path.join(homePath, caseDescFileName))

server = None

##
# auto generate over ##


