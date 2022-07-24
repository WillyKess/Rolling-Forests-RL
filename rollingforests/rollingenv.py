import gym
from gym import spaces
from webinterface import WebInterface
import numpy as np
from time import strftime


class MovingAverage(object):
    def __init__(self, size: int):
        self.size = size
        self.queue = []

    def next(self, val):
        if not self.queue or len(self.queue) < self.size:
            self.queue.append(val)
        else:
            self.queue.pop(0)
            self.queue.append(val)
        return int(sum(self.queue) / len(self.queue))

class RollingForestsEnv (gym.Env, WebInterface):
    def __init__(self, headless=False):
        gym.Env.__init__(self)
        WebInterface.__init__(self, headless=headless)
        self.action_dict = {0: self.jump,
                            1: self.go_left,
                            2: self.go_right,
                           }
        self.action_space = spaces.Discrete(4)
        shape = (540, 960, 3)
        self.observation_space = spaces.Box(low=0, high=255, shape=shape, dtype=np.uint8)
        self.lastscore = 0
        self.stepno = 0
        self.maxscoreavg = 0
        self.avg = MovingAverage(20)
        self.batchno = 0
    def reset(self):
        obs = self.grab_screen()
        self.pause()
        if self.batchno % 2 == 0:
            print(f"({strftime('%I:%M %p')}): Starting Batch #{int(self.batchno / 2) + 1}, Last Batch's Average Score: {self.maxscoreavg}")
        self.batchno += 1
        return obs

    def step(self, action):
        if self._driver.execute_script("return paused"):
            self.pause()
        if action != 3:
            self.action_dict[action]()
        tempscore = self.lastscore
        info = self.get_info()
        if self.lastscore < tempscore:
            self.maxscoreavg = self.avg.next(tempscore)
        print(f"Step #{self.stepno},    Average Max Score: {self.maxscoreavg}", end = '\r')
        self.stepno += 1
        return info

    def get_info(self):
        screen =  self.grab_screen()
        score = self.get_score()
        scorediff = (score - self.lastscore) - 1
        reward = -5 if scorediff < 0 else scorediff + 0.1
        self.lastscore = score
        return screen, reward, False, {"score": score}

    def get_score(self):
        score = self._driver.execute_script("return score")
        return int(score)

    def close(self):
        self.end()