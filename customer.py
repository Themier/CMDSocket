
import socket
import sys, getpass, time
import constants
from commands import CommandBase
from tools import ChoiceBox
from config import ConfigIOer
from tools import IterableToStr


def prepareUserImformation():
    username = ConfigIOer().getSTDConfig(constants.latestUsernameConfigId)
    password = ConfigIOer().getSTDConfig(constants.latestPasswordConfigId)
    while username == None:
        print('没有在本地发现用户信息')
        username = input('输入 用户名: ')
        password = getpass.getpass('输入 密码: ')
        ConfigIOer().writeSTDConfig(constants.latestUsernameConfigId, username)
        ConfigIOer().writeSTDConfig(constants.latestPasswordConfigId, password)

    return


def prepareLinkImformation():
    ip = ConfigIOer().getSTDConfig(constants.latestLinkIPConfigId)
    port = ConfigIOer().getSTDConfig(constants.latestLinkPortConfigId)
    while ip == None:
        print('没有在本地发现目标服务器信息')
        ip = input('输入 目标服务器 ip: ')
        port = input('输入 目标服务器 端口: ')
        ConfigIOer().writeSTDConfig(constants.latestLinkIPConfigId, ip)
        ConfigIOer().writeSTDConfig(constants.latestLinkPortConfigId, port)

    return


def main():

    cmds = CommandBase.GetAllCommandId()
    cb = ChoiceBox()
    for item in cmds:
        cb.newChoice(item, abbr=CommandBase.GetCommandAbbr(item))
    print("\n用户名 {}".format(ConfigIOer().getSTDConfig(constants.latestUsernameConfigId)))
    print("\n目标服务器 ip {}:{}".format(ConfigIOer().getSTDConfig(constants.latestLinkIPConfigId), ConfigIOer().getSTDConfig(constants.latestLinkPortConfigId)))
    while True:
        inp = cb.getChoice('\n选择指令：', addConfirm=False, addCancel=False)

        try:
            if not inp in CommandBase.inses:
                raise Exception('输入的指令无效')
            cmd = CommandBase.inses[inp].Gen()
            if not isinstance(cmd, constants.cmd_type):
                raise Exception('指令未生成')
            elif inp[0] == '*':
                print('在本地执行指令')
                CommandBase.inses[inp].Action(cmd, None, None)
            else:
                targetIP = ConfigIOer().getSTDConfig(constants.latestLinkIPConfigId)
                targetPort = int(ConfigIOer().getSTDConfig(constants.latestLinkPortConfigId))
                print('上传指令到服务器 {}:{}'.format(targetIP, targetPort))
                customer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                customer.connect((\
                    targetIP, \
                    targetPort\
                    ))
                cmd.update({\
                    'username': ConfigIOer().getSTDConfig(constants.latestUsernameConfigId)\
                    , 'password': ConfigIOer().getSTDConfig(constants.latestPasswordConfigId)\
                    })
                cmdStream = constants.BuildCommandStream(cmd)
                customer.send(cmdStream.encode('utf-8'))
                while True:
                    reply = customer.recv(constants.maxSizePerRecv).decode('utf-8')
                    print('服务器回复：{}'.format(reply))
                    if reply[-(len(constants.cmd_finish_words)):] == constants.cmd_finish_words:
                        customer.close()
                        break

        except Exception as error:
            print(error)


if __name__ == '__main__':
    try:
        prepareUserImformation()
        prepareLinkImformation()
        main()
    except Exception as error:
        print('启动失败: \n{}'.format(error))

