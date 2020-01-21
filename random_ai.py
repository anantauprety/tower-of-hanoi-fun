
import logging

import numpy as np
import random

from hanoi_env import HanoiEnv
from simulation import runSimulation


class RandomAI(object):

    def __init__(self, actions):
        # self.seed = 16
        # np.random.seed(self.seed)
        # random.seed(self.seed)
        self.actionSteps = actions

    def __str__(self):
        return 'Rando AI'

    def getActionCommand(self, state, reward):
        return np.random.choice(self.actionSteps, 1)[0]




if __name__=='__main__':
    env = HanoiEnv(5)
    # env.getState()
    actions = np.asarray(env.getActions())
    print(actions)
    randoAgent = RandomAI(actions)

    runSimulation(env, randoAgent, 10000, numOfTries=100000)





