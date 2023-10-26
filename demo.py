import commands

str = 'abcdef'
subStr = 'bc'

print(str.find(subStr))

str[3]=0
print(str)

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