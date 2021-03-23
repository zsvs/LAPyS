def Encrypt(String):
    lst = list()
    for symbol in String:
        lst.append(ord(symbol))
    return lst

def Decrypt(ByteList):
    st = str()
    for ASCII_Code in ByteList:
        st += chr(int(ASCII_Code))
    return st