import hashlib
import math
from string import ascii_letters
import time
import csv
import sympy
import random


#: ------------- GLOBAL VARIABLES -------------
FILE_CREATED = False
MAX_TRY_COUNTER = 500
LARGEST_PWD = "99999999"
# LARGEST_PWD = "3333"


# ALPHABET = ['0', '1', '2', '3']
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# ALPHABET = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

LENGTH = 8
# LENGTH = 4
# TABLE_MULTIPLIER = 1.3
# TABLE_MULTIPLIER = 1.6
TABLE_MULTIPLIER = 2.0

#: ------------- FUNCTIONS -------------

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def create_csv_file(file_name):
    keys = ["chain_end", "chain_start"]
    try:    
        with open(file_name, 'x', encoding='UTF8', newline='', ) as f:
            writer = csv.DictWriter(f, keys)
            writer.writeheader()
    except Exception as err:
        print(f"File already exists: {err}")
        return

def write_hash_table(dictionary, file_name):
    with open(file_name, 'a', encoding='UTF8', newline='', ) as f:
        for keys in dictionary.keys():
            f.write("%s,%s\n"%(keys, dictionary[keys]))

def read_hash_table(file_name):
    read_table = dict()
    with open(file_name, newline='') as csvfile:
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

def password_space_size(alphabet_size, pass_length, table_size_multiplier):
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
    pass_space += 1
    incremented_space = pass_space * table_size_multiplier
    table_size = int(round_half_up(math.sqrt(incremented_space)))
    # prime = sympy.nextprime(pass_space)
    prime = sympy.nextprime(LARGEST_PWD)#: force prime that will return a value <= 8 and not bigger
    
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
    total = (total + position) % prime_mod

    return total

def int_to_string(n, alphabet_set):
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

def reduction(pass_hash, position, prime_mod, alphabet_set):
    #* maybe use two separate functions
    sum_ = 0
    sum_ = weighted_sum(pass_hash, position, prime_mod, len(alphabet_set))
    # if sum_ < 1: print("weigted sum returned 0\n")
    sum_to_passwordSpace = int_to_string(sum_, alphabet_set)
    # if len(sum_to_passwordSpace) > len(alphabet_set): print(f"weighted_sum: {sum_}\tform this hash : {pass_hash} | maps to int : {sum_to_passwordSpace}")

    return sum_to_passwordSpace

def password_generator(alphabet_set, pass_length):
    rand_password = ""
    for i in range(pass_length):
        random_char_index = random.randint(0, len(alphabet_set)-1)
        rand_password = rand_password + alphabet_set[random_char_index]
    return rand_password

def build_rainbow_table_dynamically(table_size, prime_mod, alphabet_set, pass_length):
    number_of_chains = 0
    hash_table = dict()
    hash_ = ""

    while number_of_chains < table_size: 
        random_password = password_generator(alphabet_set, pass_length)
        hash_ = sha1_encode(random_password)
        starting_hash = hash_

        for chain_length in range(table_size - 1):
            position = chain_length + 1
            int_in_password_space = reduction(hash_, position, prime_mod, alphabet_set)

            # if len(int_in_password_space) > len(alphabet_set): print(f"{random_password} password after chains returned number bigger \n")
            # print(f"Reduction: {int_in_password_space}\t| hash: {hash_}"

            hash_ = sha1_encode(int_in_password_space)
            chain_start = hash_
        
        chain_end = random_password
        
        #: add chain if not existen
        if hash_ not in hash_table:
            print(f"addind key: {hash_} | value: {random_password}")
            hash_table[chain_start] = chain_end #* dict searches by key -> key must be end of chain
            number_of_chains += 1 
            
    return hash_table

def build_rainbow_table_set_value(chains, chain_length, prime_mod, alphabet_set, pass_length):
    number_of_chains = 0
    hash_table = dict()
    hash_ = ""
    try_counter = 0

    while number_of_chains < chains: 
        random_password = password_generator(alphabet_set, pass_length)
        hash_ = sha1_encode(random_password)
        starting_hash = hash_

        #* chainlength - 1 becasue random password is considered -> makes it desired length
        for chain_length in range(chain_length - 1):
            position = chain_length + 1
            int_in_password_space = reduction(hash_, position, prime_mod, alphabet_set)

            if len(int_in_password_space) > len(alphabet_set): print(f"{random_password} password after chains returned number bigger \n")

            hash_ = sha1_encode(int_in_password_space)
            chain_start = hash_
        
        chain_end = random_password
        
        #: add chain if not existen
        if hash_ not in hash_table:
            print(f"addind key: {hash_} | value: {random_password}")
            hash_table[chain_start] = chain_end #* dict searches by key -> key must be end of chain
            number_of_chains += 1 
            try_counter = 0
        
        #* used to prevent infinte loop trying to meet number of chains
        if try_counter == MAX_TRY_COUNTER: return hash_table
            
    return hash_table

def traverse_chain(start_of_chain):
    '''
        definition: builds the length of a chain used to check values in chain
    '''
    lengt_of_alphaset = len(ALPHABET)
    pass_length = LENGTH
    table_multiplier = TABLE_MULTIPLIER
    table_size, prime_mod = password_space_size(lengt_of_alphaset, pass_length, table_multiplier) #* not including " " as we dont generate space as password
    chain_length = dict()
    password = start_of_chain
    hash_ = sha1_encode(password)
    position = 1
    print(f"chain start: {password}\t|hash: {hash_}\tposition: 0")

    for chain_length in range(table_size - 1):
        
        int_in_password_space = reduction(hash_, position, prime_mod, ALPHABET)

        # if len(int_in_password_space) > len(ALPHABET): print(f"{password} password after chains returned number bigger \n")

        hash_ = sha1_encode(int_in_password_space)
        print(f"Reduction: {int_in_password_space}\t|hash: {hash_}\tposition: {position}")    
        position += 1

def chain_reduce(target, plaintext, prime, table_size, alphabet):
    #: reduce chain and check against target
    pwd = plaintext
    found_password = False
    position = 0
    
    while (position < table_size): #the last position of the chain):
        
        next_hash = sha1_encode(pwd)

        if next_hash == target: 
            # print(f"pwd: {pwd}\t hash: {next_hash}")
            found_password = True
            return pwd, next_hash, found_password

        position += 1
        pwd = reduction(next_hash, position, prime, alphabet) #* R at pos

    return pwd, next_hash, found_password

def build_chain_from_position(use_hash, position, chain_length, prime, alphabet):
    starting_hash = use_hash
    for position in range(position, chain_length):
        # print(f"reducing poss: {position}")
        pwd = reduction(starting_hash, position, prime, alphabet)
        hash_value = sha1_encode(pwd)
        starting_hash = hash_value
    # print(f"pwd: {pwd}\t hash: {hash_value}\n")
    return hash_value

def break_password(target, goal, position, read_dict, table_size, prime, alphabet):
    pass_found = False
    find_key = target
    new_possition = position

    while new_possition > 0 :

        if find_key in read_dict:
            chain_start = read_dict[find_key] #* hash in look up table return start of that chain
            print(f"key found: {find_key}\t init: {chain_start}\treducing from position: {new_possition}")
            
            pwd, hash_found, pass_found= chain_reduce(goal, chain_start, prime, table_size, alphabet)

            if pass_found:    
                print(f"\n----- :) PASSWORD FOUND: {pwd}\tHash: {hash_found}\n") 
                exit() 
        
        find_key = build_chain_from_position(goal, new_possition, table_size, prime, alphabet)
        new_possition -= 1

    print("\n!! ----- PASSWORD NOT FOUND ----- !!\n")
    exit()

#* #* ------------- CODE ------------- ------------- CODE ------------- ------------- CODE -------------


#: ------- building One chain of x Length 

# traverse_chain("1033")

#* ------- building table length 4

lengt_of_alphaset = len(ALPHABET)
pass_length = 4

create_csv_file("RainbowTable/table_length_4_adding_2.3.csv") 
table_size, prime = password_space_size(lengt_of_alphaset, pass_length, TABLE_MULTIPLIER) #* not including " " as we dont generate space as password
table = build_rainbow_table_dynamically(table_size, prime, ALPHABET, pass_length)
write_hash_table(table, "RainbowTable/table_length_4_adding_2.3.csv")

#* ------- cracking password length 4
# plaintext = "0303"
# plaintext = "0210"
# plaintext = "0001"
# plaintext = "1042"
# plaintext = "012"


# goal = sha1_encode(plaintext)

# read_dict = read_hash_table("RainbowTable/table_length_4_adding_2.3.csv") #* read table
# table_size, prime = password_space_size(len(ALPHABET), LENGTH, TABLE_MULTIPLIER)
# starting_position = table_size -1
# print(f"goal: {plaintext}\thash: {goal}\n")
# break_password(goal, goal, starting_position, read_dict, table_size, prime, ALPHABET)

#: ------- building table length 8 range 0-9

# lengt_of_alphaset = len(ALPHABET)

# create_csv_file("RainbowTable/table_2.4_adding.csv") 
# table_size, prime = password_space_size(lengt_of_alphaset, LENGTH, TABLE_MULTIPLIER)
# table = build_rainbow_table_dynamically(table_size, prime, ALPHABET, pass_length)
# write_hash_table(table, "RainbowTable/table_2.4_adding.csv")
# exit()

# #: ------- cracking password length 8 range 0-9


# goal = ""

# read_dict = read_hash_table("RainbowTable/table_2.4_adding.csv") #* read table
# table_size, prime = password_space_size(len(ALPHABET), LENGTH, TABLE_MULTIPLIER)
# starting_position = table_size -1
# print(f"goal: {plaintext}\thash: {goal}\n")
# break_password(goal, goal, starting_position, read_dict, table_size, prime, ALPHABET)


# 100000001
# 111111113










    







