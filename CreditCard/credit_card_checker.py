
#: ------- TASK 1 - CREDIT CARD CHECKER ------- ------- TASK 1 - CREDIT CARD CHECKER ------- ------- TASK 1 - CREDIT CARD CHECKER -------
def read_number(readNumber):
    '''
        FUNCTION: read_number
        DEFINITION: Read's number from keyboard input and returns it into a list
        PARAMETERS: String read from input()
        RETURNS: list of string passed in
    '''
    numberList = list()
    sliceUpto = 1
    #
    for i in range(0, len(readNumber), sliceUpto):
        numberList.append(int(readNumber[i : i + sliceUpto]))
    return numberList


def doubled_digit(digit):
    '''
        FUNCTION: doubled_digit
        DEFINITION: Doubles value passed in and checks if number passed in is bigger or equal to 10
                    if it subtract 9 to make it single digit and returns digit
        PARAMETERS: Int
        RETURNS: Int
    '''
    doubleDigit = digit * 2 
    if ( doubleDigit >= 10):
        return (doubleDigit - 9)
    return doubleDigit

def credit_card_checker(cardNumber):
    '''
        FUNCTION: doubled_digit
        DEFINITION: loops through list of numbers passed, jumping by 2.
                    then adds all numbers in the list and mods by 10. 
                    if value is 0 is valid else invalid
        PARAMETERS: list of integers
        RETURNS: void
    '''
    cardNumbersSplit = cardNumber.copy()

    #* loops through list of integers, starting from index 0. 
    #* with step index of 2 so only second index from starting position/ previious position is used
    for digit in range(0, len(cardNumbersSplit) , 2):
        cardNumbersSplit[digit] = doubled_digit(cardNumbersSplit[digit])
    cardNumbersSum = sum(cardNumbersSplit)

    #* mod carNumbersum by 10 and check if its 0 it's valid
    #* otherwise print mod value
    validCardNumber = cardNumbersSum % 10
    if validCardNumber == 0: print("valid: {0}".format(validCardNumber))
    else: print("invalid: {0}".format(validCardNumber))
        
# ---> Task 2 Card Checker
# a = read_number(input("\nenter credit card number:"))
# a = [4,0,0,3,6,0,0,0,0,0,0,0,0,0,1,4]
a = [4,5,5,2,7,2,0,4,1,2,3,4,5,6,9,8]
credit_card_checker(a)