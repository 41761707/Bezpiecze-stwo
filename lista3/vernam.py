#Radoslaw Wojtczak, nr indeksu:254607
#Bezpieczenstwo Komputerowe
#Lista 3

import string
import collections
import sys
    

def XOR_text(text_one_array,text_two_array):
    text_one=" ".join(text_one_array)
    text_two=""
    if (type(text_two_array)==list):
        text_two=" ".join(text_two_array)
    if(type(text_two_array)==str):
        text_two=text_two_array
    decode=""
    length=min(len(text_one),len(text_two))
    for i in range(length):
        if(text_one[i]==' '):
            decode=decode+" "
            continue
        if(bool(int(text_one[i])) ^ bool(int(text_two[i]))):
            decode=decode+"1"
        else:
            decode=decode+"0"
    product=decode.split(" ")
    return product








def main():
    l=int(sys.argv[1])
    possibleSpaces=int(sys.argv[2])
    ciphers=[]
    texts=[]
    final_cipher="11110000 11000100 01101001 11001001 11010000 10111000 01010100 10010011 10001100 11000000 01000101 00110010 01010011 01001011 10011000 00010111 01101000 10110101 11011010 10010100 01100010 10011101 10111111 00011001 01100111 01011110 11011101 11100010 00000111 11101100 00111111 10011000 00010000 11001011 11011101 10011001 00010000 11111110 01100101 11000010 00101111 01011010 00010000 10101100 11110111 00100111 00001101 10100101 10110110 10011011 00100010 10011101 11001001 01110010 11010001 00111110 11001111 01010100 01101101 00011101 10010101 11110111 10001001 00001110 10111101 10101000 00010011 01010111 10101000 01010110 00101111 10001100 01000010 11100011 00001110 00101111 11111010 00101100 10111110 11100000 10101100 00100100 01111011"
    target_cipher=final_cipher.split(" ")
    for i in range(l):
        filename="text"+str(((i)%l)+1)+".txt"
        f=open(filename,"r")
        texts.append(f.read())
    for i in range(l):
        array=texts[i].split(" ")
        ciphers.append(array)
    final_key=[None]*max(len(text) for text in texts)
    known_key_positions=set()
    for current_index,ciphertext in enumerate(ciphers):
        counter=collections.Counter()
        for index,ciphertext2 in enumerate(ciphers):
            if current_index!=index:
                text_xor=XOR_text(ciphertext,ciphertext2)
                for indexOfChar, char in enumerate(text_xor):
                    a=chr(int(char,2))
                    if a in string.printable and a.isalpha():
                        counter[indexOfChar]+=1
        knownSpaceIndexes=[]

        for ind,val in counter.items():
            if val >= possibleSpaces:
                knownSpaceIndexes.append(ind)

        spaces="00100000 "*len(ciphertext)
        xor_with_spaces=XOR_text(ciphertext,spaces)
        for index in knownSpaceIndexes:
            final_key[index]=xor_with_spaces[index]
            known_key_positions.add(index)
    final_key_bin=" ".join([val if val is not None else '00000000' for val in final_key])
    output=XOR_text(target_cipher,final_key_bin)
    #output=XOR_text(target_cipher,final_key_bin)
    finish=""
    unknown=0
    for index,item in enumerate(output):
        if(index in known_key_positions):
            new=chr(int(item,2))
            finish=finish+new
        else:
            unknown=unknown+1
            finish=finish+"*"
    print(finish)
    print("Liczba nieznanych wzgledem dlugosci tekstu: ",100-(unknown/len(finish)*100),"%")
    '''
    for i in range(l):
        output2=XOR_text(ciphers[i],final_key_bin)
        finish=""
        for index,item in enumerate(output2):
            if(index in known_key_positions):
                new=chr(int(item,2))
                finish=finish+new
            else:
                finish=finish+"*"
        print(finish)
    '''
    '''
    finish=""
    for item in output:
        new=chr(int(item,2))
        finish=finish+new
    print(finish)
    '''



if __name__=='__main__':
    main()

