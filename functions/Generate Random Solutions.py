
import random
def main():
    print("Here is the 6x6 array\n");
    print(generateCombinations());

def generateCombinations():
    arrayOfSolutions = [];

    maxNumber = 7;
    for y in range(0,maxNumber):
        rowOfSolutions = [];
        for i in range(0,6):
            validNumber = getRandom(6,rowOfSolutions);
            rowOfSolutions.append(validNumber);
        arrayOfSolutions.append(rowOfSolutions);

    return arrayOfSolutions;

def getRandom(maxNumber,rowArray):
    randomNumber = random.randint(1, maxNumber);
    boolean = True;
    for i in range(0,len(rowArray)):
        if randomNumber == rowArray[i]:
            boolean = False;

    if boolean:
        return randomNumber;
    else:
        return getRandom(maxNumber,rowArray);

main();
