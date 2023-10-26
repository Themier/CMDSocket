
import socket
import constants

class ServerBooter():
    '''
    '''

    def __init__(self):
        self.switch = 'off'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        constants.server = self.server
        self.ip=None
        self.port=None
        self.nlisten = None

        return


    def Boot(self, hostIP:str, port:int)->bool:
        '''
        '''
        if self.switch == 'off':
            try:
                self.server.bind((hostIP, port))
                self.switch = 'on'
                self.ip = hostIP
                self.port = port
                return True
            except Exception as error:
                print(error)
            
        return False


    def TryBoot(self, hostIPs:list, ports:list)->bool:
        '''
        '''
        if self.switch == 'off':
            for ip in hostIPs:
                for port in ports:
                    try:
                        self.server.bind((ip, port))
                        self.switch = 'on'
                        self.ip = ip
                        self.port = port
                        for i in range(100):
                            print(' ', end='')
                        print()
                        return True
                    except Exception as error:
                        print('位于 {} 的端口无法使用 : {}'.format((ip, port), error), end='\r')

        return False


    def Listen(self, n):
        '''
        '''
        if self.switch == 'on':
            self.server.listen(n)
            self.nlisten = n

        return
