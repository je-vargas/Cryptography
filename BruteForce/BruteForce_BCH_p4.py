import hashlib
import math
from string import ascii_letters
import itertools # --use this for permutations
import time
import bch_checker as bch
# ------------- Implementing SHA1 -------------

def sha1_encode(password):
    sha1 = hashlib.sha1(str.encode(password))
    return sha1.hexdigest()

# print("hash encode ??: {0}".format(hash("abc")))
# print("sha1 with encode : {0}".format(sha1.hexdigest())) #must encode string --> error

# ------------- BruteForce -------------

def size_of_possible_passwords_set(passwordLength):
    size = list()
    for length in range(0, passwordLength+1):
        size.append(pow(passwordLength, length))
    return size

def range_numeric_alphabetical(startLetter, endLetter, startInt, endInt):
    "definition: returns list of alphabettic and numeric range to use for combinations"
    alpha_numeric_range = ascii_letters[ascii_letters.index(startLetter):ascii_letters.index(endLetter)+1]
    alpha_numeric_range_list = [char for char in alpha_numeric_range]
    for i in range(startInt, endInt+1):
        alpha_numeric_range_list.append(str(i))
    return alpha_numeric_range_list

def test(target, possibleSolution, start):
    encodedSolution = sha1_encode(possibleSolution)
    if target == encodedSolution:
        end = time.time()
        print("solution found : {0}".format(possibleSolution))
        print(f"Runtime of the program is {end - start}")
        exit()

def test_bch_hash(target, possibleSolution, start):
    encodedSolution = sha1_encode(possibleSolution)
    if target == encodedSolution:
        end = time.time()
        print("solution found : {0}".format(possibleSolution))
        print(f"Runtime of the program is {end - start}")
        exit()

def brute_force_alpha_numeric(target, alphaNumericList, startTime):
    startingSet = alphaNumericList
    sizeOfSet = len(alphaNumericList)
    
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

                            encoded_bch = bch.encode_bch(solution)
                            if len(encoded_bch) != 0:
                                validBCH = bch.valid_bch_check(encoded_bch)
                                if validBCH:
                                    testPassword = ''.join(str(n) for n in encoded_bch)
                                    print(f"password to hash: {testPassword}\n")
                                    test_bch_hash(target, testPassword, startTime)
                            print("position d7, d8, d9 or d10 returned a value of 10")

#! ---------------- CODE START HERE ----------------

# combinationRange = range_numeric_alphabetical("a", "z", 0, 9)

# pass1 = "c2543fff3bfa6f144c2f06a7de6cd10c0b650cae" #this -> #1.65sec
# pass2 = "b47f363e2b430c0647f14deea3eced9b0ef300ce" #is -> #0.0007832050323486328
# pass3 = "e74295bfc2ed0b52d40073e8ebad555100df1380" #is -> #0.0007832050323486328
# pass4 = "0f7d0d088b6ea936fb25b477722d734706fe8b40" # -> #0.0007832050323486328
# pass5 = "77cfc481d3e76b543daf39e7f9bf86be2e664959"
# pass6 = "5cc48a1da13ad8cef1f5fad70ead8362aabc68a1"
# pass7 = "4bcc3a95bdd9a11b28883290b03086e82af90212" 
# pass8 = "7302ba343c5ef19004df7489794a0adaee68d285"
# pass9 = "21e7133508c40bbdf2be8a7bdc35b7de0b618ae4"
# pass10 = "6ef80072f39071d4118a6e7890e209d4dd07e504"
# pass11 = "02285af8f969dc5c7b12be72fbce858997afe80a"
# pass12 = "57864da96344366865dd7cade69467d811a7961b"

# start = time.time()
# brute_force_alpha_numeric(pass4, combinationRange, start)


# ------------- BCH -------------
bch_Bforce = [
    "902608824fae2a1918d54d569d20819a4288a4e4",
    "88d0b34055b79644196fce25f876bc1a5ef654d3",
    "5b8f495b7f02b62eb228c5dbece7c2f81b60b9a3"
]

# for target in bch_Bforce:
#     start = time.time()
#     brute_force_BCH(target, start)

start = time.time()
brute_force_BCH(bch_Bforce[0], start)





















