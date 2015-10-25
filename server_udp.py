#tcp imp
import os
import sys
import socket
from msg_t import *

def bye(addr):
    text = 'bye'
    msgT = msg_t()

    msgT.payload = str.encode(text)
    msgT.payload_len = len(text)
    msgT.cur_seq = cur_seq
    msgT.max_seq = max_seq
    msgT.msg_type_t = msg_type_t.MSG_TYPE_FINISH
    #UDP is not very good at signalling things are done, since its unreliable. So send about 5 UDP reqs.
    for i in range(1,5):
        serversocket.sendto(structToBytes(msgT), addr)
    serversocket.close()


if len(sys.argv)!=2:
    print("not enough arguments. arg1 is port")
    exit()
port = int(sys.argv[1])#8081


# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind the socket to a public host, and a well-known port
serversocket.bind(("", port))

# NO NEED TO LISTEN - UDP

## No need to accept - UDP
# (clientsocket, addr) = serversocket.accept()

#RECEIVE
d = serversocket.recvfrom(sizeof(msg_t))
data = d[0]
addr = d[1]
someMsgT = msg_t()
someMsgT = bytesToStruct(data)

print("server: RX ", someMsgT.msg_type_t, someMsgT.cur_seq, someMsgT.max_seq, someMsgT.payload_len)
##Double check that it was a get
if(someMsgT.msg_type_t !=msg_type_t.MSG_TYPE_GET):
    print("The first message was not MSG_TYPE_GET")
    serversocket.close()
    exit()

filename = someMsgT.payload.decode("UTF-8")
cur_seq = 0
max_seq = 0
try:
    with open(filename,mode = 'r',encoding = 'utf-8') as f:
        #get the filesize so we can have a max_seq

        statinfo = os.stat(filename)
        max_seq = statinfo.st_size // BUF_SZ#need to throw away decimals/remainders to calculate the max_seq #

        while True:
            fileText = f.read(BUF_SZ)#possible to do byte stuff
            if(fileText==""):
                print("file text is empty yay!")
                bye(addr)
                serversocket.close()
                exit()
            fileMsgT = msg_t()
            fileMsgT.payload = str.encode(fileText)
            fileMsgT.payload_len = len(fileText)
            fileMsgT.cur_seq = cur_seq
            fileMsgT.max_seq = max_seq
            fileMsgT.msg_type_t = msg_type_t.MSG_TYPE_GET_RESP

            serversocket.sendto(structToBytes(fileMsgT), addr)

            # newD = serversocket.recvfrom(sizeof(msg_t))
            # newData = newD[0]
            #
            # newMsgT = msg_t()
            # newMsgT = bytesToStruct(newData)
            # print("server: RX ", newMsgT.msg_type_t, newMsgT.cur_seq, newMsgT.max_seq, newMsgT.payload_len)
            #
            # ##Double check that it was a ack
            # if(newMsgT.msg_type_t !=msg_type_t.MSG_TYPE_GET_ACK):
            #     print("The message was not MSG_TYPE_GET_ACK???")
            #     serversocket.close()
            #     exit()

            cur_seq+=1

#if the file is not found, or whatever, stackoverflow said this is a good way
except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
    print('oops something went wrong opening up the file probably')
    failMsg = "fail"
    failMsgT = msg_t()
    failMsgT.payload = str.encode(failMsg)
    failMsgT.payload_len = len(failMsg)
    failMsgT.cur_seq = 0#doesnt matter
    failMsgT.max_seq = 0
    failMsgT.msg_type_t = msg_type_t.MSG_TYPE_GET_ERR






serversocket.sendto(structToBytes(fileMsgT), addr)

serversocket.close()
exit()
