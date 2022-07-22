# from time import sleep
import gym
from gym import spaces
from webinterface import WebInterface
import numpy as np
# import logging
from PIL import Image
from time import asctime
# from datetime import datetime
import progressbar

class RollingForestsEnv (gym.Env, WebInterface):
    def __init__(self, headless=False):
        # logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%H:%M:%S', filename='rollingforests.log', filemode='w')
        gym.Env.__init__(self)
        WebInterface.__init__(self, headless=headless)
        self.action_dict = {0: self.jump,
                            1: self.go_left,
                            2: self.go_right,
                            # 3: self.pause
                           }

        self.action_space = spaces.Discrete(4)
        shape = (600,800,3) if headless else (880, 901, 3)
        self.observation_space = spaces.Box(low=0, high=255, shape=shape, dtype=np.uint8)
        # self.reward_range = (-10, 200)
        self.bar: progressbar.ProgressBar = progressbar.ProgressBar(maxval=100000, widgets=['On Step #', progressbar.SimpleProgress(), ' ', progressbar.GranularBar(), ' ', progressbar.Timer(), progressbar.AdaptiveETA()]).start()
        self.lastscore = 0


    def reset(self):
        # logging.info("Resetting")
        obs = self.grab_screen()
        self.pause()
        # self.bar.update(0)
        # self.bar.start_time = datetime.now()
        return obs

    def step(self, action):
        if self._driver.execute_script("return paused"):
            self.pause()
        # sleep(0.01)
        if action != 3:
            self.action_dict[action]()
        # self.pause()
        # logging.info("Stepping, action: %s", action)
        self.bar.update(self.bar.value + 1)
        return self.get_info()

    def get_info(self):
        screen =  self.grab_screen()
        score = self.get_score()
        scorediff = (score - self.lastscore) - 1
        reward = scorediff / 4 if scorediff < 0 else scorediff + 0.5
        self.lastscore = score
        # return screen, reward, False, {"score": score}
        try:
            return screen, reward, False, {"score": score}
        finally:
            Image.fromarray(screen).save(f'pics/{asctime()[-13:-5]}.png')
    def get_score(self):
        score = self._driver.execute_script("return score")
        return int(score)

    def close(self):
        self.end()