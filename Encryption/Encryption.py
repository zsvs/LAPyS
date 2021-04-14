"""
Module provides simple functions for encoding/decoding in ASCII table
"""
class Coder:
    """
    Static class for encode/decode data to/from ASCII
    """
    @staticmethod
    def Encrypt(String):
        """
        Return string in ASCII representation, splitted by comma
        """
        lst = list()
        for symbol in String:
            lst.append(ord(symbol))
        return str(lst)[1:len(str(lst))-1]

    @staticmethod
    def Decrypt(ByteList):
        """
        Return string decoded from ASCII
        """
        st = str()
        for ASCII_Code in ByteList:
            st += chr(int(ASCII_Code))
        return st