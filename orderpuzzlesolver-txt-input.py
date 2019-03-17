#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      katie
#
# Created:     26/01/2016
# Copyright:   (c) katie 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()


"""This is the order puzzle solver! Make sure you spell everything correctly
and consistently (caps etc.)!!"""

#make sure you don't have an item called x, make sure you don't have more than 1 of the same item
"""make it so that you can have clues like 'so and so was not third' or 'so and
so was not last' maybe make it so you can just type in the whole clue?"""

import numbers

File_obj = open('orderpuzzlesolver-items.txt', 'r')

#list of all items
orderListStr = File_obj.readline()
orderListStr = orderListStr.rstrip()

orderList = orderListStr.split(', ')
print(orderListStr)
print(orderList)

File_obj.close()

#dictionary with all items as keys, and arrays with potiential positions
#as values. When a potential position is ruled out, it is replaced with an 'x'.
numOrderList = {}

#list of things known to be in front of each item
frontList = {}

#list of things known to be behind each item
behindList = {}

#fills in initial values for numOrderList. Creates dictionaries with items as
#keys and empty arrays as values for frontList and behindList
for i in orderList:
    numOrderList[i]= [x for x in range(1, len(orderList) + 1)]
    frontList[i] = []
    behindList[i] = []

#accepts clue inputs from the user.
def clueFinder(clue):
    fullClue = clue.rstrip()
    fullClue = fullClue.split(', ')
    thing = fullClue[1]
    forBeh = fullClue[0]
    thing2 = fullClue[2]
    print('fullClue: ', fullClue)

    #if thing2 is behind thing, thing can't be last and thing2 can't be first
    if forBeh.lower() == 'behind':
        behindList[thing].append(thing2)
        frontList[thing2].append(thing)
        print('%s is behind %s' % (thing2, thing))
        numOrderList[thing][len(orderList) - 1] = 'x'
        numOrderList[thing2][0] = 'x'

    if forBeh.lower() == "in front of":
        frontList[thing].append(thing2)
        behindList[thing2].append(thing)
        print('%s is in front of %s' % (thing2, thing))
        numOrderList[thing][0] = 'x'
        numOrderList[thing2][len(orderList) - 1] = 'x'
    print('numOrderList: ', numOrderList)

#dict of items whose positions have been determined
knownItems = {}

#below is the check to see if an item only has one possible position
def horizontalCheck():
    for i in numOrderList:
        appendTo = i
        if numOrderList[i].count('x') == len(orderList) - 1:
            print("hc the position of %s has been determined" % (i))
            for k in numOrderList[i]:
                if k == 'x':
                    pass
                else:
                    knownPosition = k
                    knownItems[appendTo] = knownPosition
                    #eliminates the known position for all other items
                    for l in numOrderList:
                        if l != i:
                            print('numOrderList, l: ', numOrderList, l)
                            for m in numOrderList[l]:
                                #print('m: ', m)
                                if m == knownPosition:
                                    numOrderList[l][m - 1] = 'x'
            print("%s is in position %s" % (i, knownPosition))

#check to see if a certain position is eliminated for all but one item
def verticalCheck():
    #cycles through positions
    for i in range(0, len(orderList)):
        #print("i = ", i),
        total = 0
        #counts how many items have an x for a certian position
        for k in numOrderList:
            #print("k = ", k)
            if numOrderList[k][i] == 'x':
                total += 1
            else:
                tempKnown = k #item that the postition has been found out for
        #gives knownPosition if only one item has that position
        if total == len(orderList) - 1:
            knownPosition = i + 1 #to offset the fact that the indeces start at 0
            knownItems[tempKnown] = knownPosition
            print("verticalCheck knownPosition = ", knownPosition)

            #deletes all other positions for an item whose correct position has been found
            for m in numOrderList[tempKnown]:
                if m != knownPosition and m != 'x':
                    numOrderList[tempKnown][m - 1] = 'x'
            print("%s is in position %s" % (tempKnown, knownPosition))

def clueResubmit():
    for i in frontList:
        thing = i
        listy = numOrderList[i]
        filteredList = [x for x in listy if isinstance(x, numbers.Number)]
        print(filteredList)
        if i not in knownItems and filteredList:
            print(i)
            frontPosition = min(filteredList)
            print(frontPosition)
            backPosition = max(filteredList)
            print(backPosition)
            for j in frontList[i]:
                print(j)
                thing2 = j
                if j not in knownItems:
                    print('clueResubmit, numOrderList [thing]: ', numOrderList[thing])
                    print(numOrderList[thing2])
                    numOrderList[thing][frontPosition - 1] = 'x'
                    numOrderList[thing2][backPosition - 1] = 'x'
                    print(numOrderList[thing])
                    print(numOrderList[thing2])

def frontBehindCheck():
    for i in frontList:
        tempFrontThings = []
        tempBehindThings = []
        for j in behindList:
            if i == j:
                for k in frontList[i]:
                    tempFrontThings.append(k)
                for l in behindList[i]:
                    tempBehindThings.append(l)
                for m in tempFrontThings:
                    for n in tempBehindThings:
                        if n not in behindList[m]:
                            behindList[m].append(n)
                for p in tempBehindThings:
                    for q in tempFrontThings:
                        if q not in frontList[p]:
                            frontList[p].append(q)

#check this dicitonary with frontlist and behindlist

f = open('orderpuzzlesolver-clues.txt', 'r')

for line in f:
    clueFinder(line)
    horizontalCheck()
    horizontalCheck()
    verticalCheck()
    horizontalCheck()
    horizontalCheck()
    #clueYes = input("Are there any more clues?")

for x in range(len(orderList)):
    clueResubmit()
    horizontalCheck()
    horizontalCheck()
    verticalCheck()
    horizontalCheck()
    horizontalCheck()


frontBehindCheck()

print('numOrderList: ', numOrderList)
print('knownItems: ', knownItems)
print("FrontList: ", frontList)
print("BehindList: ", behindList)