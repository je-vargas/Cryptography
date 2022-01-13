
#: --------------- Task 3 credit card checker
#* 15 digits of credit card are random generated
def read_number(readNumber):
    '''
        DEFINITION: Read's number and transfroms it into a list
    '''
    numberList = list()
    sliceUpto = 1
    for i in range(0, len(readNumber), sliceUpto):
        numberList.append(int(readNumber[i : i + sliceUpto]))
    return numberList


def doubled_digit(digit):
    doubleDigit = digit * 2 
    if ( doubleDigit >= 10):
        return (doubleDigit - 9)
    return doubleDigit

def credit_card_checker(cardNumber):
    cardNumbersSplit = cardNumber.copy()
    for digit in range(0, len(cardNumbersSplit) , 2):
        cardNumbersSplit[digit] = doubled_digit(cardNumbersSplit[digit])
    cardNumbersSum = sum(cardNumbersSplit)
    validCardNumber = cardNumbersSum % 10
    if validCardNumber == 0: print("valid: {0}".format(validCardNumber))
    else: print("invalid: {0}".format(validCardNumber))
        
# ---> Task 2 Card Checker
a = read_number(input("enter number"))
# a = [4,0,0,3,6,0,0,0,0,0,0,0,0,0,1,4]
a = [4,5,5,2,7,2,0,4,1,2,3,4,5,6,9,8]
credit_card_checker(a)