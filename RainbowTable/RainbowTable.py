import hashlib
import math
from string import ascii_letters
import time
import csv
import sympy
import random


#: ------------- GLOBAL VARIABLES -------------
FILE_CREATED = False
ALPHABET = ['0', '1', '2']
# ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# ALPHABET = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# LENGTH = 3
# ALPHABET = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

#: ------------- FUNCTIONS -------------

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def create_csv_file(file_name):
    file_name = "RainbowTable/{0}.csv".format(file_name)
    keys = ["chain_end", "chain_start"]
    try:    
        with open(file_name, 'x', encoding='UTF8', newline='', ) as f:
            writer = csv.DictWriter(f, keys)
            writer.writeheader()
    except Exception as err:
        print(f"File already exists: {err}")
        return

def write_hash_table(dictionary):
    with open('RainbowTable/table.csv', 'a', encoding='UTF8', newline='', ) as f:
        for keys in dictionary.keys():
            f.write("%s,%s\n"%(keys, dictionary[keys]))

def read_hash_table():
    read_table = dict()
    with open('RainbowTable/table.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            read_table[row['chain_end']] = row['chain_start']
    return read_table

def sha1_encode(password):
    sha1 = hashlib.sha1(str.encode(password))
    return sha1.hexdigest()

def range_numeric_alphabetical(startLetter, endLetter, startInt, endInt):
    "definition: returns list of alphabettic and numeric range to use for combinations"
    alpha_numeric_range = ascii_letters[ascii_letters.index(startLetter):ascii_letters.index(endLetter)+1]
    alpha_numeric_range_list = [char for char in alpha_numeric_range]
    for i in range(startInt, endInt+1):
        alpha_numeric_range_list.append(str(i))
    return alpha_numeric_range_list

def password_space_size(alphabet_size, pass_length):
    '''
        #* returns: 
            #: size of password space -> possible combinations
            #: length of chain and number of chains
            #* table size ^ * 1.3 or 1.5
    '''
    pass_space = 0
    for i in range(alphabet_size):
        # print(f"power : {pass_length - i}")
        pass_space += alphabet_size ** (pass_length - i)

    incremented_space = pass_space * 1.3
    table_size = int(round_half_up(math.sqrt(incremented_space)))
    # prime = sympy.nextprime(incremented_space)
    prime = sympy.nextprime(pass_space)

    print(f"\nspace: {pass_space} \t table size: {table_size} \t prime: {prime}\n")

    return table_size, prime

def hex_sum(hexHash, position, prime_mod):
    hex_sum = 0
    hex_look_up = {"a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
    for a in range(len(hexHash)):
        if hexHash[a].isdigit():
            hex_sum += (int(hexHash[a]) * position)
        else:
            hx = int(hex_look_up.get(hexHash[a]))
            hex_sum += (hx * position)
    hex_sum = hex_sum % prime_mod
    return hex_sum

def weighted_sum(hash_value, position, prime_mod, alphabet_set_len):
    #* think it needs bit shifting based on wrongs algorithm using position to make it different every position
    hash_value_length = len(hash_value)
    total = 0
    ascii_list = []
    for i in range(hash_value_length):
        ascii_list.append(ord(hash_value[i]))
        total += (ascii_list[i] * (alphabet_set_len ** (hash_value_length - i))) #% prime_mod
    total = (total * position) % prime_mod

    return total

def int_to_string(n, alphabet_set, pass_length):
    s = ""
    base = len(alphabet_set)

    while n >= 0:
        remainder = n % base
        n = n // base
        s = s + str(alphabet_set[remainder]) 
        n = n - 1
    return s

def int_to_string_fixed_length(n, alphabet):
    '''
        #* Returns
        #: maps hex reduction to integer in my space size
    '''
    s = ""
    base = len(alphabet)

    while n >= 0:
        check = n // base
        r = n % base
        s = str(alphabet[r]) + s
        n = n // base
    return s


# def add_chain_to_hash_table(table, chain_end, chain_start):
#     existing_key = True
#     if chain_end in table: return table, existing_key
    
#     table[chain_end] = chain_start #* dict searches by key -> key must be end of chain
#     existing_key = False
#     return table, existing_key


def reduction(pass_hash, position, prime_mod, alphabet_set):
    #* maybe use two separate functions
    sum_ = 0
    sum_ = weighted_sum(pass_hash, position, prime_mod, len(alphabet_set))

    if sum_ < 1: print("weigted sum returned 0\n")
    sum_to_passwordSpace = int_to_string(sum_, alphabet_set, pass_length)
    
    # if len(sum_to_passwordSpace) > len(alphabet_set): print(f"weighted_sum: {sum_}\tform this hash : {pass_hash} | maps to int : {sum_to_passwordSpace}")

    return sum_to_passwordSpace

def password_generator(alphabet_set, pass_length):
    rand_password = ""
    for i in range(pass_length):
        random_char_index = random.randint(0, len(alphabet_set)-1)
        rand_password = rand_password + alphabet_set[random_char_index]
    return rand_password

def build_rainbow_table(table_size, prime_mod, alphabet_set, pass_length):
    number_of_chains = 0
    hash_table = dict()
    chain_length = dict()
    hash_ = ""

    while number_of_chains < table_size: 
        random_password = password_generator(alphabet_set, pass_length)
        hash_ = sha1_encode(random_password)
        starting_hash = hash_
        # chain_length[random_password] = [starting_hash]

        for chain_length in range(table_size - 1):
            position = chain_length + 1
            int_in_password_space = reduction(hash_, position, prime_mod, alphabet_set)

            # if len(int_in_password_space) > len(alphabet_set): print(f"{random_password} password after chains returned number bigger \n")
            # print(f"Reduction: {int_in_password_space}\t| hash: {hash_}")

            hash_ = sha1_encode(int_in_password_space)
            # chain_length[int_in_password_space] = hash_
            chain_start = hash_
        
        chain_end = random_password
        
        #: add chain if not existen
        if hash_ not in hash_table:
            print(f"addind key: {hash_} | value: {random_password}")
            print("------------------------\n") 
            hash_table[chain_start] = chain_end #* dict searches by key -> key must be end of chain
            number_of_chains += 1 
            
    return hash_table

def chain_reduce(pass_hash, position, prime, table_size, alphabet):
    next_chain = ""
    
    if pass_hash in read_dict:
        next_chain = read_dict[pass_hash] #* if match return start of chain
        if len(next_chain) < 1 : print(f"next chain is empty")
        print("found password beggining of func\n")
    else: 
        next_chain = pass_hash
        pwd = reduction(next_chain, position, prime, alphabet)
        
        while (position != table_size-1): #the last position of the chain):
            
            position += 1
            next_chain = sha1_encode(pwd)

            if next_chain in read_dict:
                next_chain = read_dict[next_chain] #* if match return start of chain
                print(f"found password: {pwd}\n")
                break
            else:
                pwd = reduction(next_chain, position, prime, alphabet) #* R at pos
            
        return pwd

def crack(chain_start, prime, table_size, alphabet):
    # chain_start = read_dict[chain_start] #* if match return start of chain

    # if len(chain_start) > 0: chain_start = sha1_encode(chain_start) 

    return chain_reduce(chain_start, 1, prime, table_size, alphabet)
    

#* ------------- Code -------------


# # : ------- building One chain of x Length for (0-4) length 3
# # password =  "000"
# # # password =  "1100" #: length 3
# # # password =  "2211"
# # # password =  "1220"
# # # password =  "1220"

# lengt_of_alphaset = len(ALPHABET)
    # pass_length = 8
    # table_size, prime_mod = password_space_size(lengt_of_alphaset, pass_length) #* 👍 not including " " as we dont generate space as password
    # chain_length = dict()
    # # password = "222"
    # # password = "020"
    # password = "221"
    # hash_ = sha1_encode(password)

    # for chain_length in range(table_size - 1):
    #     position = chain_length + 1
    #     int_in_password_space = reduction(hash_, position, prime_mod, ALPHABET)

    #     if len(int_in_password_space) > len(ALPHABET): print(f"{password} password after chains returned number bigger \n")

    #     hash_ = sha1_encode(int_in_password_space)
    #     print(f"Reduction: {int_in_password_space}\t| hash: {hash_}")


#: ------- building table
lengt_of_alphaset = len(ALPHABET)
pass_length = 3

# create_csv_file("table") #:* 👍
table_size, prime = password_space_size(lengt_of_alphaset, pass_length) #* 👍 not including " " as we dont generate space as password
# table = build_rainbow_table(table_size, prime, ALPHABET, pass_length)
# write_hash_table(table)


#: ------- cracking password
read_dict = read_hash_table()
# pass_ = sha1_encode("103")
# pass_ = sha1_encode("121") #end hash value
# pass_ = sha1_encode("01") #end hash value
pass_ = sha1_encode("112") #end hash value

chain_start = ""
position = 1

if pass_ in read_dict:
    # crack()
    chain_start = read_dict[pass_] #* if match return start of chain

    if len(chain_start) > 0: chain_start = sha1_encode(chain_start) 

    pwd = chain_reduce(chain_start, 1, prime, table_size, ALPHABET)
    print(f"found ?: {pwd}")
    
else:
    next_chain = pass_
    while (position != table_size): #the last position of the chain):
        
        pwd = reduction(next_chain, position, prime, ALPHABET) #* R at pos
        next_chain = sha1_encode(pwd)

        if next_chain in read_dict:
            next_chain = read_dict[next_chain] #* if match return start of chain
            next_chain = sha1_encode(next_chain)
            pwd = crack(next_chain, prime, table_size, ALPHABET)
            print(f"found password {pwd}")
            break
        
        position+= 1







    







