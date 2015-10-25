#TCP imp

import socket
import sys
import io
from msg_t import *


if len(sys.argv)!=4:
    print("not enough arguments. arg1 is server ip, arg2 is port, arg3 is filename")
    exit()
serverIP = sys.argv[1]#localhost
port = int(sys.argv[2])#8081
filename = sys.argv[3]

try:
    # UDP gets INET, DATAGRAM
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # UDP doesn't need connection handshake
    # s.connect((serverIP, port))
except Exception as e:
    print('something\'s wrong with %s:%d. Exception type is %s' % (serverIP, port, e))

#form the first message that asks for the file
firstMsg = msg_t()
firstMsg.msg_type_t = msg_type_t.MSG_TYPE_GET
firstMsg.cur_seq = 0
firstMsg.max_seq = 0
firstMsg.payload_len = len(filename)
firstMsg.payload = str.encode(filename)
#conver the message to bytes to send as a datagram
x = structToBytes(firstMsg)

s.sendto(x,(serverIP, port))
fileText = ''
clientSeq=0

while True:
    d = s.recvfrom(sizeof(msg_t))
    data = d[0]
    addr = d[1]
    if not data:
        print("The data was empty??")
        s.close()
        exit()
    someMsgT = msg_t()
    someMsgT = bytesToStruct(data)
    print("client: RX ", someMsgT.msg_type_t, someMsgT.cur_seq, someMsgT.max_seq, someMsgT.payload_len)
    if(someMsgT.msg_type_t == msg_type_t.MSG_TYPE_FINISH  ):
        #it's the end, so wrie and clos the file
        print("The message was MSG_TYPE_FINISH. That means we're done.")
        with open("2" + filename ,mode = 'w',encoding = 'utf-8') as f:
            f.write(fileText)
        s.close()
        exit()
    if(someMsgT.msg_type_t == msg_type_t.MSG_TYPE_GET_ERR  ):
        print("The message was MSG_TYPE_GET_ERR. That means something went wrong serverside.")
        s.close()
        exit()
    if(someMsgT.msg_type_t != msg_type_t.MSG_TYPE_GET_RESP ):
        print("The message was not MSG_TYPE_GET_RESP. Something weird happened.")
        s.close()
        exit()
    #dont have to check order on UDP

    #we do have to decode the bytes into a thing
    fileText += someMsgT.payload.decode("UTF-8")
    clientSeq+=1
