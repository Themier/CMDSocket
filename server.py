
import socket, sys, os
try:
    import requests
except Exception as error:
    print(error)
from serverAndCustomer.serverBooter import ServerBooter
from serverAndCustomer.serverTutelage import ServerTutelage
from tools import PathMaker
import constants


def goHome():
    '''
    '''
    homePath = os.path.abspath(constants.homePath)
    PathMaker().make(homePath)
    os.chdir(homePath)


def initial():
    '''
    '''
    courtesyStr = '\n你好 ^-^， 愿一切向好。\n启动中 ... \n'
    hostname = socket.gethostname()
    hostip = socket.gethostbyname(hostname)
    hostIP = None
    try:
        hostIP = requests.get('http://httpbin.org/ip').json()['origin']
    except Exception as result:
        print('获取公网 IP 失败：', result)

    print(courtesyStr)
    print('服务器主机名: {}'.format(hostname))
    print('服务器主机 ip: {}'.format(hostip))
    print('服务器主机 ip: {}'.format(hostIP))
    print('端口范围: {} - {}'.format(constants.minPort, constants.maxPort))

    return hostname, hostip, hostIP


def main(hostname, hostip, hostIP):
    '''
    '''
    serverBooter = ServerBooter()
    tryBindIps = [ip for ip in ['0.0.0.0', hostIP, hostip] if ip != None]
    if serverBooter.TryBoot(tryBindIps, range(constants.minPort, constants.maxPort)):
        print('\n服务器启动 {}:{}\n'.format(serverBooter.ip, serverBooter.port))
    else:
        print('\n服务器启动失败。\n')
        sys.exit(1)
    serverBooter.Listen(constants.maxConnection)
    server = serverBooter.server
    print('最大连接数 {}\n\n'.format(serverBooter.nlisten))

    tutelage = ServerTutelage(server)
    tutelage.Tutelage()


if __name__ == '__main__':
    goHome()
    main(*initial())




