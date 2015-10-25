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
    # create an INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # now connect to the web server on port 8081 - the normal http port
    s.connect((serverIP, port))
except Exception as e:
    print('something\'s wrong with %s:%d. Exception type is %s' % (serverIP, port, e))

firstMsg = msg_t()
firstMsg.msg_type_t = msg_type_t.MSG_TYPE_GET
firstMsg.cur_seq = 0
firstMsg.max_seq = 0
firstMsg.payload_len = len(filename)
firstMsg.payload = str.encode(filename)

x = structToBytes(firstMsg)

s.send(x)
fileText = ''
clientSeq=0

while True:
    data = s.recv(sizeof(msg_t))
    if not data:
        break
    someMsgT = msg_t()
    someMsgT = bytesToStruct(data)
    print("client: RX ", someMsgT.msg_type_t, someMsgT.cur_seq, someMsgT.max_seq, someMsgT.payload_len)
    if(someMsgT.msg_type_t == msg_type_t.MSG_TYPE_GET_ERR  ):
        print("The message was MSG_TYPE_GET_ERR. That means something went wrong serverside.")
        s.close()
        exit()
    if(someMsgT.msg_type_t != msg_type_t.MSG_TYPE_GET_RESP ):
        print("The message was not MSG_TYPE_GET_RESP. Something weird happened.")
        s.close()
        exit()
    #check order TCP
    if(someMsgT.cur_seq > someMsgT.max_seq or someMsgT.cur_seq != clientSeq):
        print("Something funky hapened on the packet order.",someMsgT.cur_seq,someMsgT.max_seq, clientSeq)
        s.close()
        exit()
    fileText += someMsgT.payload.decode("UTF-8")
    clientSeq+=1

    continueMsgTxt = "more"
    continueMsg = msg_t()
    continueMsg.msg_type_t = msg_type_t.MSG_TYPE_GET_ACK
    continueMsg.cur_seq = someMsgT.cur_seq
    continueMsg.max_seq = someMsgT.max_seq
    continueMsg.payload_len = len(continueMsgTxt)
    continueMsg.payload = str.encode(continueMsgTxt)
    s.send(structToBytes(continueMsg))

with open("2" + filename ,mode = 'w',encoding = 'utf-8') as f:
    f.write(fileText)



s.close()
