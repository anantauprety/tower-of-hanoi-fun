import numpy as np
import matplotlib.pyplot as plt

def displayGraphs(numRuns, numOfStepsTaken, totalRewardRuns, solvedInRuns):

    numRuns = np.arange(numRuns)
    fig, axs = plt.subplots(1, 2, figsize=(20,5))
    axs[0].plot(numRuns, [0] * len(numRuns), 'w', numRuns[solvedInRuns], numOfStepsTaken[solvedInRuns], 'g+')

    axs[1].plot(numRuns, [0] * len(numRuns), 'w', numRuns[solvedInRuns], totalRewardRuns[solvedInRuns], 'bd')
    plt.show()


def runSimulation(env, agent, numRuns=1, numOfTries=1000, doLog=True, displayGraph=True):


    totalRewardRuns = []
    numStepsRuns = []
    solvedInRuns = []

    for i in range(numRuns):

        solved = False
        movesTaken = 0
        state = env.getState()
        reward = 0
        totalRewards = 0

        while not solved and movesTaken <= numOfTries:
            action = agent.getActionCommand(state, reward)
            print(action)
            state, reward, solved, movesTaken = env.takeAction(action)
            # print(state, reward, solved, movesTaken)
            totalRewards += reward
            if doLog:
                print('Solved', solved, 'Moves Taken', movesTaken, 'Reward', totalRewards)

        numStepsRuns.append(movesTaken)
        totalRewardRuns.append(totalRewards)
        solvedInRuns.append(solved)


    numStepsRuns = np.array(numStepsRuns)
    totalRewardRuns = np.array(totalRewardRuns)
    solvedInRuns = np.array(solvedInRuns)

    if len(solvedInRuns[solvedInRuns]):
        print('for %d total runs %s sucessfully solved %d times at avg. moves of %d with avg. reward %d' %
                (numRuns, agent, len(solvedInRuns[solvedInRuns == True]),
                 np.average(numStepsRuns[solvedInRuns == True]),
                 np.average(totalRewardRuns[solvedInRuns == True]))
                  )
    else:
        print('for %d total runs %s di not sucessfully solve it'  % (numRuns, agent))

    if displayGraph:
        displayGraphs(numRuns, numStepsRuns, totalRewardRuns, solvedInRuns)

    return numStepsRuns, totalRewardRuns, solvedInRuns
