import numpy as np
import os
import math

class Message:
    pathname=None
    content=None
    content_length = 0
    header = None
    header_length = 0
    file_name = None
    file_extension = None
    binary_digit_list=None

    def __init__(self, pathname = None):
        if pathname!= None:
            with open(pathname,'rb') as f:
                self.content=f.read()
            self.content_length = len(self.content)
            self.file_name, self.file_extension = os.path.splitext(pathname)
            self.file_name = self.file_name.split('/')[-1]

    def to_binary(self,msg=None):
        if msg is None:
            msg=self.content
        return [format(i,'08b') for i in msg]

    def num_to_binary_list(self,num):
        binary_list=[]
        binary=bin(num).replace("0b","")
        for digit in np.array(list(binary)):
            binary_list.append(digit.astype(int))
        while len(binary_list)<8:
            binary_list.insert(0,0)
        return binary_list

    def binary_to_dcible(self,binary_list):

        in_binary_str=[str(digit) for digit in binary_list]
        in_binary=''.join(in_binary_str)
        return int(in_binary,2)

    def to_binary_list(self,binary_msg=None):
        if binary_msg is None:
            binary_msg=self.to_binary()
        binary_list=[]
        temp = np.array([list(i) for i in binary_msg])
        for b_list in temp:
            for b_digit in b_list:
                binary_list.append(b_digit.astype(int))
        return binary_list
        
    def create_message_header(self):
        msg_header_string = ""
        temp = []
        msg_header_string += self.file_name + ";"
        msg_header_string += self.file_extension + ";"
        msg_header_string += str(self.content_length) + ";"
        #print(msg_header_string)
        
        self.header = msg_header_string.encode('utf-8')

        header_binary_msg=self.to_binary(self.header)
        header_binary_list=self.to_binary_list(header_binary_msg)
        self.header_length = len(header_binary_list)

        return self.num_to_binary_list(self.header_length) + header_binary_list
        
    def create_message_content(self):
        return self.to_binary_list()

    def create_binary_list(self):
        self.binary_digit_list=self.create_message_header() +self.create_message_content()
        return self.binary_digit_list

    def extract_msg(self,binary_list):
        self.header_length=self.binary_to_dcible(binary_list[0:8])
        self.header=self.extract_header(binary_list[8:8+self.header_length],self.header_length)


        header_items=self.header.split(';')
        self.content_length=int(header_items[-2])
        self.file_name=header_items[0]
        self.file_extension=header_items[1]

        temp=binary_list[8+self.header_length:]
        self.content=self.extract_content(temp, self.content_length)

        self.write_msg(file_name='output',)
        return self.content

    def extract_header(self,header_binary_list,length_of_list):
        header_char_size=8
        header_str=""
        for start in range(0,length_of_list,header_char_size):
            temp=header_binary_list[start:start+header_char_size]
            header_str+=chr(self.binary_to_dcible(temp))
        return header_str

    def extract_content(self,content_binary_list,length_of_content):
        content_char_size=8
        content_byte_array=bytearray()
        #print(content_binary_list)
        count=1
        start=0
        while count<=length_of_content:
            temp=content_binary_list[start:start+content_char_size]
            byte=self.binary_to_dcible(temp)
            content_byte_array.append(byte)
            start=start+content_char_size
            count+=1

        return content_byte_array

    def write_msg(self,file_name=None):
        if file_name == None:
            file_name = self.file_name
        file_name += self.file_extension

        with open(file_name, 'wb') as fout:
            fout.write(self.content)






def main():
    m=Message("Ape_Face.bmp")
    #print(m.create_message_header()[8:])
    #print(m.create_message_content())
    #print(m.create_binary_list())
    lis=m.create_binary_list()
    lis=lis+[1,0,0,1,1,1,0,1,0,0,1,0,0,1]
    m.extract_msg(lis)
    # m.extract_msg(
    #     [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0])

if __name__=="__main__":
    main()