#原文用的是 python2 ，这里我用python3
from  socket import *#导入 socket 包
serverSocket =socket(AF_INET,SOCK_STREAM)#AF_INET - IPv4,SOCK_STREAM - TCP
serverSocket.bind(('',6789))#指定本机6789端口
serverSocket.listen(1)#设置最大连接数为 1

while True:
    #建立连接
    print('服务已准备')#提示服务可用
    connectionSocket, addr = serverSocket.accept()# 接收到客户连接请求后，建立新的TCP连接套接字。connectionSocket 指向用户与服务器建立的 socket，addr 记录客户的地址
    try:
        message = connectionSocket.recv(1024)#缓冲设为 1024
        print(message)#这一句非必须，只是探究一下发送到服务器的 HTTP 报文是怎样的
        filename = message.split()[1]#获取文件名
        f=open(filename[1:])#打开文件
        outputdata = f.read();
        # Send one HTTP header line into socket
        header = ' HTTP/1.1 200 OK\n' \
                 'Connection: close\n' \
                 'Content-Type: text/html' \
                 '\nContent-Length: %d\n\n' % (len(outputdata))
        connectionSocket.send(header.encode())#先发请求头，编码后发到客户端
        # Send the content of the requested file to the client，逐字节发送
        for i in range (0,len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()#发送完毕后关闭 socket
    except IOError:
        header = ' HTTP/1.1 404 Found'#回复内容：HTTP/1.1 404 Found
        connectionSocket.send(header.encode())#编码后发送
        # Close client socket
        connectionSocket.close()
serverSocket.close()

