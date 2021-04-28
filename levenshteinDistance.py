def levenshteinDistance(stringA,stringB):
    distanceMatrix = [[0 for j in range(len(stringA)+1)] for i in range(len(stringB)+1)]
    for i in range(len(stringB)+1):
        for j in range(len(stringA)+1):
            if j == 0:
                distanceMatrix[i][j] = i
            if i == 0:
                distanceMatrix[i][j] = j
            if (j-1 >= 0 and i!= 0):
                distanceMatrix[i][j] = min(distanceMatrix[i][j-1], distanceMatrix[i-1][j-1],distanceMatrix[i-1][j])
                if (stringA[j-1] != stringB[i-1]):
                    distanceMatrix[i][j] += 1 
    return distanceMatrix[len(stringB)-1][len(stringA)-1]

def LD(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
       
    res = min([LD(s[:-1], t)+1,
               LD(s, t[:-1])+1, 
               LD(s[:-1], t[:-1]) + cost])

    return res

def missWordRecc(text, kataPenting, missThreshold, result):
    # result = [[0],[]]
    
    for count, mismatch in enumerate((text.split())):
        foundMismatch = False
        for keyword in kataPenting:
            editDistance = levenshteinDistance(mismatch.lower(),keyword.lower())
            mismatchPercentage = float(editDistance/max(len(keyword),len(mismatch)))
            if (mismatchPercentage < missThreshold and mismatchPercentage > 0):
                print("mismatch percentage",mismatchPercentage)
                print(keyword)
                print("editdistance: ", editDistance)
                result[1].append(keyword)
                foundMismatch = True
                result[0] = 1
                break
        if (not foundMismatch and mismatch not in result[1]):
            result[1].append(mismatch)
    if (result):
        return result
    return -1