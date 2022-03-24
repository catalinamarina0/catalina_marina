import random
import copy
import argparse
import sys
import move
import modes

def initialState(height,width,depth):
    state1d = []
    for w in range(width):
        state1d.append(0)
    state2d = []
    for h in range(height):
        state2d.append(state1d.copy())
    state = []
    for d in range(depth):
        state.append(copy.deepcopy(state2d))
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
    if turn == "exit":
        sys.exit()
    return turn
    
def turnResolve(state,turn):
    if turn == move.left():
        left(state)
        mergeLeft(state)
        left(state)
    elif turn == move.right():
        right(state)
        mergeRight(state)
        right(state)
    elif turn == move.up():
        up(state)
        mergeUp(state)
        up(state)
    elif turn == move.down():
        down(state)
        mergeDown(state)
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
def mergeLeft(state):
    height = len(state)
    width = len(state[0])
    for h in range(height):
        for w in range(width-1):
            if modes.mergeRules(state[h][w],state[h][w+1]):
                state[h][w] += state[h][w+1]
                state[h][w+1] = 0

def mergeRight(state):
    height = len(state)
    width = len(state[0])
    for h in range(height):
        for w in range(width-1):
            if modes.mergeRules(state[h][width-1-w],state[h][width-w-2]):
                state[h][width-1-w] += state[h][width-w-2]
                state[h][width-w-2] = 0

def mergeUp(state):
    height = len(state)
    width = len(state[0])
    for w in range(width):
        for h in range(height-1):
            if modes.mergeRules(state[h][w],state[h+1][w]):
                state[h][w] += state[h+1][w]
                state[h+1][w] = 0

def mergeDown(state):
    height = len(state)
    width = len(state[0])
    for w in range(width):
        for h in range(height-1):
            if modes.mergeRules(state[height-1-h][w],state[height-h-2][w]):
                state[height-1-h][w] += state[height-h-2][w]
                state[height-h-2][w] = 0

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
        for d in range(len(state)):
            turnPC(state[d],newNumbers)
            printStateStr(state[d])
        stateCheck = copy.deepcopy(state)
        while stateCheck == state:
            turn = turnPlayer()
            for d in range(len(state)):
                turnResolve(state[d],turn)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",help = "Options: classic, ratio")
    parser.add_argument("height",type = int,help = "The height of your playing field.")
    parser.add_argument("width",type = int,help = "The width of your playing field. Warning: The game grows wider as numbers get bigger. If width is too wide for your window, this wil break the visuals.")
    parser.add_argument("depth",type = int,help = "Depth or number of copies.")
    size = parser.parse_args()
    mode = size.mode
    height = size.height
    width = size.width
    depth = size.depth
    modeFile = open("mode.txt","w")
    modeFile.write(mode)
    modeFile.close()
    newNumbers = modes.newNumbers(mode)
    state = initialState(height,width,depth)
    play(state,newNumbers)


if __name__ == "__main__":
    main()