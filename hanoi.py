
class Disc(object):

    def __init__(self, num):
        self.num = num


class Rod(object):

    def __init__(self, num, sizeofStack):
        self.rod_num = num
        self.stack = [None] * sizeofStack
        self.size = 0

    def push(self, disc):
        if self.size > 0 and self.stack[self.size -1].num > disc.num:
            self.stack[self.size] = disc
            self.size += 1
            return True
        elif self.size == 0:
            self.stack[self.size] = disc
            self.size += 1
            return True
        else:
            return False

    def pop(self):
        if self.size > 0:
            disc = self.stack[self.size -1]
            self.size -= 1
            return disc
        return None

    def discAtIndex(self, indx):
        if indx < self.size:
            return self.stack[indx]
        return None

    def printState(self):
        res = []
        for n in range(self.size-1,-1,-1):
            res.append(self.stack[n].num)
        print('\n'.join(map(str, res)))


class Hanoi(object):

    def __init__(self, numDiscs):
        self.rods = [Rod(0, numDiscs), Rod(1, numDiscs), Rod(2, numDiscs)]
        self.numDiscs = numDiscs
        for n in range(self.numDiscs-1, -1, -1):
            # print(n)
            self.rods[0].push(Disc(n))
        # self.rods[0].printState()


    def move_from_to(self, rod_from, rod_to):
        if rod_from < len(self.rods) and rod_from > -1 and rod_to < len(self.rods) and rod_to > -1:
            disc = self.rods[rod_from].pop()
            if disc:
                 res = self.rods[rod_to].push(disc)
                 if not res:
                     self.rods[rod_from].push(disc)
                 return res
        return False

    def atIndex(self, towerNum, levelNum):
        if towerNum > -1 and towerNum < 3:
            return self.rods[towerNum].discAtIndex(levelNum)
        return None

    def isSolved(self):
        bigDiscNum = self.numDiscs - 1
        if self.rods[-1].size != self.numDiscs:
            return False

        for disc in self.rods[-1].stack:
            if disc.num != bigDiscNum:
                return False
            bigDiscNum -= 1
        return True

    def printState(self):
        res = []

        levelEmpty = False

        level = 0
        while level < self.numDiscs:
            levelEmptyCnt = 0
            lvlRes = []
            for rod_num in range(len(self.rods)):
                disc = self.rods[rod_num].discAtIndex(level)
                if disc:
                    lvlRes.append(' %s ' % disc.num)
                else:
                    lvlRes.append(' - ')
                    levelEmptyCnt += 1

                if levelEmptyCnt == len(self.rods):
                    levelEmpty = True


            level += 1
            res.append(''.join(lvlRes))

        print('\n'.join(reversed(res)))
        print()
        # for rod in self.rods:
        #     rod.printState()





if __name__ == "__main__":

    towers = Hanoi(3)
    towers.printState()

    moves = [(0,2),(0,1)]
    for move in moves:
        print(towers.move_from_to(*move))

    towers.printState()

