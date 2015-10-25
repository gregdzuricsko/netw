from ctypes import *

BUF_SZ = 1024
#hide the pythony syntax which isn't super comfortable to me yet
def structToBytes(self):
    return bytearray(self)

#hide the pythony syntax which isn't super comfortable to me yet 
def bytesToStruct(self):
    return msg_t.from_buffer_copy(self)

str_map =  [
    "invalid",
    "get",
    "get_err",
    "get_resp",
    "get_ack",
    "max",
    "finish"
]

class msg_type_t():
    MSG_TYPE_INVALID = 0
    MSG_TYPE_GET = 1
    MSG_TYPE_GET_ERR = 2
    MSG_TYPE_GET_RESP = 3
    MSG_TYPE_GET_ACK = 4
    MSG_TYPE_FINISH = 5
    MSG_TYPE_MAX = 6



class msg_t(Structure):
    _fields_ = [("msg_type_t", c_int),                      # message type
                ("cur_seq", c_int),                     # current seq number
                ("max_seq", c_int),                         # max seq number
                ("payload_len", c_int),                     # length of payload
                ("payload", c_char * BUF_SZ)]                 # bytearray buffer for data
