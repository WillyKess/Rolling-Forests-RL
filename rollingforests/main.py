from math import inf
from rollingenv import RollingForestsEnv
from stable_baselines3.dqn.dqn import DQN
# from stable_baselines3.common.evaluation import evaluate_policy
# from stable_baselines3.common.env_checker import check_env

# progressbar.ProgressBar(maxval=200, widgets=['On Round #', progressbar.SimpleProgress(), ' |', progressbar.GranularBar(), '| Total Time Elapsed: ', progressbar.Timer()]).start()
env = RollingForestsEnv(headless=True)
# check_env(env)
# print(env.observation_space)
# env = FlattenObservation(env)
# print(env.observation_space)
env.reset()
model = DQN('MlpPolicy', env, buffer_size=5000)
# model.load('a2c_rolling')
for i in range(200):
    model.learn(total_timesteps=500)
    # print(f"Round {i+1}/100 done!")
    env.reset()
    model.save('dqn_rolling')
env.end()
# sleep(2)
# model = A2C.load('a2c_rolling', env=env)
# mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)  # type: ignore
# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs, deterministic=True)  # type: ignore
#     obs, rewards, dones, info = env.step(action)