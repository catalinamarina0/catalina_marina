import random
import copy
import move
import argparse

def initialState(height,width):
    state1d = []
    for w in range(width):
        state1d.append(0)
    state = []
    for h in range(height):
        state.append(state1d.copy())
    return state

def randomEmptyField(state):
    emptyfields = []
    for h in range(len(state)):
        for w in range(len(state[0])):
            if state[h][w] == 0:
                emptyfields.append((h,w))
    return random.choice(emptyfields)

def randomNumber(newNumbers):
    return random.choice(list(newNumbers))

def turnPC(state,newNumbers):
    newNumberAt = randomEmptyField(state)
    h = newNumberAt[0]
    w = newNumberAt[1]
    newNumber = randomNumber(newNumbers)
    state[h][w] = newNumber
    
def turnPlayer():
    turn = input()
    return turn
    
def turnResolve(state,turn):
    if turn == move.left():
        left(state)
        mergeHorizontal(state)
        left(state)
    elif turn == "e":
        right(state)
        mergeHorizontal(state)
        right(state)
    elif turn == ",":
        up(state)
        mergeVertical(state)
        up(state)
    elif turn == "o":
        down(state)
        mergeVertical(state)
        down(state)

def left(state):
    height = len(state)
    width = len(state[0])
    for h in range(height):
        for w in range(width-1):
            if state[h][width-2-w] == 0:
                for ww in range(width-2-w,width-1):
                    state[h][ww] = state[h][ww+1]
                state[h][width-1] = 0

def right(state):
    height = len(state)
    width = len(state[0])
    for h in range(height):
        for w in range(1,width):
            if state[h][w] == 0:
                for ww in range(w):
                    state[h][w-ww] = state[h][w-ww-1]
                state[h][0] = 0

def up(state):
    height = len(state)
    width = len(state[0])
    for w in range(width):
        for h in range(height-1):
            if state[height-2-h][w] == 0:
                for hh in range(height-2-h,height-1):
                    state[hh][w] = state[hh+1][w]
                state[height-1][w] = 0

def down(state):
    height = len(state)
    width = len(state[0])
    for w in range(width):
        for h in range(1,height):
            if state[h][w] == 0:
                for hh in range(h):
                    state[h-hh][w] = state[h-hh-1][w]
                state[0][w] = 0

#merge moet uitgesplitst worden
def mergeHorizontal(state):
    height = len(state)
    width = len(state[0])
    for h in range(height):
        for w in range(width-1):
            if mergeRules(state[h][w],state[h][w+1]):
                state[h][w] += state[h][w+1]
                state[h][w+1] = 0

def mergeVertical(state):
    height = len(state)
    width = len(state[0])
    for w in range(width):
        for h in range(height-1):
            if mergeRules(state[h][w],state[h+1][w]):
                state[h][w] += state[h+1][w]
                state[h+1][w] = 0

#outdated
def printState(state):
    for h in range(len(state)):
        print(state[h])


def printStateStr(state):
    stateCopy = copy.deepcopy(state)
    valuesSet = set()
    for h in range(len(state)):
        valuesSet = valuesSet.union(set(state[h]))
    length = len(str(max(valuesSet)))
    for h in range(len(state)):
        for w in range(len(state[0])):
            if stateCopy[h][w] == 0:
                stateCopy[h][w] = " "
            else:
                stateCopy[h][w] = str(stateCopy[h][w])
    for w in range(len(state[0])):      #bovenrand
        print("_",end = "_")            #bovenrand
        for l in range(length - 1):     #bovenrand
            print("", end = "_")        #bovenrand
    print("___")                        #bovenrand
    for h in range(len(state)):
        print("|",end = " ")            #linkerrand
        for w in range(len(state[0])):
            print(stateCopy[h][w],end = " ")
            for l in range(length - len(stateCopy[h][w])):
                print("", end = " ")
        print("|")                      #rechterrand
    for w in range(len(state[0])):      #onderrand
        print("-",end = "-")            #onderrand
        for l in range(length - 1):     #onderrand
            print("", end = "-")        #onderrand
    print("---")                        #onderrand


def play(state,newNumbers):
    while True:
        turnPC(state,newNumbers)
        printStateStr(state)
        stateCheck = copy.deepcopy(state)
        while stateCheck == state:
            turn = turnPlayer()
            turnResolve(state,turn)



def mergeRules(m1,m2):
    if m1 != 0 and m1 == m2:                    #double
#    if m1 != 0 and m1 < 2*m2 and m2 < 2*m1:     #ratio
        return True
    else:
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("height",type = int,help = "The height of your playing field.")
    parser.add_argument("width",type = int,help = "The width of your playing field. Warning: The game grows wider as numbers get bigger. If width is too wide for your window, this wil break the visuals.")
    size = parser.parse_args()
    height = size.height
    width = size.width

    newNumbers = {2,4}
    state = initialState(height,width)
    play(state,newNumbers)


if __name__ == "__main__":
    main()