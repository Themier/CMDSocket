#import commands
#import re

d = {1:'1', 2:'2'}

for i in d.keys():
    print(i)

#import os

#print(os.path.basename('not a path'))

#format = '.*1.*'
#p = re.compile(format)
#m = p.match('0101010')
#print(m)

#import constants

#cmd = {'1':1, '2':2}
#cmdStream = constants.BuildCommandStream(cmd)
#print(type(cmdStream), cmdStream)
#size  = constants.ParseCommandStreamSize(cmdStream)
#print(type(size), size)
#print('check:', constants.CheckCommandStream(cmdStream[:-2], size))
#print('check:', constants.CheckCommandStream(cmdStream, size))
#cmd_ = constants.ParseCommandStream(cmdStream)
#print(type(cmd_), cmd_)

#print(repr(dict()))

#cmd = {'a':1, 'b':'two'}

#cmdStream = commands.CommandBase.BuildCommandStream(cmd)
#print(cmdStream)
#print(commands.CommandBase.ParseCommandStream(cmdStream))


#str =  '{}{}'
##former = lambda dictStr:eval(str.format('{}', '{}', len(dictStr), dictStr))
#former = lambda dictStr:str.format(len(dictStr), dictStr)

#val = former(repr({'1' : 1}))
#print(val)

#format = "^(\d+)\D+"
#p = re.compile(format)
#m = p.match('1234')
#print(m[1])

## 获取用户输入的文件路径
#file_path = input("请输入文件路径：")

## 验证文件是否存在
#if not os.path.isfile(file_path):
#    print("文件不存在，请重新输入有效的文件路径。")
#    exit(0)

## 获取文件权限
#file_permission = oct(os.stat(file_path).st_mode)[-3:]

## 输出文件权限
#print("文件权限：", file_permission)