from Crypto.Cipher import AES   #import AES functions from PyCrypto
import binascii                 #Library for Hex to Binary
import string
import time
from joblib import Parallel, delayed   #Library for running parallel loops
import multiprocessing                 #Library for multiprocessing

def gen_all_hex():    #function to generate all hex value combinations
    i = 0    #initialize i
    while i < 16**4:    #loop until all 16^4 combinations are found
        yield "{:04x}".format(i).upper()    #{:04x} means pad zeroes to the left, max width is 4, x is to make it hex
        i += 1    #increment i

missingkey = '639404CBD1A1BD2322B206C39140'    #key with missing bits
hexciphertext = '5A052F928464CC3E437187ADCFC7E8F1CF9DEAC7059B5264E4E940D8C35AA60E2277D4832843043F593F40E4084609C886681BCF5B570D353BFF24C0E1F4A65E'
lowercase = list(string.lowercase[:26])
uppercase = list(string.uppercase[:26])
digits = list(string.digits[:10])
punctuation = [',', '.', ' ']
allowed = lowercase + uppercase + digits + punctuation    #array with all allowed ascii characters
check = 0    #setting check bit to zero. If it becomes 1, correct plaintext is found, code terminates

def decryption(s, check, missingkey, hexciphertext):    #create the decryption function
    fullkey = missingkey + s    #fullkey is missingkey concatenated with all hex combinations
    binarykey = binascii.unhexlify(fullkey)    #take the full key and convert it to binary
    obj = AES.new(binarykey, AES.MODE_ECB)    #pass the binary key into AES, set it to ECB mode
    binciphertext = binascii.unhexlify(hexciphertext)    #we must also convert the ciphertext from hex to binary
    plaintext = obj.decrypt(binciphertext)    #pass ciphertext into pycrypto AES and decrypt with the key
    splittext = list(plaintext)    #split the plaintext you get into an array of characters
    counter = 0    #this counter checks how many characters match the allowed ascii characters
    for index, i in enumerate(splittext):    #this for loop iterates through indices of splittext
         for j in allowed:    #also iterate through all allowed ascii characters
            if index <= 19:    #we will check only the first 20 characters (index for python starts at 0)
                if i == j:    #if the character in splittext matches any of the allowed ascii characters...
                    counter += 1    #increment the counter
                    if counter == 20:    #if we find a string with 20 consecutive character matches....
                        check += 1    #raise the check bit to 1
                        if check == 1:    #if check bit is raised to 1....
                            print plaintext    #we found the plaintext, print it
                            print 'Missing Key Bits: ' + s    #also print the missing key bits
                            break    #terminate the code

if __name__ == '__main__':    #this is the syntax used to start multiprocessing
    num_cores = multiprocessing.cpu_count()    #count the number of cores available
    start_time = time.time()    #start the timer
    results = Parallel(n_jobs=num_cores)(delayed(decryption)(s, check, missingkey, hexciphertext) for s in gen_all_hex())
    #depending on number of cores, set the number of jobs
    #run the decryption function while passing all needed variables into the function
    #run this function for all possible combinations of hex until the decryption is successful
    end_time = time.time()    #stop the timer
    print 'Time Elapsed: ' + "{0:.3f}".format(end_time - start_time) + ' seconds'    #print the time elapsed

########################################################################################################################
#                                                       END OF CODE                                                    #
########################################################################################################################