from rollingenv import RollingForestsEnv
from stable_baselines3 import A2C
from stable_baselines3.common.evaluation import evaluate_policy
# from stable_baselines3.common.env_checker import check_env

env = RollingForestsEnv()
# check_env(env)
# print(env.observation_space)
# env = FlattenObservation(env)
# print(env.observation_space)
model = A2C('MlpPolicy', env)
# model.load('a2c_rolling')
for i in range(100):
    model.learn(total_timesteps=100)
    print("Round {i}/100 done!".format(i=i+1))
    model.save('a2c_rolling')
env.end()
# sleep(2)
# model = A2C.load('a2c_rolling', env=env)
# mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)  # type: ignore
# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs, deterministic=True)  # type: ignore
#     obs, rewards, dones, info = env.step(action)