# CMDSocket
 依靠 socket 库进行 TCP 通信，基于命令系统的远程操作工具。
 
 客户端发送命令流，服务端监听并执行命令。
 “命令”是命令类的实例，它们告诉客户端如何构造命令流，并告诉服务端收到命令流后如何执行。
 通过生成新的命令实例，可以方便地拓展任何可能的功能。

# 目前已实现的功能：
 用户验证登录  
 将客户端的代码更新同步到服务端  
 热重启服务端  
 文件传输  
 格式化文件传输  
