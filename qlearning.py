# Q-learning program which generates midi files
import numpy as np
import pandas as pd
import time

class Qlearning():

    def __init__(self, N_STATES, ACTIONS, EPSILON, ALPHA, GAMMA, MAX_EPISODES, REFRESH_TIME, EPISODE_TIME, DB):
        
        np.random.seed(2)  # reproducible

        self.N_STATES = N_STATES            # the length of the 1 dimensional world
        self.ACTIONS = ACTIONS              # available self.ACTIONS
        self.EPSILON = EPSILON              # greedy police / RANDOMNESS / original 0.9
        self.ALPHA = ALPHA                  # learning rate
        self.GAMMA = GAMMA                  # discount factor
        self.MAX_EPISODES = MAX_EPISODES    # maximum episodes
        self.REFRESH_TIME = REFRESH_TIME    # refresh time for one move
        self.EPISODE_TIME = EPISODE_TIME    #time between episodes
        self.DB = DB                        #Debugging, printing data to console

        self.S = 0
        self.step_counter = 0
        self.episodeCounter = 0
        self.done = False
        self.doingEpisodes = True

        self.startTime = time.time()
        self.endTime = REFRESH_TIME

        self.qTable = self.build_q_table(self.N_STATES, self.ACTIONS)
        self.rl()

    def build_q_table(self, N_STATES, ACTIONS):
        table = pd.DataFrame(
            np.zeros((self.N_STATES, len(self.ACTIONS))),   # q_table initial values
            columns=self.ACTIONS,                           # self.ACTIONS's name
        )
        # print(table)
        # print""
        return table

    def choose_action(self, state, q_table):
        # This is how to choose an action
        state_actions = q_table.iloc[state, :]
        # act non-greedy or state-action have no value
        if (np.random.uniform() > self.EPSILON) or ((state_actions == 0).all()):
            action_name = np.random.choice(self.ACTIONS)
        else:   # act greedy
            # replace argmax to idxmax as argmax means a different function in newer version of pandas
            action_name = state_actions.idxmax()
        return action_name

    def get_env_feedback(self, S, A):
        # This is how agent will interact with the environment
        if A == 'up':    # move right
            if S == self.N_STATES - 2:   # terminate
                S_ = 'terminal'
                R = 1
            else:
                S_ = S + 1
                R = 0
        else:   # move left
            R = 0
            if S == 0:
                S_ = S  # reach the wall
            else:
                S_ = S - 1
        return S_, R

    def rl(self):

        A = self.choose_action(self.S, self.qTable)
        # take action & get next state and reward
        S_, R = self.get_env_feedback(self.S, A)
        q_predict = self.qTable.loc[self.S, A]
        if S_ != 'terminal':
            # next state is not terminal
            q_target = R + self.GAMMA * self.qTable.iloc[S_, :].max()
        else:
            q_target = R     # next state is terminal
            self.is_terminated = True    # terminate this episode
            self.doingEpisodes = True

        self.qTable.loc[self.S, A] += self.ALPHA * (q_target - q_predict)  # update

        #parse data from table
        #data = self.qTable.values.tolist()

        self.S = S_  # move to next state

        self.step_counter += 1 

        if self.DB:
            print (self.qTable)
            print ("state:", self.S)
            print ("action:", A)
            print ("Q-Predict", q_predict)
            print ("episode:", self.episodeCounter)

        #return self.qTable

    def run(self):

        if not self.done:
            if self.doingEpisodes:
                self.doingEpisodes = False
                self.is_terminated = False
                self.step_counter = 0
                self.S = 0

                if(self.episodeCounter>self.MAX_EPISODES):
                    self.done = True

                self.episodeCounter+=1

        if not self.is_terminated:
            timer = time.time() - self.startTime
            if timer >= self.endTime:
                self.rl()
                self.startTime = time.time()


