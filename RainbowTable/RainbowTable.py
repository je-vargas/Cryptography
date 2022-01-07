import hashlib
import math
from string import ascii_letters
import time
import csv
import sympy
import random


#: ------------- GLOBAL VARIABLES -------------
LENGTH = 3
FILE_CREATED = False
ALPHABET = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

#: ------------- FUNCTIONS -------------

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def create_csv_file(file_name):
    file_name = "RainbowTable/{0}.csv".format(file_name)
    try:    
        with open(file_name, 'x', encoding='UTF8', newline='', ) as f:
            writer = csv.writer(f)
            writer.writerow(["Plaintext", "End_Hash"]) # Table Header
    except Exception as err:
        print(f"File already exists: {err}")
        return

def write_hash_table(dictionary):
    with open('RainbowTable/table.csv', 'a', encoding='UTF8', newline='', ) as f:
        writer = csv.writer(f)
        writer.writerows(table_list) # Table
        for key, value in dictionary.items():
            writer.writerow([key, value])

def read_hash_table():
    read_table = dict()
    with open('RainbowTable/table.csv', 'a', encoding='UTF8', newline='', ) as f:
        read = csv.DictReader(f)
        for row in reader:
            read_table[row["Plaintext"]] = row["End_Hash"]
        print(f"dictionary returned from csv file : {read_table}")


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
    prime = sympy.nextprime(incremented_space)

    print(f"space: {pass_space} \t table size: {table_size} \t prime: {prime}")

    # return pass_space, int(round_half_up(table_size)), prime
    return pass_space, table_size, prime

def hex_sum(hexHash, position, prime_mod):
    hex_sum = 0
    hex_look_up = {"a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
    for a in range(len(hexHash)):
        if hexHash[a].isdigit():
            # hex_sum += (int(hexHash[a]) * position) #% prime
            hex_sum += (int(hexHash[a]) * position) #% prime
        else:
            hx = int(hex_look_up.get(hexHash[a]))
            # hex_sum += (hx * position) #% prime
            hex_sum += (hx * position) #% prime
    hex_sum = hex_sum % prime_mod
    return hex_sum

def weighted_sum(hash_value, position, prime_mod, alphabet_set_len):
    hash_value_length = len(hash_value)
    total = 0
    ascii_list = []
    for i in range(len(hash_value)):
        ascii_list.append(ord(hash_value[i]))
        total += (ascii_list[i] * (alphabet_set_len ** (hash_value_length - i))) #% prime_mod
    # total = (total + position) % prime_mod
    total = (total * position) % prime_mod

    #: think it needs bit shifting based on wrongs algorithm using position to make it different every position
    return total

def int_to_string(n, alphabet_set):
    '''
        #* Returns
        #: maps hex reduction to integer in my space size
    '''
    s = ""
    base = len(alphabet_set)

    while n >= 0:
        r = n % base
        n = n // base
        s = s + str(alphabet_set[r]) 
        n -= 1
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

def reduction(pass_hash, position, prime_mod, alphabet_set_length):
    # maybe use two separate functions
    even_poistion = position % 2
    hash_sum = 0
    if even_poistion:
        hash_sum = weighted_sum(pass_hash, prime, position, alphabet_set_length)
    else:
        hash_sum = hex_sum(pass_hash, position, prime_mod)
    
    return hash_sum

def password_generator(alphabet_set, pass_length):
    rand_password = ""
    print(f"alpha len: {len(alphabet_set)}\n")
    for i in range(pass_length):
        random_char_index = random.randint(0, len(alphabet_set)-1)
        rand_password = rand_password + alphabet_set[random_char_index]
    return rand_password

def build_rainbow_table(table_size, prime_mod, alphabet_set, pass_length):
    number_of_chains = 0
    hash_table = dict()
    chain_end = ""

    while number_of_chains < table_size: 
        random_password = password_generator(alphabet_set, pass_length)
        hash_pass = sha1_encode(random_password)
        for chain_length_position in range(table_size):
            hash_sum = reduction(hash_pass, chain_length_position, prime_mod, len(alphabet_set))
            chain_end = int_to_string(hash_sum, alphabet_set)
            if len(chain_end) > pass_length :
                chain_end = int_to_string(chain_end, alphabet_set)
        
        #: checks if int_to_string is valid
        if chain_end.strip(): raise Exception("reduction method | End of chain is empty needs to be a password in PASS-SPACE!")
        
        #: checks if end of chain already exists if not we add it
        if chain_end not in table: 
            table[chain_end] = chain_start #* dict searches by key -> key must be end of chain
            number_of_chains += 1 
    return table

def read_password_character_set():
    return

    

#* ------------- Code -------------
full_alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# numb_alpha = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
numb_alpha = ['0', '1', '2']

# #: ------- building One chain of x Length for (0-4) length 3
    # space, table_size, prime = password_space_size(len(numb_alpha), 4)
    # password =  password_generator(numb_alpha, 4)
    # # password =  "2211"
    # # password =  "1220"
    # pass_sha = sha1_encode(password)
    # print(f"random pass: {password}\tsha1_pass: {pass_sha}\n")

    # for i in range(12-1):
    #     reduction = weighted_sum(pass_sha, i+1, prime, len(numb_alpha))
    #     # reduction = hex_sum(pass_sha, i+1, prime)
    #     next_chain = int_to_string(reduction, numb_alpha)
    #     if len(next_chain) > 4 :
    #         next_chain = int_to_string(reduction, next_chain)
    #     print(f"next chain : {next_chain}")   
    #     password = sha1_encode(next_chain)
    #     print(f"next hash: {password}")
    #     # print("\n")

#: ------- building table
create_csv_file("table")
lengt_of_alphaset = len(numb_alpha)
pass_length = 3
space, table_size, prime = password_space_size(len(numb_alpha), pass_length)
table = build_rainbow_table(table_size, prime, numb_alpha, pass_length)
write_hash_table(table)







# reduction = hex_sum(password, 5, prime)
    # reduction = weighted_sum(password, prime, i)
    # print(f"hex sum: {reduction}")
    # print(int_to_string(reduction, a))



    







