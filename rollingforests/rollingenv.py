import gym
from gym import spaces
from webinterface import WebInterface
import numpy as np
import progressbar

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
        self.highscore = 0
        self.bar: progressbar.ProgressBar = progressbar.ProgressBar(maxval=100000, widgets=['Step #', progressbar.SimpleProgress(), ' ', progressbar.GranularBar(), ' ', progressbar.Timer(), '', progressbar.AdaptiveETA()]).start()

    def reset(self):
        obs = self.grab_screen()
        self.pause()
        return obs

    def step(self, action):
        if self._driver.execute_script("return paused"):
            self.pause()
        if action != 3:
            self.action_dict[action]()
        self.bar.update(self.bar.value + 1)
        return self.get_info()

    def get_info(self):
        screen =  self.grab_screen()
        score = self.get_score()
        scorediff = (score - self.lastscore) - 1
        reward = scorediff / 4 if scorediff < 0 else scorediff + 0.5
        self.lastscore = score
        self.highscore = self._driver.execute_script("return highScore")
        return screen, reward, False, {"score": score}

    def get_score(self):
        score = self._driver.execute_script("return score")
        return int(score)

    def close(self):
        self.end()