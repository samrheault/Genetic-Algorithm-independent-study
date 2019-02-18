distance =[ [0,802,156,389,249,300],
            [802,0,759,482,608,584],
            [156,759,0,182,150,401],
            [389,482,182,0,179,179],
            [249,608,150,179,0,100],
            [300,584,401,179,100,0]]

flow = [ [0,0,13,5,1,1],
         [0,0,0,0,0,0],
         [15,0,0,5,2,0],
         [50,25,15,0,50,0],
         [50,15,10,50,0,10],
         [1,5,0,0,5,0]]

#Need a 6x6 matrix to work with
import random
population=[]
generations = 5

for j in range (6):
    population.append(random.sample(range(1,7),6)) #Creates 6 rows, each row containing numbers 1-6 in random order (no repeated #'s) 

#crossover function
def crossover(x,y):
    xo_loc = random.randint(0,5) #location where split is made
    #ID parents: rows x and y from 6x6 array
    parent1 = x
    parent2 = y
    xochild1= []
    xochild2= []

    for i in range(0, xo_loc):
        xochild1.append(parent1[i])#copies 1st part of 1st parent to 1st child
        xochild2.append(parent2[i])#copies 1st part of 2nd parent to 2nd child
    for j in range(xo_loc,len(parent2)):
        xochild1.append(parent2[j])#copies 2nd part of 2nd parent to 1st child
        xochild2.append(parent1[j])#copies 2nd part of 1st parent to 2nd child
    population.append(xochild1)
    population.append(xochild2)
    return(xochild1,xochild2)

def fitness(solution):
    #Create and fill a sorted distance matrix based on solution
    sorteddistance = [[],[],[],[],[],[]]
    for i in range(6):
        row = solution[i]-1
        for j in range(6):
            col = solution[j]-1
            sorteddistance[i].append(distance[row][col])

    #Compute sumproduct of sorted distance and flow matrices
    products = []
    for i in range(6):
        for j in range(6):
            products.append(sorteddistance[i][j]*flow[i][j])
    sump = sum(products)
    return (sump)

def fit_eval(): #Evaluates the fitness of every member of the population and stores it in a dictionary
    fit_dict = {}
    for n in range(len(population)):
        fit_dict[n]=fitness(population[n])
    return(fit_dict)

#tournament function
def tournament(k): #k being the "size" of the tournament - typically 3, can be changed for more/less diversity 
    best = 0
    for i in range (generations):
        crossovercouple = []
        for j in range (2):
            competitors = random.sample(population,k)

            fit1 = fit_dict[population.index(competitors[1])]
            fit2 = fit_dict[population.index(competitors[2])]
            fit3 = fit_dict[population.index(competitors[3])]

            if fit1 < fit2:
                if fit1 < fit3:
                    best = p1
                else:
                    if fit3 < fit2:
                        best = p3
                    else:
                        best = p2
            #print("best is ", best)
            crossovercouple.append(best)

        x = crossovercouple[0]
        y = crossovercouple[1]
        crossover(x,y)

    print("new pop is: ", population)
 

    



def main():
#tell the program which rows from the 6x6 matrix should be the crossover couple
#    k = int(input("enter a value for k \n"))
    #print ("initial pop is: ", population)
#    tournament(k)
    fit_eval()
    print (fit_dict)

main()



