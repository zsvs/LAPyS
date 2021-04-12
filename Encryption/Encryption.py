"""
Module provides simple functions for encoding/decoding in ASCII table
"""
def Encrypt(String):
    lst = list()
    for symbol in String:
        lst.append(ord(symbol))
    return str(lst)[1:len(str(lst))-1]

def Decrypt(ByteList):
    st = str()
    for ASCII_Code in ByteList:
        st += chr(int(ASCII_Code))
    return st