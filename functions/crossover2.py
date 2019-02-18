#Crossover Function

#Need a 6x6 matrix to work with
import random
solnarray=[[],[],[],[],[],[]]
#Creates 6 rows, each row containing numbers 1-6 in random order (no repeated #'s)
for j in range (6):
    solnarray[j]=(random.sample(range(1,7),6)) 

#crossover function
def crossover(x,y):
    split = random.randint(1,6) #number which determines location where split is made
    #ID parents: rows x and y from 6x6 array
    parent1 = solnarray[x]
    parent2 = solnarray[y]
    xochild1= []
    xochild2= []
    xo_loc = parent1.index(split)

    for i in range(0, xo_loc):
       xochild1.append(parent1[i])#copies 1st part of 1st parent to 1st child
       xochild2.append(parent2[i])#copies 1st part of 2nd parent to 2nd child
    for j in range(xo_loc,len(parent2)):
        xochild1.append(parent2[j])#copies 2nd part of 2nd parent to 1st child
        xochild2.append(parent1[j])#copies 2nd part of 1st parent to 2nd child

    print ("parent1:", parent1, "  parent 2:", parent2)
    print ("splitter:", split, ", split at", xo_loc)
    print ("child1:", xochild1, "  child2:", xochild2)


def main():
#tell the program which rows from the 6x6 matrix should be the crossover couple
    x = int(input("parent 1: "))
    y = int(input("parent 2: "))
    crossover(x,y)

main()



