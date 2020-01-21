from hanoi import Hanoi
import numpy as np

class HanoiEnv(object):

    '''
    state is the state of all the discs in the towers
    if there are 3 discs and 3 towers like below where
    it is the the initial state of the discs
            discs
             0  -  -
             1  -  -
             2  -  -
    tower:   a  b  c

    (higher the number means the disc is bigger)
     so each disc can be in 9 of the grid spaces so the rest can be in any
     8 grid spaces and 7 grid respectively
     so there are 9*8*7 = 504 states

     but, since 504 is not prime we can use 509 such that we can do modulo arithmetic

     position of the disc on the towers can be encoded as if they were on a 3X3 grid



  y-axis
         |
         |
       3 |
       2 |
       1 |
           a b c
          ------------->
x-axis    1 2 3
      which mean 0 at (1,1), 1 is at (1,2) and 3 is at (1,3)


      so if we put these number together we get (111213 % 509) = 251
      so we just say it starts out at state 333 and as we go through
      the states we can fill those out

      we can also know if we reached the final stage by checking comparing the
      numbers where 0 will be at (3,1), 1 at (3,2) and 2 at (3,3) which gives
      (313233 % 509) = 198

     Actions:

     Since we can only take 1 action at a time
     we can model the action of the agent to mean
     from tower a move the top disc to tower b or tower c
     which basically means agent needs to choose the tower
     and give command as below (left, right, left jump or right jump)
     jump basically means skip to the next tower


    tower		     ACTIONS
        a	   left 	right	left_jump	right_jump
        b	   left 	right	left_jump	right_jump
        c	   left 	right	left_jump	right_jump


     so there 3 towers * 4 differnt actions = 12 different actions

     we can number them 0 to 12 to make is easier

     0: from tower a move left (not a valid move but, keeping it to make agent simple)
     1: from tower a move right (move to tower b
     2: from twoer a left jump (not a valid move cause it doesn't wrap around)
     3: from tower a right jump (moves to tower 3)
     ...
     ....
     10: from tower c left jump to tower a
     12: from tower c right jump (wrong move)

     For the reward I am keeping it simple
     if the action causes any violation of rule like going off board or trying to place
     bigger disc on top of smaller disc than it gets -10 reward
     if the state is good and no viloations it gets 10 reward
     if the goal is reached it gets 1000 reward
    '''

    def __init__(self, numOfDisc):
        self.hanoi = Hanoi(numOfDisc)
        self.numDisc = numOfDisc
        self.moveDict = self._getMoveDict()
        self.rewards = [-10,0,100000]
        self.prime = 509
        self.totalMoves = 0

    def _getMoveDict(self):
        # pop from rod and push into rod (invalid moves are -1)
        move_dict = { 0: (0, -1), # tower 0 pop disc and move left (invalid)
                      1: (0, 1), # tower 0 pop disc and move right
                      2: (0, -1), # tower 0 pop disc and jump left skip one rod (invalid)
                      3: (0, 2), # tower 0 pop disc and jump righ skip one rod to tower 2
                      4: (1, 0),
                      5: (1, 2),
                      6: (1, -1),
                      7: (1, -1),
                      8: (2, 1),
                      9: (2, -1),
                      10: (2, 0),
                      11: (2, -1),
        }

        return move_dict

    def getActions(self):
        return [n for n in self.moveDict.keys()]

    def getState(self):
        posDict = {}
        for y in range(self.numDisc):
            for x in range(3):
                disc = self.hanoi.atIndex(x, y)
                if disc:
                    posDict[disc.num] = 10 * (x+1) + (y+1)

        # print(posDict)
        state = 0
        for n in range(self.numDisc):
            num = posDict.get(n)
            state = state * 100 + num
        # print(state)
        # print(state % self.prime)
        return state % self.prime

    def isSolved(self):
        return self.hanoi.isSolved()


    def takeAction(self, actionNumber):
        self.totalMoves += 1
        action = self.moveDict.get(actionNumber, (-1,-1))
        res = self.hanoi.move_from_to(*action)
        solved = self.isSolved()

        if solved:
            reward = self.rewards[2]

        elif res:
            reward = self.rewards[1]
        else:
            reward = self.rewards[0]

        return self.getState(), reward, solved, self.totalMoves


    def printState(self):
        self.hanoi.printState()

    def nStates(self):
        return 509

    def reset(self):
        self.hanoi = Hanoi(self.numDisc)
        self.totalMoves = 0
        return self.getState()


def solveThreeMin():
    # give the actions to solve in 7 min steps
    # rod 1 jump right, rod 1 right, rod 3 left, rod 1 jump right, rod2 left, rod2 right, rod1 jump right
    return [3, 1, 8, 3, 4, 5, 3]



if __name__=='__main__':
    env = HanoiEnv(3)
    # env.getState()
    actions = np.asarray(env.getActions())
    print(actions)


    for n in actions:
        print(n)
        state, reward, solved, movesTaken = env.takeAction(n)
        print(state, reward, solved, movesTaken)
        env.printState()
        env.getState()

    env.reset()
    for n in solveThreeMin():
        print(n)
        state, reward, solved, movesTaken = env.takeAction(n)
        # print(state, reward, solved, movesTaken)
        env.printState()
        # env.getState()

    env.reset()
    #
    # env.takeAction(1)
    # print(env.printState())
    # print(env.getState())


