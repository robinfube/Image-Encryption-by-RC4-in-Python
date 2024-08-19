from PIL import Image
import numpy as np

#initialize state array S in the below function using Key Scheduling Algorithm for generating keystream by picking size of integer S
def Initialize(key):
    S=list(range(256))
    j=0
    for i in range(256):
        j=(j+S[i]+key[i%len(key)])%256
        S[i],S[j]=S[j],S[i]
        return S

#Generating keystream using Pseudo Random Generation Algorithm
def GenerateKeyStream(S,data_length):
    i=0
    j=0
    keystream=[]
    
    #Length of data for encrypt or decrypting purpose
    for _ in range(data_length):
        i=(i+1)%256
        j=(j+S[i])%256
        S[i],S[j]=S[j],S[i]
        keystream.append(S[(S[i]+S[j])%256])
        
    return keystream
    


def imageEncrypt_Decrypt(img_path,key):
    img=Image.open(img_path)

    #converting image into multi dimensional array and flattening them into single dimensional array
    img_data = np.array(img).flatten()

    #convert key  into integers list by iterating over character and return Unicode point of each representing character

    key=[ord(c) for c in key]
    
    #initialize state array
    S=Initialize(key)

    keystream=GenerateKeyStream(S,len(img_data))

    #XORing byte of data with keystream
    result_data=np.array([data_byte ^ keystream_byte for data_byte,keystream_byte in zip(img_data,keystream)],dtype=np.uint8)

    #Reshape flat array back to original image where size[0] represent image width and s[1] represent height
    result_img_array=result_data.reshape(img.size[1],img.size[0],-1)
    result_img=Image.fromarray(result_img_array,img.mode)

    return result_img

def main():
    count=0
    key="20010b91001i91001i70111g91001i20010b40100d50101e81000h"

    print("type encrypt for encryption or decrypt for decryption\n")
    action=input("Do you want to encrypt or decrypt the image?").strip().lower()
    img_path=input("Enter the path of the image file:").strip()

    #key=input("Enter the custom key if you want").strip()

    if action == 'encrypt':
        result_img=imageEncrypt_Decrypt(img_path,key)
        result_img.save(f'encryptedimage{count}.png')
        count=count+1
        print(f"Image encryption successful and saved  as 'encrypted_image{count}.png'\n")
        
    elif action == 'decrypt':
        result_img=imageEncrypt_Decrypt(img_path,key)
        result_img.save(f'decryptedimage{count}.png')
        print(f"Image decryption successful and saved as 'decrypted_image{count}.png'\n")

    else :
        print("Please enter appropriate command")


if __name__=="__main__":
    main()