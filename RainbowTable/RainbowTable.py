import hashlib
import math
from string import ascii_letters
import time
import csv
import sympy
import random

#: ----------- TASK 4 - RAINBOW TABLE ----------- TASK 4 - RAINBOW TABLE ----------- TASK 4 - RAINBOW TABLE -----------

def sha1_encode(password):
    '''
        FUNCTION: sha1_encode
        DEFINITION: Applies SHA1 hash function to string passed in
        PARAMETERS: password: string
        RETURNS: hexidecimal string
    '''
    sha1 = hashlib.sha1(str.encode(password))
    return sha1.hexdigest()

def round_half_up(n, decimals=0):
    '''
        FUNCTION: round_half_up
        DEFINITION: round number to given decimal. decimal set to 0
                    This is being used to round number for search space 
        PARAMETERS: n: int, decimal: int
        RETURNS: int
    '''
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def write_hash_table(dictionary, file_name):
    '''
        FUNCTION: write_hash_table
        DEFINITION: Writes dictionary to a csv file
        PARAMETERS: dictionary: Dictionary, file_name: string
        RETURNS: void
    '''
    with open(file_name, 'a', encoding='UTF8', newline='', ) as f:
        keys = ["chain_end", "chain_start"]
        writer = csv.DictWriter(f, keys)
        writer.writeheader() #* sets the header values of the csv file
        for keys in dictionary.keys():
            f.write("%s,%s\n"%(keys, dictionary[keys])) #* for each chain in the dictionary copy over to cvs file

def read_hash_table(file_name):
    '''
        FUNCTION: read_hash_table
        DEFINITION: Reads csv file containing chains and transforms it into a dictionary
        PARAMETERS: file_name: string
        RETURNS: read_table: dictionary
    '''
    read_table = dict()
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #* Reads each row and stores in the dictionary row by row
            read_table[row['chain_end']] = row['chain_start'] 
    return read_table

def range_numeric_alphabetical(startLetter, endLetter, startInt, endInt):
    '''
        FUNCTION: range_numeric_alphabetical
        DEFINITION: Returns list of alphabettic and numeric range to use for combinations 
                    -> meant to be used to make program more flexible
        PARAMETERS: startLetter: string, endLetter: string, startInt: int, endInt: int
        RETURNS: list of all characters used for password space
    '''
    alpha_numeric_range = ascii_letters[ascii_letters.index(startLetter):ascii_letters.index(endLetter)+1]
    alpha_numeric_range_list = [char for char in alpha_numeric_range]
    for i in range(startInt, endInt+1):
        alpha_numeric_range_list.append(str(i))
    return alpha_numeric_range_list

def password_space_size(alphabet_size, pass_length, table_size_multiplier):
    '''
        FUNCTION: password_space_size
        DEFINITION: Calculates password space size and length of chains and chain lengths
                    Table size is the password space * the multiplier
        PARAMETERS: alphabet_size: int, pass_length: int, table_size_multiplier: float
        RETURNS: table_size: int, prime: int
    '''
    pass_space = 0
    for i in range(alphabet_size):
        pass_space += alphabet_size ** (pass_length - i)
    pass_space += 1
    
    incremented_space = pass_space * table_size_multiplier
    table_size = int(round_half_up(math.sqrt(incremented_space)))
    prime = sympy.nextprime(pass_space)

    print(f"\nspace: {pass_space} \t table size: {table_size} \t prime: {prime}\n")

    return table_size, prime

def hex_sum(hexHash, position, prime_mod):
    '''
        FUNCTION: hex_sum
        DEFINITION: Hexidecimal strng is added to return a unique number
                    made different by multiplying by position passed in
        PARAMETERS: hexHash: string, position: int, prime_mod: int
        RETURNS: hex_sum: int
    '''
    hex_sum = 0
    #* hexidecimal look up table for none integers values
    hex_look_up = {"a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
    for a in range(len(hexHash)):
        #* add each value in the hexidecimal string and multiply by position
        if hexHash[a].isdigit():
            hex_sum += (int(hexHash[a]) * position)
        else:
            hx = int(hex_look_up.get(hexHash[a]))
            hex_sum += (hx * position)
    hex_sum = hex_sum % prime_mod
    return hex_sum

def weighted_sum(hash_value, position, prime_mod, alphabet_set_len):
    '''
        FUNCTION: weighted_sum
        DEFINITION: Reduction function that finds ascii value for each letter in the hash_value
                    and adds it to make a unique number
        PARAMETERS: hash_value: string, position: int, prime_mod: int, alphabet_set_len: int
        RETURNS: total: int
    '''
    #* think it needs bit shifting based on wrongs algorithm using position to make it different every position
    hash_value_length = len(hash_value)
    total = 0
    ascii_list = []

    if position % 2 == 0:
        for i in range(hash_value_length):
            #* add ascii value for string hash_value[i] to ascii_list
            ascii_list.append(ord(hash_value[i]))
            total += (ascii_list[i] * (alphabet_set_len ** (hash_value_length - i))) % prime_mod
        total = (total - position) % prime_mod
    else:
        total = int(hash_value, 16)
        total = (total + position) % prime_mod

    return total

def int_to_string(n, alphabet_set):
    '''
        FUNCTION: int_to_string
        DEFINITION: Maps a big integer into a possible solution for the set password length
        PARAMETERS: n: int, alphabet_set: list(string)
        RETURNS: s: int
    '''
    s = ""
    base = len(alphabet_set)

    while n >= 0:
        remainder = n % base
        n = n // base #* int division
        s = s + str(alphabet_set[remainder]) 
        n = n - 1
    return s

def reduction(pass_hash, position, prime_mod, alphabet_set):
    '''
        FUNCTION: reduction
        DEFINITION: Takes a hash value -> hexidecimal string and returns a possible password in search space
        PARAMETERS: pass_hash: string, position: int, prime_mod: int, alphabet_set: list(string)
        RETURNS: sum_to_passwordSpace: int
    '''
    #* maybe use two separate functions
    sum_ = 0
    sum_ = weighted_sum(pass_hash, position, prime_mod, len(alphabet_set))
    sum_to_passwordSpace = int_to_string(sum_, alphabet_set)

    return sum_to_passwordSpace

def password_generator(alphabet_set, pass_length):
    '''
        FUNCTION: password_generator
        DEFINITION: creates a random password of given length and given character set 
        PARAMETERS: alphabet_set: list(string), pass_length: int
        RETURNS: rand_password: int
    '''
    rand_password = ""
    for i in range(pass_length):
        random_char_index = random.randint(0, len(alphabet_set)-1) #* return a random int from 0 to length of character set 
        rand_password = rand_password + alphabet_set[random_char_index] #* random inde
    return rand_password

def build_rainbow_table(chains, length_chain,  prime_mod, alphabet_set, pass_length):
    '''
        FUNCTION: build_rainbow_table
        DEFINITION: build a set of keys for a rainbow table returned as a dictionary
        PARAMETERS: chains: int, length_chain: int, prime_mod: int, alphabet_set: list(strings), pass_length: int
        RETURNS: hash_table: dictionary
    '''
    number_of_chains = 0
    hash_table = dict()
    hash_ = ""
    counter = 0

    while number_of_chains < chains: #* this while loops keeps track of how many chains have been created
        random_password = password_generator(alphabet_set, pass_length)
        hash_ = sha1_encode(random_password) #* encode random password created
        starting_hash = hash_

        for chain_position in range(1, length_chain): #* this controls the individuals chains length
            int_in_password_space = reduction(hash_, chain_position, prime_mod, alphabet_set)
            hash_ = sha1_encode(int_in_password_space)
            chain_start = hash_
        
        chain_end = random_password
        
        #* add chain if not existen in dictionary already
        if chain_start not in hash_table:
            print(f"addind -> key: {hash_} | value: {random_password}")
            hash_table[chain_start] = chain_end #* dict searches by key -> key must be end of chain
            number_of_chains += 1 #* increment number of chains if a new chain is added
            counter = 0 #* reset counter back 0 
        else:
            counter += 1 #* keeps track of how many solutions have returned none new solutions

        #* if no more solution can be found but we havent satisifed while loop statement return dictionary up to now
        if counter > MAX_COUNTER :
            print(len(hash_table))
            terminate = input("Terminate y/n: ")
            if terminate == "y": return hash_table
            else: counter = 0
            
    return hash_table

def traverse_chain(start_of_chain, chain_length, prime, alphabet):
    '''
        FUNCTION: traverse_chain
        DEFINITION: Builds a whole chain (length) by taking the start value of any chain
        PARAMETERS: start_of_chain: string
        RETURNS: void
    '''
    password = start_of_chain
    hash_ = sha1_encode(password)
    print(f"chain start: {password}\t|hash: {hash_}\tposition: 0")

    for chain_position in range(1, chain_length):
        int_in_password_space = reduction(hash_, chain_position, prime, alphabet)
        hash_ = sha1_encode(int_in_password_space)
        print(f"Reduction: {int_in_password_space}\t|hash: {hash_}\tposition: {chain_position}")  
    print("\n")  

def check_password_exists_in_chain(goal, plaintext, chain_length, prime, alphabet):
    '''
        FUNCTION: check_password_exists_in_chain
        DEFINITION: builds each chain position up to the lenth of the chain length.
                    Checking if the hash solution of each position equals to the goal hash
        PARAMETERS: goal: string, plaintext: string, chain_length: int, prime: int, alphabet: list(string)
        RETURNS: pwd: string, next_hash: string, found_password: boolean
    '''
    found_password = False
    pwd = plaintext
    
    for chain_position in range(1, chain_length+1):
        next_hash = sha1_encode(pwd)

        if next_hash == goal: 
            found_password = True
            return pwd, next_hash, found_password

        pwd = reduction(next_hash, chain_position, prime, alphabet) 

    return pwd, next_hash, found_password

def build_chain_from_position_backwards(use_hash, reduce_position, chain_length, prime, alphabet):
    '''
        FUNCTION: build_chain_from_position_backwards
        DEFINITION: Builds chain backwards from chainlength - reduce position up to 1
        PARAMETERS: use_hash: string, reduce_position: int, chain_length: int, prime: int, alphabet: list(strings)
        RETURNS: pwd: string, next_hash: string, found_password: boolean
    '''
    starting_hash = use_hash
    for position in range(reduce_position, chain_length):
        # print(f"reducing poss: {position}")
        pwd = reduction(starting_hash, position, prime, alphabet)
        hash_value = sha1_encode(pwd)
        starting_hash = hash_value
    # print(f"pwd: {pwd}\t hash: {hash_value}/n")
    return hash_value

def break_password(target, goal, length_of_chain, read_dict, prime, alphabet):
    '''
        FUNCTION: build_chain_from_position_backwards
        DEFINITION: 
        PARAMETERS: target: string, goal: string, length_of_chain: int, read_dict: dictionary, prime: int, alphabet: list(strings)
        RETURNS: void
    '''
    chain_start = ""
    pass_found = False
    find_key = target
    end_position_of_chain = length_of_chain - 1

    while end_position_of_chain >= 0:
        
        #* checks if hash is one of the keys in the dictionary
        if find_key in read_dict:
            chain_start = read_dict[find_key] 
            
            #* check if for the key found any of the chains are equal to goal
            pwd, hash_found, pass_found = check_password_exists_in_chain(goal, chain_start, length_of_chain, prime, alphabet)

            if pass_found:
                print(f"key found: {find_key}\t chain start: {chain_start}\treduced poss: {end_position_of_chain}")
                print(f"\nPASSWORD FOUND: {pwd}\thash: {hash_found}\n") 
                exit() 
        
        find_key = build_chain_from_position_backwards(goal, end_position_of_chain, length_of_chain, prime, alphabet)
        end_position_of_chain -= 1
    
    print("\nPASSWORD NOT FOUND ---- !!")
    exit()

#* #* ------------- CODE ------------- ------------- CODE ------------- ------------- CODE -------------

#* ------------- GLOBAL VARIABLES -------------
# ALPHABET = ['0', '1', '2', '3']
# ALPHABET = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

FILE_NAME = "RainbowTable/8_add_subtract_1.8.csv"

MAX_COUNTER = 500000
# MAX_COUNTER = 500

TABLE_MULTIPLIER = 1.8
# TABLE_MULTIPLIER = 1.3

# CHAINS = 25000 #*8
# C_LENGTH = 8000
CHAINS = 30800 #*8
C_LENGTH = 6500
# CHAINS = 41 #*4
# C_LENGTH = 15 


ALPHABET = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LENGTH = 8
# ALPHABET = ['0', '1', '2', '3']
# LENGTH = 4


table_size, prime = password_space_size(len(ALPHABET), LENGTH, TABLE_MULTIPLIER)

#: ------- building table

# chain = table_size
# c_length = table_size

# table = build_rainbow_table(CHAINS, C_LENGTH, prime, ALPHABET, LENGTH)
# write_hash_table(table, FILE_NAME)

#: ------- building One chain of x Length 
# traverse_chain("0011", table_size, prime, ALPHABET)

# #: ------- cracking password

# goal = "fe635ae88967693bc7e7eead87906e62e472c52f" #* solution: 187494 -> demo 1
# goal = "3ac2d907663deccd843f9bbcf0c63bd3ad885a0e" #* solution: 940376 -> -> demo 1
# goal = "3557c095ed6c16a90febda48d6b3a4490107b0d9" #* solution: 1098368 -> -> demo 1
# goal = "85e04129ed328d4a2b3eedabca74d08b3e6badc1" #* solution: NOT FOUND -> -> demo 1
# goal = "70352f41061eda4ff3c322094af068ba70c3b38b" #* solution: 00000000 -> -> demo 1
# goal = "052bd5b02559d1270866c5626538e720cec0c135" #* solution: 93020840 -> -> demo 1
# goal = "3e71f65d56cb29521ac16ff1f92ecace156b1db5" #* solution: 87657890 -> -> demo 1
# goal = "bfc52d4e36cb45cb667749982755e63630f3bc93" #* solution: 09680243 -> -> demo 1
# goal = "8cb2237d0679ca88db6464eac60da96345513964" #* solution: 12345 -> -> demo 1
# goal = "38bbc0a1ca7e9b3e9f6ab33782e0f780f009db1f" #* solution: 99887766 -> -> demo 1

# goal = "21e4b025b7b858928ec3ce22e373ff5b28df87ad" #* solution: 58493072 -> demo 3
# goal = "d7d5d8b3838452a833f4c6a30a3b9a78cb88e530" #* solution: 0139826 -> demo 3
# goal = "7236da7fee4ddcb8c389b9732e78c7c4e1fcc1e4" #* solution: 60248677 -> demo 3
# goal = "564831f5a86d1d0b8f465042c6e17c4e7d1a1e7d" #* solution: NOT FOUND -> demo 3
# goal = "7f06bee6c1214d732a9e40765bfae0aa3e547c09" #* solution: 34284930 -> demo 3
# goal = "6ec7be98bca5d1812fa41dbb719b552d01c253f7" #* solution: 76422585 -> demo 3
# goal = "cedd8db553409b282deb6ca276203c5edd6f0971" #* solution: 36432700 -> demo 3
# goal = "8bc2059150084f16ad065924444d552ce521c090" #* solution: 09385847 -> demo 3
# goal = "886e177c49dc6dd72176e1be8ba5f4f907f54883" #* solution: 23216780 -> demo 3
# goal = "911a45dec90e5ee1d4f5acc8ce17c8068c9512b0" #* solution: 5927477 -> demo 3
# goal = sha1_encode(plaintext)

read_dict = read_hash_table(FILE_NAME)
print(f"goal: {goal}\thash: {goal}\n")
break_password(goal, goal, C_LENGTH, read_dict, prime, ALPHABET)








    







