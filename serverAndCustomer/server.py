import socket, sys, os, requests
from .serverBooter import ServerBooter
from .serverTutelage import ServerTutelage

# constants
from constants import *

# home
homePath = os.path.abspath(homePath)
os.chdir(homePath)
#os.system('explorer.exe {}'.format(homePath))

# init
courtesyStr = '\n你好 ^-^， 愿一切向好。\n启动中 ... \n'
hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
#hostIP = requests.get('http://httpbin.org/ip').json()['origin']

#courtesy
print(courtesyStr)
print('服务器主机名: {}'.format(hostname))
#print('服务器主机 ip: {}'.format(hostIP))
print('服务器主机 ip: {}'.format(hostip))
print('端口范围: {} - {}'.format(minPort, maxPort))

#boot
serverBooter = ServerBooter()
tryBindIps = [hostip]
if serverBooter.TryBoot(tryBindIps, range(minPort, maxPort)):
    print('\n服务器启动 {}:{}\n'.format(serverBooter.ip, serverBooter.port))
else:
    print('\n服务器启动失败，可能是没有可用的端口或 ip\n')
    sys.exit(1)
serverBooter.Listen(maxConnection)
server = serverBooter.server
print('最大连接数 {}\n\n'.format(serverBooter.nlisten))

#tutelage
tutelage = ServerTutelage(server)
tutelage.Tutelage()




