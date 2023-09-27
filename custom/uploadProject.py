import socket
import sys, os

#projectPath = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
#print(os.listdir(projectPath))
#for dirpath, dirs, files in os.walk(projectPath):
#    print('\n\n')
#    print(dirpath)
#    print(os.path.basename(dirpath))
#    print(dirs)
#    print(files)
#    print('\n\n')
#sys.exit(0)

def GenPrjMap(prjMap, rootPath, ignores):
    for dirpath, dirs, files in os.walk(rootPath):
        if os.path.basename(dirpath) in ignores:
            continue
        for file in files:
            if file in ignores:
                continue
            f = open(os.path.join(rootPath, dirpath, file), 'r', encoding='utf-8')
            content = f.read()
            size = len(content)
            prjMap[file] = {'fileContent':content, 'fileSize':size}


userImformation = {
    'username':'tower'
    ,'password':'tower^10'
    }
prjMap = {}
cmd = {'cmd':'uploadProject'}

projectPath = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
GenPrjMap(prjMap, projectPath, ['.vs', '__pycache__'])

sys.exit(0)


customer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

customer.connect(('192.168.41.85', 8000))

f= open(programPath, 'rb')
cmd['programContent'] = f.read()
cmd['programSize'] = len(cmd['programContent'])
f.close()
f= open(inputFilePath, 'r')
cmd['inputFileContent'] = f.read()
cmd['inputFileSize'] = len(cmd['inputFileContent'])
f.close()

while True:
    inp = input('case id : {}\ndescription: {}\n[y]es / [r]esetId / [i]nputDescription\n'.format(caseImformation['caseId'], caseImformation['description']))

    if inp == 'y':
        cmd.update(caseImformation)
        cmd.update(userImformation)
        cmd = repr(cmd)
        print(f'cmd length {len(cmd)}')
        customer.send(cmd.encode('utf-8'))
        while True:
            reply = customer.recv(1024).decode('utf-8')
            print(reply)
            if reply == 'cmd_finish':
                customer.close()
                sys.exit(0)
    elif inp == 'r':
        caseImformation['caseId'] = input('new case name ')
    elif inp == 'i':
        caseImformation['description'] = input('new case description ')