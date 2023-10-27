
import socket
import sys, getpass, time
import constants
from commands import CommandBase
from tools import ChoiceBox
from config import ConfigIOer


def genUserImformation():
    username = ConfigIOer().getSTDConfig('customer_local_username')
    password = ConfigIOer().getSTDConfig('customer_local_password')
    while username == None or len(username) == 0:
        username = input('input uername: ')
        password = getpass.getpass('input password: ')

    cb = ChoiceBox()
    cb.newChoice('reinput username')
    cb.newChoice('reinput password')
    cb.newChoice('show password')
    while True:
        inp = cb.getChoice('your username: {}'.format(username))
        if inp == 'reinput username':
            username = input('input uername: ')
        elif inp == 'reinput password':
            password = getpass.getpass('input password: ')
        elif inp == 'show password':
            print(password, end='\r')
            time.sleep(1.0)
            for i in range(len(password)):
                print('*', end='')
        elif inp == ChoiceBox.confirmId:
            break
        elif inp == ChoiceBox.cancelId:
            sys.exit(0)

    ConfigIOer().writeSTDConfig('customer_local_username', username)
    ConfigIOer().writeSTDConfig('customer_local_password', password)
    return { \
        'username':username\
        ,'password':password\
        }


def main(userImformation:dict):
    cmds = CommandBase.GetAllCommandId()
    cb = ChoiceBox()
    for item in cmds:
        cb.newChoice(item, '')
    cb.newChoice('*quit')
    while True:
        inp = cb.getChoice('选择指令：', addConfirm=False, addCancel=False)

        try:
            if inp in CommandBase.inses:
                cmd = CommandBase.inses[inp].Gen()
                if not isinstance(cmd, constants.cmd_type):
                    print('指令生成失败')
                elif inp[0] == '*':   # 本地命令
                    CommandBase.inses[inp].Action(cmd, None, None)
                else:   # 远程命令
                    customer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    customer.connect(('192.168.41.129', 8000))
                    cmd.update(userImformation)
                    cmdStream = constants.BuildCommandStream(cmd)
                    customer.send(cmdStream.encode('utf-8'))
                    while True:
                        reply = customer.recv(constants.maxSizePerRecv).decode('utf-8')
                        print('服务器回复：{}'.format(reply))
                        if reply[-(len(constants.cmd_finish_words)):] == constants.cmd_finish_words:
                            customer.close()
                            break
            elif inp == '*quit':
                sys.exit(0)
            else:
                print('可用的指令：{}'.format(CommandBase.inses.keys()))

        except Exception as error:
            print('发生错误: \n{}'.format(error))


if __name__ == '__main__':
    try:
        main(genUserImformation())
    except Exception as error:
        print('发生错误: \n{}'.format(error))

