
# hand input
homePath = r'n:/fileServer/'

minPort = 8000
maxPort = 60000

maxConnection = 3

cmdMaxSize = 10*1024*1024

caseFolder = r'lbmCase'
caseInputFileName = 'parames.dat'
caseProgrameName = 'program.exe'
caseResultPathName = 'results'
caseDescFileName = 'desc.txt'

# auto generate
import os
prjPath = os.path.abspath(os.path.join(__file__, os.pardir))
