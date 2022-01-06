import hashlib
import math
from string import ascii_letters
import time
import csv
import sympy


#: ------------- GLOBAL VARIABLES -------------
LENGTH = 3
FILE_CREATED = False

#: ------------- FUNCTIONS -------------
def create_csv_file(file_name):
    file_name = "RainbowTable/{0}.csv".format(file_name)
    try:    
        with open(file_name, 'x', encoding='UTF8', newline='', ) as f:
            writer = csv.writer(f)
            writer.writerow(["Plaintext", "End_Hash"]) # Table Header
    except Exception as err:
        print(f"File already exists: {err}")
        return

def write_hash_table(table_list):
    
    with open('RainbowTable/table.csv', 'a', encoding='UTF8', newline='', ) as f:
        writer = csv.writer(f)
        writer.writerows(table_list) # Table

def sha1_encode(password):
    sha1 = hashlib.sha1(str.encode(password))
    return sha1.hexdigest()

def password_space_size(alphabet_size, pass_length):
    '''
        #* returns: 
            #: size of password space -> possible combinations
            #: length of chain and number of chains
            #* table size ^ * 1.3 or 1.5
    '''
    pass_space = 0
    space_calc = 0
    for i in range(alphabet_size):
        space_calc += pow(alphabet_size, pass_length)
        pass_space = pass_space + space_calc

    # pass_space = pow(alphabet_size, pass_length)
    incremented_space = pass_space * 1.3
    table_size = math.sqrt(incremented_space)
    prime = sympy.nextprime(incremented_space)
    return pass_space, round_half_up(table_size), prime

def hex_sum(hexHash, position, prime_mod):
    hex_sum = 0
    hex_look_up = {"a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
    for a in range(len(hexHash)):
        if hexHash[a].isdigit():
            hex_sum += (int(hexHash[a]) * position) #% prime
        else:
            hx = int(hex_look_up.get(hexHash[a]))
            hex_sum += (hx * position) #% prime
    hex_sum = hex_sum % prime_mod
    return hex_sum

def weighted_sum(hashValue, position, prime_mod):
    n = hashValue
    total = 0
    ascii_list = []
    for i in range(len(n)):
        ascii_list.append(ord(n[i]))
        total += (ascii_list[i] * (4 ** len(n) - i)) #% prime
    total = (total * position) % prime_mod

    #: think it needs bit shifting based on wrongs algorithm using position to make it different every position
    return total

def int_to_string(n, alphabet):
    '''
        #* Returns
        #: maps hex reduction to integer in my space size
    '''
    s = ""
    base = len(alphabet)

    while n >= 0:
        r = n % base
        s = str(alphabet[r]) + s
        n = n // base
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
        r = n % base
        s = str(alphabet[r]) + s
        check = n / base
        n = n // base
        if n == 0: break
    return s

def reduction(pass_hash, position, prime_mod):
    # maybe use two separate functions
    even_poistion = position % 2
    hash_sum = 0
    if even_poistion:
        hash_sum = weighted_sum(pass_hash, prime, position)
    else:
        hash_sum = hex_sum(pass_hash, position, prime_mod)
    
    pass_in_pass_space = int_to_string(n, alphabet)
    return pass_in_pass_space

#* ------------- Code -------------
# create_csv_file("table")
# write_hash_table([])
a = ["a", "b", "c", "d"]
#: ------- building table for (0-4) length 3
space, table_size, prime = password_space_size(len(a), 3)


print(f"space: {space} \t table size: {table_size} \t prime: {prime}")

pss = "ddd"
password = sha1_encode(pss)
print(f"start password: {pss}\nstart hash: {password}")
# reduction = hex_sum(password, 5, prime)
# reduction = weighted_sum(password, prime, i)
# print(f"hex sum: {reduction}")
# print(int_to_string(reduction, a))

for i in range(9):
    # reduction = hex_sum(password, i+1, prime)
    reduction = weighted_sum(password, prime, i+1)
    # next_chain = int_to_string(reduction, a)
    next_chain = int_to_string_fixed_length(reduction, a)
    print(f"next chain : {next_chain}")   
    password = sha1_encode(next_chain)
    print(f"next hash: {password}")

    







