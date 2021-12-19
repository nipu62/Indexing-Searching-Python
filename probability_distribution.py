"""
@author: Ayesha Siddika Nipu
"""
import numpy as np
import matplotlib
from matplotlib import pyplot as plt 
    
#returns sum of random numbers list for each trial 
def GetRandomNumbersList(num_dice, trials):
    listOfRandomNumbers = []
    for _ in range(trials):
        sum = 0
        for _ in range(num_dice):
            rand = np.random.randint(1, 7)
            sum += rand
        listOfRandomNumbers.append(sum)
    return listOfRandomNumbers
    
#plots graph using matplotlib 
def PlotGraphWithProbability(myDict, n, t):
    x = myDict.keys()
    y = myDict.values()
    plt.title("Probabilities with " + str(n) + " dice over " + str(t) + " trials") 
    plt.xlabel("Roll") 
    plt.ylabel("Probability") 
    plt.xticks(np.arange(0, len(x)+1, 2))
    plt.yticks(np.arange(0, max(y), 0.02))
    plt.plot(x, y,"ob") 
    plt.show() 
    print()
    
def main():
    while(True):
        num_dice = input('\nPlease enter the number of dice: ')
        # check if user wants to quit or not
        if num_dice.lower() == 'quit':
            print("Program Terminated!\n")
            return;
            
        trials = input('\nPlease enter the number of trials: ')  
        if trials.lower() == 'quit':
            print("Program Terminated!\n")
            return;
            
        # converted inputs to integer
        num_dice_int = int(num_dice)
        trials_int = int(trials)
        
        lst = GetRandomNumbersList(num_dice_int, trials_int)
        np_arr = np.array(lst, dtype=np.int64)
        myDict = {}
        
        max_sum = num_dice_int*6 + 1
        
        for i in range(0, max_sum):
            # used numpy to count the number of occurrences of each roll. 
            count = np.count_nonzero(np_arr == i)
            probability = count/trials_int
            
            # for less than 5 dice, rounded the probabilities to 3 decimal places
            # for 5 or more dice, rounded the probabilities to 5 decimal places 
            if num_dice_int<5:
                probability = round(probability, 3)
            else:
                probability = round(probability, 5)
                
            # The roll and probability is stored as key-value pair in a dictionary
            myDict[i] = probability
            
            if i>= int(num_dice):
                print(i, "\t", myDict[i])
    
        PlotGraphWithProbability(myDict, num_dice_int, trials_int)
        
if __name__ == "__main__":
    main()
