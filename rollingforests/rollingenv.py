from time import sleep
import gym
from gym import spaces
from webinterface import WebInterface
import numpy as np

class RollingForestsEnv (gym.Env, WebInterface):
    def __init__(self):
        gym.Env.__init__(self)
        WebInterface.__init__(self)
        # print("doing thing")
        # print(self._driver.execute_script("return score"))
        # self._driver.execute_script("rollingSpeed=0.004")

        # init_script = "document.getElementsByClassName('runner-canvas')[0].id = 'runner-canvas'"
        # self._driver.execute_script(init_script)

        self.action_dict = {0: self.jump,
                            1: self.go_left,
                            2: self.go_right,
                            # 3: self.pause
                           }

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=255, shape=(880, 901, 3), dtype=np.uint8)
        # self.reward_range = (-10, 200)
        self.lastscore = 0


    def reset(self):
        print("Resetting")
        obs = self.grab_screen()
        return obs

    def step(self, action):
        # assert action in self.action_space
        # print(action)
        print("Stepping")
        if action != 3:
            self.action_dict[action]()
        # else:
        #     print("Doing nothing")

        return self.get_info()

    def get_info(self):
        screen =  self.grab_screen()
        score = self.get_score()
        scorediff = (score - self.lastscore) - 1
        reward = -5 if scorediff < -5 else scorediff
        self.lastscore = score
        return screen, scorediff, False, {"score": score}

    def get_score(self):
        score = self._driver.execute_script("return score")
        return int(score)

    def close(self):
        self.end()