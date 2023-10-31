
import os
import constants
from tools import PathMaker

class ConfigIOer():
    '''
    '''

    def __init__(self):
        pass


    @classmethod
    def getConfigFolderPath(self):
        '''
        '''
        return os.path.join(constants.homePath, constants.configFolder)


    @classmethod
    def getConfigFilePath(self, title):
        '''
        '''
        return os.path.join(self.getConfigFolderPath(), title + constants.configFileSuffix)

    
    @classmethod
    def getConfig(self, title, id, defaultValue=None):
        '''
        '''
        if title == constants.athorFileName:
            return defaultValue
        configs = {}
        path = ConfigIOer.getConfigFilePath(title)
        if os.path.isfile(path):
            configFile = open(path, 'r')
            configs.update(eval(configFile.read()))
            configFile.close()
            if id in configs:
                return configs[id]

        return defaultValue

    
    @classmethod
    def write(self, title, id, value)->bool:
        '''
        '''
        if title == constants.athorFileName:
            return False
        configs = {}
        path = ConfigIOer.getConfigFilePath(title)
        if os.path.isfile(path):
            configFile = open(path, 'r')
            configs.update(eval(configFile.read()))
            configFile.close()
        if configs[id] == value:
            return True
        configs[id] = value
        configFile = open(path, 'w')
        configFile.write(repr(configs))
        configFile.close()
        return True

    
    @classmethod
    def getSTDConfig(self, id, defaultValue=None):
        return self.getConfig(constants.stdConfigFileName, id, defaultValue)

    
    @classmethod
    def writeSTDConfig(self, id, value):
        return self.write(constants.stdConfigFileName, id, value)


if not PathMaker().make(ConfigIOer.getConfigFolderPath()):
    raise "config folder can't be generated."


def singleTest():
    print('write test config: {} -> {}'.format(ConfigIOer().write('test_config', 'test_id', 'test_value'), ConfigIOer().getConfig('test_config', 'test_id')))
    print('rewrite test config: {} -> {}'.format(ConfigIOer().write('test_config', 'test_id', 'test_value2'), ConfigIOer().getConfig('test_config', 'test_id')))
    print('write test config: {} -> {}'.format(ConfigIOer().write('test_config', 'test_id2', 'test_value2'), ConfigIOer().getConfig('test_config', 'test_id2')))