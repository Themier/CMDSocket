import socket
import sys

programPath = r'W:\Cpp\LBM_230914\LBM_230914\x64\Release\LBM_230914.exe'
inputFilePath = r'W:\Cpp\LBM_230914\LBM_230914\params.dat'

userImformation = {
    'username':'tower'
    ,'password':'tower^10'
    }
caseImformation = {
    'caseId':''
    ,'description':''
    }


customer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

customer.connect(('192.168.41.85', 8000))

cmd = {'cmd':'newCase'}

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