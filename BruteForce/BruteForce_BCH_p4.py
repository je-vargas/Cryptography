import hashlib
import math
from string import ascii_letters
import itertools # --use this for permutations
import time
import bch_checker as bch

#: ----------- TASK 3 - BRUTE FORCE ----------- TASK 3 - BRUTE FORCE ----------- TASK 3 - BRUTE FORCE -----------

def sha1_encode(password):
    '''
        FUNCTION: sha1_encode
        DEFINITION: Applies SHA1 hash function to string passed in
        PARAMETERS: password: string
        RETURNS: hexidecimal string
    '''
    sha1 = hashlib.sha1(str.encode(password))
    return sha1.hexdigest()

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

def test(target, possibleSolution, start):
    '''
        FUNCTION: test
        DEFINITION: checks to see if the target hash has been found. 
                    start time is used to calculate how long it takes to find a password
        PARAMETERS: target: string, possibleSolution: string, start: float
        RETURNS: void
    '''
    #* solution found is encoded using SHA1 and checked against target
    encodedSolution = sha1_encode(possibleSolution)
    if target == encodedSolution:
        end = time.time()
        print("solution found : {0}".format(possibleSolution))
        print(f"Runtime of the program is {end - start}")
        exit()

def test_bch_hash(target, possibleSolution, start):
    '''
        FUNCTION: test_bch_hash
        DEFINITION: checks to see if the target hash has been found.
                    start time is used to calculate how long it takes to find a password
                    used for checking BCH brute force
        PARAMETERS: target: string, possibleSolution: string, start: float
        RETURNS: void
    '''
    encodedSolution = sha1_encode(possibleSolution)
    if target == encodedSolution:
        print(f"target: {target} - solution: {possibleSolution}")
        end = time.time()
        print("solution found : {0}".format(possibleSolution))
        print(f"Runtime of the program is {end - start}")
        exit()

def brute_force_alpha_numeric(target, alphaNumericList, startTime):
    '''
        FUNCTION: brute_force_alpha_numeric
        DEFINITION: builds all the possible combinations for password length of 6 using the alphabet / numbers passed n
        PARAMETERS: target: string, alphaNumericList: list(string), startTime: float
        RETURNS: void
    '''
    startingSet = alphaNumericList
    sizeOfSet = len(alphaNumericList)
    
    #* bredth search building all single solutions first and moving then to 2, 3, 4, 5, combinations
    #* and then checking if matches target
    # 1 combination
    for i in range(0, sizeOfSet):
        test(target, startingSet[i], startTime)
    
    # 2 combination
    for pos0 in range(0, sizeOfSet):
        for pos1 in range(0, sizeOfSet):
            solution = startingSet[pos0] + startingSet[pos1]
            test(target, solution, startTime)
            
    # 3 combination
    for pos0 in range(0, sizeOfSet):
        for pos1 in range(0, sizeOfSet):
            for pos2 in range(0, sizeOfSet):
                solution = startingSet[pos0] + startingSet[pos1] + startingSet[pos2]
                test(target, solution, startTime)

    # 4 combination
    for pos0 in range(0, sizeOfSet):
        for pos1 in range(0, sizeOfSet):
            for pos2 in range(0, sizeOfSet):
                for pos3 in range(0, sizeOfSet):
                    solution = startingSet[pos0] + startingSet[pos1] + startingSet[pos2] + startingSet[pos3]
                    test(target, solution, startTime)

    # 5 combination             
    for pos0 in range(0, sizeOfSet):
        for pos1 in range(0, sizeOfSet):
            for pos2 in range(0, sizeOfSet):
                for pos3 in range(0, sizeOfSet):
                    for pos4 in range(0, sizeOfSet):
                        solution = startingSet[pos0] + startingSet[pos1] + startingSet[pos2] + startingSet[pos3] + startingSet[pos4]
                        test(target, solution, startTime)

    # 6 combination
    for pos0 in range(0, sizeOfSet):
        for pos1 in range(0, sizeOfSet):
            for pos2 in range(0, sizeOfSet):
                for pos3 in range(0, sizeOfSet):
                    for pos4 in range(0, sizeOfSet):
                        for pos5 in range(0, sizeOfSet):
                            solution = startingSet[pos0] + startingSet[pos1] + startingSet[pos2] + startingSet[pos3] + startingSet[pos4] + startingSet[pos5]
                            test(target, solution, startTime)
    print("no solution found")


def brute_force_BCH(target, startTime):
    '''
        FUNCTION: brute_force_BCH
        DEFINITION: builds all the possible combinations for password length of 6 using int in range 0-9
        PARAMETERS: target: string, startTime: float
        RETURNS: void
    '''
    number_rangee = [x for x in range(10)]
    number_range_size = len(number_rangee)
    solution = []

    for pos0 in range(0, number_range_size):
        for pos1 in range(0, number_range_size):
            for pos2 in range(0, number_range_size):
                for pos3 in range(0, number_range_size):
                    for pos4 in range(0, number_range_size):
                        for pos5 in range(0, number_range_size):
                            solution.append(number_rangee[pos0])
                            solution.append(number_rangee[pos1])
                            solution.append(number_rangee[pos2])
                            solution.append(number_rangee[pos3])
                            solution.append(number_rangee[pos4])
                            solution.append(number_rangee[pos5])

                            #* build an int of length 6 as set length required for bch and pass as a list
                            encoded_bch = bch.encode_bch(solution)

                            if len(encoded_bch) != 0:
                                #* check if the number created is a valid bch
                                validBCH = bch.valid_bch_check(encoded_bch)

                                if validBCH:
                                    #* bch number valid turn int into a string it's hashed and checked against the target
                                    testPassword = ''.join(str(n) for n in encoded_bch)
                                    print(f"password to hash: {testPassword}\n")
                                    test_bch_hash(target, testPassword, startTime)
                            #* if number is not target or valid clear list to create 6 integers
                            solution.clear()

#: ------------- CODE ------------- ------------- CODE ------------- ------------- CODE -------------

combinationRange = range_numeric_alphabetical("a", "z", 0, 9)

# pass1 = "c2543fff3bfa6f144c2f06a7de6cd10c0b650cae" #* time: 1.29463791847229 secs / solution: this
# pass2 = "b47f363e2b430c0647f14deea3eced9b0ef300ce" #* time: 0004630088806152344 secs / solution: is
# pass3 = "e74295bfc2ed0b52d40073e8ebad555100df1380" #* time: 1.461106777191162 secs / solution: very
# pass4 = "0f7d0d088b6ea936fb25b477722d734706fe8b40" #* time: secs / solution:
# pass5 = "77cfc481d3e76b543daf39e7f9bf86be2e664959" #* time: secs / solution:
# pass6 = "5cc48a1da13ad8cef1f5fad70ead8362aabc68a1" #* time: secs / solution:
# pass7 = "4bcc3a95bdd9a11b28883290b03086e82af90212" #* time: secs / solution: 
# pass8 = "7302ba343c5ef19004df7489794a0adaee68d285" #* time: 73.33839678764343 secs / solution: 1you1
# pass9 = "21e7133508c40bbdf2be8a7bdc35b7de0b618ae4" #* time: secs / solution:
# pass10 = "6ef80072f39071d4118a6e7890e209d4dd07e504" #* time: secs / solution:
# pass11 = "02285af8f969dc5c7b12be72fbce858997afe80a" #* time: secs / solution:
# pass12 = "57864da96344366865dd7cade69467d811a7961b" #* time: secs / solution:

start = time.time()
brute_force_alpha_numeric(pass3, combinationRange, start)

#* use to take input from keyboard
# start = time.time()
# brute_force_alpha_numeric(input("\nenter alpha-numeric hash: "), combinationRange ,start)


#: ------------- BCH Brute Force -------------
# bch_1 = "902608824fae2a1918d54d569d20819a4288a4e4" #* time: 0.00086998 secs solution is -> 0000118435
# bch_2 = "88d0b34055b79644196fce25f876bc1a5ef654d3" #* time: 13.94 seconds solution is -> 1111110565
# bch_3 = "5b8f495b7f02b62eb228c5dbece7c2f81b60b9a3" #* time: 104.50316596031189 solution is -> 8888880747

# start = time.time()
# brute_force_BCH(bch_2, start)

#* use to take input from keyboard
# start = time.time()
# brute_force_BCH(input("\nenter BCH hash: "), start)



























