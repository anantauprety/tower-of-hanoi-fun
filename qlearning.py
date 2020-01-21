
from hanoi_env import HanoiEnv
import numpy as np
import matplotlib.pyplot as plt


class QLearner(object):

    def __init__(self, env, df=0.999, alpha=0.5, eps=0.9, eps_decayrate=0.99):
        self.env = env
        self.actions = env.getActions()
        self.nStates = env.nStates()
        self.nActions = len(self.actions)
        self.eps = eps
        self.df = df
        self.alpha = alpha
        self.eps_decayrate = eps_decayrate
        self.Q = np.zeros((self.nStates, self.nActions))
        self.stats = {}

    def run(self, nEpisodes=1):
        '''
        Choose action a -greedily
        Take action a, observe r,s′
        Update: Q(s,a) ← Q(s,a) + α (r+γ max a′Q(s′,a′)−Q(s,a))
        Next: s←s′
        :param nEpisodes:
        :return:
        '''

        for nEpisode in range(nEpisodes):

            done = False
            obs_state = env.reset()
            # env.printState()
            episode_reward = 0
            num_steps = 0

            while not done:
                if np.random.random() <= self.eps:
                    action = self.actions[np.random.randint(self.nActions)]
                    # print('rando', action, self.eps)
                else:
                    action = np.argmax(self.Q[obs_state])
                    # print(action)

                obs_state_next, reward, done, num_steps = env.takeAction(action)
                episode_reward += reward

                # print(action,'----->', obs_state_next, reward, done, num_steps)

                best_action_next = np.argmax(self.Q[obs_state_next])

                target_td = reward + self.df * self.Q[obs_state_next][best_action_next]

                td_delta = target_td - self.Q[obs_state][action]

                self.Q[obs_state][action] += self.alpha * td_delta

                obs_state = obs_state_next

                # print(self.Q[obs_state_next])

            if nEpisode % 10 == 0:
                self.eps *= self.eps_decayrate
                print(self.Q[398])

            # also figure out if converged

            print(nEpisode, num_steps, episode_reward, episode_reward/ num_steps, self.eps)
            self.stats[nEpisode] = [num_steps, episode_reward/ num_steps]
        print(self.Q.shape)


    def displayGraphs(self):
        steps = []
        rewards = []
        for k in self.stats.keys():
            steps.append(self.stats[k][0])
            rewards.append(self.stats[k][1])

        steps = np.array(steps)
        rewards = np.array(rewards)

        fig, axs = plt.subplots(1, 2, figsize=(20,5))

        axs[0].plot( self.stats.keys(), rewards, 'b+')

        axs[1].plot(self.stats.keys(), steps, 'go')

        plt.show()

if __name__ == "__main__":
    env = HanoiEnv(3)


    learner = QLearner(env)
    # env.printState()
    # print(env.takeAction(0))
    # env.printState()
    # print(learner.Q.shape)
    # print(learner.Q[0].shape)
    learner.run(5000)
    learner.displayGraphs()
