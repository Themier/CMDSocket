
import socket, sys, os, requests
from serverAndCustomer.serverBooter import ServerBooter
from serverAndCustomer.serverTutelage import ServerTutelage
from tools import PathMaker

# constants
import constants

# home
homePath = os.path.abspath(constants.homePath)
PathMaker().make(homePath)
os.chdir(homePath)
#os.system('explorer.exe {}'.format(homePath))

# init
courtesyStr = '\n你好 ^-^， 愿一切向好。\n启动中 ... \n'
hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
hostIP = None
try:
    hostIP = requests.get('http://httpbin.org/ip').json()['origin']
except Exception as result:
    print('获取公网 IP 失败，被接口拒绝。可能是因为代理？')

#courtesy   
print(courtesyStr)
print('服务器主机名: {}'.format(hostname))
print('服务器主机 ip: {}'.format(hostIP))
print('服务器主机 ip: {}'.format(hostip))
print('端口范围: {} - {}'.format(constants.minPort, constants.maxPort))

#boot
serverBooter = ServerBooter()
tryBindIps = [hostip]
if serverBooter.TryBoot(tryBindIps, range(constants.minPort, constants.maxPort)):
    print('\n服务器启动 {}:{}\n'.format(serverBooter.ip, serverBooter.port))
else:
    print('\n服务器启动失败，可能是没有可用的端口或 ip\n')
    sys.exit(1)
serverBooter.Listen(constants.maxConnection)
server = serverBooter.server
print('最大连接数 {}\n\n'.format(serverBooter.nlisten))

#tutelage
tutelage = ServerTutelage(server)
tutelage.Tutelage()




