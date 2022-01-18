
# --------------------- Mod Operators ---------------------
def mod_addition(x, y, mod):
    return ((x + y) % mod)

def mod_subtraction(x, y, mod):
    subtraction = (x - y) % mod
    return subtraction

def mod_multiplication(x, y, mod):
    return ((x * y) % mod)

def mod_inverse(x, mod):
    for a in range(1, mod):
        if (mod_multiplication(a, x, mod) == 1):
            return a
    return -1

def mod_division(dividend, divisor, mod):
    divisor = divisor % 11
    dividend = dividend % 11
    inverse = mod_inverse(divisor, mod)
    if inverse == -1:
        return -1
    return mod_multiplication(dividend, inverse, mod)

def mod_square_root(x, mod):
    for a in range(1, mod):
        square = pow(a, 2)
        if ((square % mod) == x):
            return a
    return -1

def mod_power(x, power, mod):
    xToPower = pow(x, power)
    return (xToPower % mod)

def mod(x, mod):
    return (x % mod)



# --------------------- Week 3 ---------------------
# inplement BHC
#* 15 digits of credit card are random generated
def read_number(readNumber):
    '''
        DEFINITION: Read's number from keyboard input and returns it into a list
    '''
    numberList = list()
    sliceUpto = 1
    for i in range(0, len(readNumber), sliceUpto):
        numberList.append(int(readNumber[i : i + sliceUpto]))
    return numberList

def encode_bch():
    # this was done in week 2 practical
    "Definition: double error correction code"
    exit()

def check_multiplier(bchMultiplier, modOperator):
    if bchMultiplier >= 10:
        return mod(bchMultiplier, modOperator)
    return bchMultiplier

def calculate_syndrome(bchNumberList, syndromeLength, modOperator):
    'working state: Complete'
    syndromeList = list()
    syndromeReturn = list()
    syndromeSum = 0
    syndromeSumCheck = 0

    for currentSyndrome in range (0, syndromeLength):
        for currentBchNumber in range(0, (len(bchNumberList))):
            power = pow((currentBchNumber+1), currentSyndrome)
            multiplier = check_multiplier(power, modOperator) 
            nextBchNumber = (multiplier * bchNumberList[currentBchNumber])
            syndromeList.append(nextBchNumber)
        #     print(" S:{0} | indexPower : {1} * bch number: {2}".format(currentSyndrome, multiplier, bchNumberList[currentBchNumber]))
        # print("\nS:{0} -> {1}\n".format(currentSyndrome, syndromeList))
        syndromeSum = sum(syndromeList)
        syndromeReturn.append(mod(syndromeSum, modOperator))
        syndromeList.clear()

    return syndromeReturn

def calculate_pqr(sydrome, modOperator):
     # p = (s2^2 - S1*S3) mod 11
    # q = (S1*S4 - S2*S3) mod 11
    # r = (s3^2 - S2*S4) mod 11
    P = mod((pow(sydrome[1], 2) - (sydrome[0] * sydrome[2])), modOperator)
    Q = mod((sydrome[0] * sydrome[3]) - (sydrome[1] * sydrome[2]), modOperator)
    R = mod((pow(sydrome[2], 2) - (sydrome[1] * sydrome[3])), modOperator)

    return P, Q, R

def bch_single_error(p, q, r, sydrome, modOperator):
    errorMagnitude = sydrome[0]
    errorPosition = mod_division(sydrome[1], errorMagnitude, modOperator)
    return errorMagnitude, errorPosition

def bch_double_error(p, q, r, syndromeList ,modOperator):

    doubleErroReturn = dict()
    quadratic = mod((pow(q, 2) - (4*p*r)), modOperator)
    error1Square = mod_square_root(quadratic, modOperator) # ROOT NOT WORKING
    divisor = 2*p

    errPositionI = mod_division((-q + error1Square), divisor, modOperator)
    errPositionJ = mod_division((-q - error1Square), divisor, modOperator)

    checkErrPositionIsNot0 = errPositionI == 0 or errPositionJ == 0
    checkErrPositionIsNot0 = errPositionI == 0 or errPositionJ == 0
    noInverseFound = errPositionI == -1 or errPositionJ == -1

    if error1Square == -1 or checkErrPositionIsNot0 or noInverseFound:
        doubleErroReturn['squareRoot'] = False
        return doubleErroReturn

    errorMagnitudeB = mod_division(((errPositionI*syndromeList[0])-syndromeList[1]), (mod_subtraction(errPositionI, errPositionJ, modOperator)), modOperator)
    errorMagnitudeA = mod_subtraction(syndromeList[0], errorMagnitudeB, modOperator)

    checkErrMaginuteIsNotOver10 = errorMagnitudeA > 9 or errorMagnitudeB > 9
    
    if checkErrMaginuteIsNotOver10:
        doubleErroReturn['squareRoot'] = False
        return doubleErroReturn

    doubleErroReturn['b'] = errorMagnitudeB
    doubleErroReturn['a'] = errorMagnitudeA
    doubleErroReturn['i'] = errPositionI
    doubleErroReturn['j'] = errPositionJ
    doubleErroReturn['squareRoot'] = True

    return doubleErroReturn

def decode_bch(bchNumber):
    SYNDROME_LENGTH = 4
    MOD = 11
    correctBchNumber = bchNumber.copy()
    syndrome = calculate_syndrome(bchNumber, SYNDROME_LENGTH, MOD)
    pqr = calculate_pqr(syndrome, MOD)
    P = pqr[0]
    Q = pqr[1]
    R = pqr[2]

    if(sum(syndrome) == 0):
        print("input: {0}".format(bchNumber))
        print("no error \n")
        return

    if (P+Q+R) == 0:
        errorMagnitude, errorPosition = bch_single_error(P, Q, R, syndrome, MOD)
        if errorPosition == 0:
            print("input: {0}".format(bchNumber))
            print("output: ??")
            print("morethan2_no_sqrt(sync({0}, pqr({1},{2},{3}))\n".format(syndrome, P, Q, R))
            return

        correction = mod_subtraction(bchNumber[errorPosition-1], errorMagnitude, MOD)
        correctBchNumber[errorPosition-1] = correction

        print("input: {0}".format(bchNumber))
        print("output: {0}".format(correctBchNumber))
        print("single_error(i={0}, a={1}, syn({2}, pqr({3},{4},{5})))\n".format(errorPosition, errorMagnitude, syndrome, P, Q, R))
        return
    else:
        doubleError = bch_double_error(P, Q, R, syndrome, MOD)
        squareRoot = doubleError['squareRoot']

        if squareRoot :    
            errMagB = doubleError['b']
            errMagA = doubleError['a']
            errPosI = doubleError['i']
            errPosJ = doubleError['j']  

            correctionI = mod_subtraction(bchNumber[errPosI-1], errMagA, MOD)
            correctionJ = mod_subtraction(bchNumber[errPosJ-1], errMagB, MOD)

            correctBchNumber[errPosI-1] = correctionI
            correctBchNumber[errPosJ-1] = correctionJ

            print("input: {0}".format(bchNumber))
            print("output: {0}".format(correctBchNumber))
            print("double_err(i={0}, a={1}, j={2}, b={3}, sync({4}, pqr({5},{6},{7}))\n".format(errPosI, errMagA, errPosJ, errMagB, syndrome, P, Q, R))
            return
        else:
            print("input: {0}".format(bchNumber))
            print("output: ??")
            print("morethan2_no_sqrt(sync({0}, pqr({1},{2},{3}))\n".format(syndrome, P, Q, R))
            return

    
testBch = [
    [3,7,4,5,1,9,5,8,7,6],
    [3,9,4,5,1,9,5,8,7,6],
    [3,7,4,5,9,9,5,8,7,6],
    [3,7,1,5,1,9,5,0,7,6],
    [0,7,4,3,1,9,5,8,7,6],
    [3,7,4,5,1,9,5,8,4,0],
    [2,7,4,5,7,9,5,8,7,8],
    [8,7,4,5,1,0,5,8,7,6],
    [3,7,4,5,1,0,2,8,7,6],
    [3,7,4,2,1,0,2,8,9,6],
    [1,1,4,5,1,9,5,8,7,6],
    [3,7,4,5,1,9,1,9,7,6],
    [3,7,4,5,1,9,0,8,7,2],
    [1,1,1,5,1,9,5,8,7,6],
    [3,1,2,1,1,9,5,8,7,6],
]

test2Bch = [
    [3,1,2,1,1,9,5,8,7,6],
    [1,1,3,5,6,9,4,7,6,6],
    [0,8,8,8,8,8,8,0,7,4],
    [5,6,1,4,2,1,6,0,0,9], 
    [9,9,9,0,9,0,9,9,2,3],
    [1,8,3,6,7,0,3,7,7,6],
    [9,8,8,5,9,8,0,7,3,1]
]


for test in testBch:
    decode_bch(test)

# for test in test2Bch:
#     decode_bch(test)

# bch = read_number(input("\nenter bch number: "))
# decode_bch(bch)
