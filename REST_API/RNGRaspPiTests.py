import numpy as np
from threading import Thread
import math
from itertools import product
testspass=False
startup_pass=False
des_length=129
result = []
startupResult = None
onlineResult = None
totResult = None

# Calculating entropy of data: test fails if entropy is below or equal to 0.997
def totTest(data):
    p = data.count("1")/(data.count("1")+data.count("0"))
    q = 1-p

    if(p==0):
        return False

    entropie = (-q*math.log2(q))-(p*math.log2(p))
    global totResult
    if entropie > 0.997:
        totResult =True
        return True
    return False


# Online test passes if data passes the Monobit- and Runs-test
def onlineTest(binary_String):
    global onlineResult
    string = [int(x) for x in binary_String]
    
    if(testMonobit(string)and runsTest(string)):
        onlineResult = True
        return True
    onlineResult = False
    return False

# Startup test passes if Monobit-, Poker- and Runs-test passes
def startupTest(binary_String):
    global startupResult
    binary_array = [int(x) for x in binary_String]
    
    if(testMonobit(binary_array) and pokerTest(binary_array) and runsTest(binary_array)):
        startupResult = True
        return True
    startupResult = False
    

def testMonobit(binary_String):
    """
    Implements the Monobit Test on 20,000 bits sequences.
    Input:
        bits: an array with the bits as integers.
    Description and Evaluation rule:
        The Monobit Test is passed when the sum of all bits is in the interval [9654;10346]. Otherwise it failed.
    """
    lastPosition = 0
    results =[]

    while(lastPosition+20000 <= len(binary_String)):
        T1 = sum(binary_String[lastPosition:20000+lastPosition])

        if 9654 < T1 < 10346:
            results.append(True)
        else:
            results.append(False)
        lastPosition += 20000
    
    if(containsOnlyTrue(results)):
        return True
    else: 
        return False

def pokerTest(binary_array):
    """
    Implements the Poker Test on 20,000 bits sequences.
    Input:
        binary_array: an array with the bits as integers.
    Description and Evaluation rule:
        The Poker Test is passed when T2 is in the interval [1.03;57.4]. Otherwise it failed.
        It checks the occurences of 4-bit patterns.
    """
    lastPosition = 0
    results =[]
    trueCounter = 0

    while(lastPosition+20000 <= len(binary_array)):
        bit_sequence = binary_array[lastPosition:lastPosition+20000]
        f = [0] * 16

        for j in range(5000):
            c_j = 8*bit_sequence[4*j] + 4*bit_sequence[4*j+1] + \
                2*bit_sequence[4*j+2] + bit_sequence[4*j+3]
            f[c_j] += 1

        T_2 = (16/5000) * sum([freq**2 for freq in f]) - 5000

        if 1.03 < T_2 < 57.4:
            results.append(True)
        else:
            results.append(False)
        lastPosition += 20000
    
    if(containsOnlyTrue(results)):
        return True
    else: 
        return False

def runsTest(binary_array):
    """
    Implements the Runs Test on 20,000 bits sequences
    Input:
        binary_array: an array with the bits as integers.
    Description and Evaluation rule:
        The Runs Test is passed when the runs for specific lengths are in a defined interval. Otherwise it failed.
        A run is defined as a consecutive sequence of the same number.
    """
    lastPosition = 1
    results =[]
    bitfieldB = binary_array
    lowerBound = [0, 2267, 1079, 502, 223, 90, 90]
    upperBound = [0, 2733, 1421, 748, 402, 223, 223]
    run = 1

    while(lastPosition+20000 <= len(binary_array)):
        run0field = [0] * 7
        run1field = [0] * 7
        for i in range(lastPosition, lastPosition+20000):
            if bitfieldB[i-1] == bitfieldB[i]:
                run += 1
            else:
                if run > 6:
                    run = 6
                if bitfieldB[i-1] == 1:
                    run1field[run] += 1
                else:
                    run0field[run] += 1
                run = 1
        if run > 6:
            run = 6
        if bitfieldB[i-1] == 1:
            run1field[run] += 1
        else:
            run0field[run] += 1
        for i in range(1, 7):
            if lowerBound[i] <= run0field[i] <= upperBound[i]:
                results.append(True)
            else:
                results.append(False)

            if lowerBound[i] <= run1field[i] <= upperBound[i]:
                results.append(True)
            else:
                results.append(False)
        lastPosition += 20000
    if(containsOnlyTrue(results)):
        return True
    else: 
        return False

def containsOnlyTrue(lst):
    return all(element is True for element in lst)