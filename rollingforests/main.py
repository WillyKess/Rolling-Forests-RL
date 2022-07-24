from rollingenv import RollingForestsEnv
from stable_baselines3.dqn.dqn import DQN
# from stable_baselines3.common.evaluation import evaluate_policy
from signal import signal, SIGINT

env = RollingForestsEnv(headless=True)
env.reset()
model = DQN('MlpPolicy', env, buffer_size=10000)
# model = DQN.load('dqn_rolling', env=env, buffer_size=5000)
def handler(signum, frame):
    env.end()
    exit(0)
signal(SIGINT, handler)

while True:
    model.learn(total_timesteps=500)
    model.save('dqn_rolling')
    env.reset()


# env.end()


# sleep(2)
# model = DQN.load('dqn_rolling', env=env, buffer_size=5000)
# mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)  # type: ignore
# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs, deterministic=True)  # type: ignore
#     obs, rewards, dones, info = env.step(action)