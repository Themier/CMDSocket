
##
# hand input ##
minPort = 8000
maxPort = 60000

maxConnection = 3

cmdMaxSize = 10*1024*1024

configFolder = r'configs'
configFileSuffix = '.cfg'
athorFileName = 'athor'

caseFolder = r'lbmCase'
caseInputFileName = 'params.dat'
caseProgrameName = 'program.exe'
caseResultPathName = 'results'
caseDescFileName = 'desc.txt'

cmd_finish_words = 'cmd_finish'
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


