import random
def main():
    individual = [1,2,3,4,5,6]
    print(mutate(individual))

def mutate(individual):
    before=[]
    after=[]
    result=[]

    L1 = random.randint(1,5);
    L2 = random.randint(1,5);
    while ( L1 == L2 ):
        L1 = random.randint(1,5);
        L2 = random.randint(1,5);

    if (L1 > L2):
        tmp = L2
        L2 = L1
        L1 = tmp;
    before = individual[0:L1]
    after = individual[L2:]
    random.shuffle(before)
    random.shuffle(after)

    print("L1=", L1, "L2=",L2)
    print("before:", before, "after:", after)
    for i in range(len(before)):
        result.append(before[i])
    for i in range(L1, L2):
        result.append(individual[i])
    for i in range(len(after)):
        result.append(after[i])

    return result
    
        

main()
