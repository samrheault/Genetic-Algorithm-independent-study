#Genetic Algorithm for job shop layout assignment
#James Houghton and Sam Rheault independent study project spring '17
#URI department of Industrial and Systems Engineering

import random
population=[] #Empty list for the initial population
popsize = 10 #Define size to which population is always trimmed, number of crossovers per generation
generations = 10 #Define number of generations
k = 5 #Define tournament size
pm = 0.3 #Define probability of mutation

#Distance and flow matrices, problem specific
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

#--------------------------------------------------------------------------------------

def main():
    initialize()
    print("generation\tbest solution\t\tfitness")
    for j in range(generations):
        for i in range(popsize):
            crossover()
        trimpop()
        print(j+1,"\t\t",absolutebest(population)[0],"\t", absolutebest(population)[1])
    print("---------------------------------------------")
    print("OPTIMAL SOLUTION: ", absolutebest(population)[0],", fitness= ", absolutebest(population)[1])
    print("---------------------------------------------")


#--------------------------------------------------------------------------------------

def initialize():
#Creates the initial population, a list of lists containing numbers 1-6 in random orders
    for j in range (popsize):
        population.append(random.sample(range(1,7),6))
        
#--------------------------------------------------------------------------------------

def fitness(solution):
#Computes and returns fitness of input solution
    sorteddistance = [[],[],[],[],[],[]]

#Sort the distance matrix based on the order of solution
    for i in range(6):
        row = solution[i]-1
        for j in range(6):
            col = solution[j]-1
            sorteddistance[i].append(distance[row][col])

#Compute sumproduct of sorted distance matrix and flow matrix
    products = []
    for i in range(6):
        for j in range(6):
            products.append(sorteddistance[i][j]*flow[i][j])
    sump = sum(products)
    return(sump)

#--------------------------------------------------------------------------------------

def fit_eval(array):
#Evaluates the fitness of every member of a population
#Returns a dictionary of individuals and their fitnesses called fit_dict
    fit_dict = {}
    for n in range(len(array)):
        key_name = str(array[n])
        fit_dict[key_name]=fitness(array[n])
    return fit_dict

#--------------------------------------------------------------------------------------

def tournament(k):
#Pairs couples for crossover based on most fit member of random samples
#k is the size of the sample - typically 3, can be changed for more/less selection pressure 

    crossovercouple = []

    for j in range (2):
#Take a sample of k competitors and creates a dictionary of competitors and their corresponding fitnesses
        competitors = random.sample(population,k)
        fitnesses = fit_eval(competitors) 
#Sort the dictionary based on fitness values
        sortedfitnesses = sorted(fitnesses.values()) 
#Store the most fit competitor as a string called "best"
        best =(list(fitnesses.keys())[list(fitnesses.values()).index(sortedfitnesses[0])])
#Convert the string "best" into a list called "bestlist"
        bestlist=[]
        for i in range(1,len(best),3):
            bestlist.append(int(best[i]))

#Add the two tournament winners into list called "crossovercouple"
        crossovercouple.append(bestlist)
    return crossovercouple

#--------------------------------------------------------------------------------------

def mutate(individual):
#Executes a mutation on the input individual
#Identifies a section of the individual to remain the same, scrambles everything before and after that section.
#Mutated individual is stored as a new list called result

    before=[]
    after=[]
    result=[]

#Choose location points to define unchanged section
    L1 = random.randint(1,5);
    L2 = random.randint(1,5);
#Ensure the locations are different
    while ( L1 == L2 ):
        L1 = random.randint(1,5);
        L2 = random.randint(1,5);
#Ensure the locations are ascending
    if (L1 > L2):
        tmp = L2
        L2 = L1
        L1 = tmp;
#Shuffle the material before and after the unchanged section
    before = individual[0:L1]
    after = individual[L2:]
    random.shuffle(before)
    random.shuffle(after)

#Populate the result list with shuffled material, unchanged section, shuffled material
    for i in range(len(before)):
        result.append(before[i])
    for i in range(L1, L2):
        result.append(individual[i])
    for i in range(len(after)):
        result.append(after[i])

    return result

#--------------------------------------------------------------------------------------

def crossover():
#Executes a two-point crossover from two parents who are winners of tournament
#Creates two new "children" lists, offs1 and offs2, and either adds them to the population whole or mutates them before adding to population

#ID parents: winners of tournament
    couple = tournament(k)
    ind1 = couple[0]
    ind2 = couple[1]

#Randomly determine two points for crossover
    size = min(len(ind1), len(ind2))
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
#Ensure crossover points are ascending 
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else: 
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

#Populate each offspring with section from parents between the two crossover points 
    offs2=ind1[cxpoint1:cxpoint2]
    offs1=ind2[cxpoint1:cxpoint2]
#Copy parental material before crossover section to children in order, skipping duplicates
    for i in range(cxpoint1):
        if not ind1[i] in offs1:
            offs1.insert(i, ind1[i])
        else:
            dupe1 = i
        if not ind2[i] in offs2:
            offs2.insert(i, ind2[i])
        else:
            dupe2 = i
#Copy parental material after crossover section to children in order, skipping duplicates
    for i in range(cxpoint2,size):
        if not ind1[i] in offs1:
            offs1.insert(i, ind1[i])
        else: dupe1 = i
        if not ind2[i] in offs2:
            offs2.insert(i, ind2[i])
        else: dupe2 = i

#Ensure each child contains every number from 1-6, add missing number(s) in location of skipped duplicates
    if len(offs1) < 6:
        for j in range (1,7):
            if not j in offs1:
                offs1.insert(dupe1, j)
    if len(offs2) < 6:
        for j in range (1,7):
            if not j in offs2:
                offs2.insert(dupe2, j)

#Determine whether the offspring will be mutated by comparing random numbers to mutation probability
    mutation1 = random.random()
    mutation2 = random.random()
#Offspring are mutated in place if random number <= mutation probability
    if mutation1 <= pm:
        offs1 = mutate(offs1)
    if mutation2 <= pm:
        offs2 = mutate(offs2)

#Add the two offspring to the population whole
    population.append(offs1)
    population.append(offs2)

#--------------------------------------------------------------------------------------

def trimpop():
#Removes least fit members of population to keep population size constant at the beginning of each generation

    mostfit = []
#Use fit_eval function to create a dictionary of individuals and fitnesses, sorts the dictionary on fitness values    
    popfitness = fit_eval(population)
    sortedpopfitness = sorted(popfitness.values())
#Create a string called "best" corresponding to the competitor with best fitness
    for i in range(popsize):
        best =(list(popfitness.keys())[list(popfitness.values()).index(sortedpopfitness[i])]) 
        bestlist=[]
#Create a list of the most fit individuals, its length being the defined population size        
        for i in range(1,len(best),3):
            bestlist.append(int(best[i]))
        mostfit.append(bestlist)
#Clear the population        
    del population[:]
#Add the most fit individuals back into the population
    for i in range(len(mostfit)):
        population.append(mostfit[i])

#--------------------------------------------------------------------------------------

def absolutebest(pop):
#Returns individual with best fitness from input population
    fitnesses = fit_eval(pop)
#Sort the dictionary created by fit_eval function based on fitness values
    sortedfitnesses = sorted(fitnesses.values())
    best =(list(fitnesses.keys())[list(fitnesses.values()).index(sortedfitnesses[0])])
    best_fitness = sortedfitnesses[0]
#Return a tuple of the most fit individual and corresponding fitness
    return best, best_fitness    

#--------------------------------------------------------------------------------------
main()
    
