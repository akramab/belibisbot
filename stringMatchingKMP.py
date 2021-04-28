def checkSufPrefKMP(patternInput, i):
    pattern = patternInput.lower().strip()
    #Fungsi buat cek pasangan suffix dan prefix dalam algoritma KMP
    return (pattern[0:i] ==  pattern[len(pattern)-i:len(pattern)])

def buildFail(patternInput):
    pattern = patternInput.lower().strip()
    #Fungsi preproses
    #Dipake buat bikin array yang isinya angka start algoritma KMP kalau ada mismatch
    result = [0 for i in range(len(pattern))]
    result[0] = 0
    result[1] = 0
    for i in range(2,len(pattern)):
        temp = 0
        for j in range(i):
            if (checkSufPrefKMP(pattern[0:i],j)):
                temp = j
        result[i] = temp
    return result

def stringMatching(textInput, patternInput):
    text = textInput.lower().strip()
    pattern = patternInput.lower().strip()
    fail = buildFail(pattern)
    i = 0
    j = i
    n = len(text)
    m = len(pattern)
    while (i < n):
        if (text[i] == pattern[j]):
            #Found
            if (j == (m-1)):
                return (i - m + 1)
            i += 1
            j += 1
        elif (j > 0):
            #Update j ke posisi pengecekan selanjutnya
            j = fail[j] #Kalau di kelas harusnya inputnya j-1, tapi di sini langsung j aja
        else:
            #Dari awal string udah mismatch. Langsung geser ke char text selanjutnya
            i += 1
    #Not found
    return -1
