def newNumbers(mode):
    if mode == "classic":
        return {2,4}
    elif mode == "ratio":
        return {2,3,4,5,6,7,8}


def mergeRules(m1,m2):
    modeFile = open("mode.txt","r")
    mode = modeFile.read()
    modeFile.close()
    if mode == "classic":
        if m1 != 0 and m1 == m2:                    #double
            return True
        else:
            return False
    elif mode == "ratio":
        if m1 != 0 and m1 < 2*m2 and m2 < 2*m1:     #ratio
            return True
        else:
            return False


if __name__ == "__main__":
    m = mergeRules(1,3)
    print(m)