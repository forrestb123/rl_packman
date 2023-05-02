import gym
import torch
import torch.nn as nn
from itertools import chain
from matplotlib import pyplot as plt
from tqdm import tqdm
import random
from torch.utils.data import Dataset, DataLoader
import numpy as np

NUM_STATES = 4
NUM_ACTIONS = 2

class RLDataset(Dataset):
    def __init__(self, data):
        super().__init__()
        self.data = []
        for d in data:
            self.data.append(d)
        
    def __getitem__(self, idx):
        return self.data[idx]
    
    def __len__(self):
        return len(self.data)
    
class Policy(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()
        hidden_size = 64
        self.net = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, action_size),
            nn.Softmax(dim=1)
        )

    def forward(self, x):
        return self.net(x)
    
class Value(nn.Module):
    def __init__(self, state_size):
        super().__init__()
        hidden_size = 64

        self.net = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

    def forward(self, x):
        return self.net(x)

def calc_return(memory, rollout, gamma):
    run_return = 0
    for i, transition in enumerate(reversed(rollout)):
        state, action, action_dist, reward = transition
        run_return = reward + gamma * run_return
        rollout[len(rollout) - i - 1] = (state, action, action_dist, run_return)
    memory.extend(rollout)
    return memory

def get_action(network, state):
    with torch.no_grad():
        action_dist = network(torch.from_numpy(state).float().unsqueeze(0).cuda()).squeeze(0)
        sel_action = torch.multinomial(action_dist, 1).item()
        return sel_action, action_dist
    
def learn(optim, policy, value, memory_dataloader, episilon, epochs):
    policy_losses = []
    val_losses = []
    criterion = nn.MSE_Loss()
    for epoch in range(epochs):
        for state, action, action_dist, returns in memory_dataloader:
            optim.zero_grad()
            state, action, action_dist, returns = state.float().cuda(), action.cuda(), action_dist.cuda(), returns.float().cuda()

            state_val = value(state).squeeze()
            val_loss = criterion(returns, state_val)

            advantage = returns - state_val
            advantage = advantage.detach()

            one_hot = nn.functional.one_hot(action, NUM_ACTIONS).bool()
            curr_policy = policy(state)[one_hot]
            old_policy = action_dist[one_hot]
            ratio = curr_policy / old_policy
            grad_loss = ratio * advantage
            clip = torch.clamp(ratio, 1-episilon, 1+episilon) * advantage
            policy_loss = -torch.mean(torch.min(grad_loss, clip))
            loss = val_loss + policy_loss

            loss.backward()
            optim.step()

            policy_losses.append(policy_loss.item())
            val_losses.append(val_loss.item())

    return np.mean(policy_losses), np.mean(val_losses)

def ppo_main():
    lr = 1e-3
    epochs = 20
    env_samples = 100
    gamma = 0.9
    batch_size = 256
    episilon = 0.2
    policy_epochs = 5

    state_size = NUM_STATES
    action_size = NUM_ACTIONS
    env = gym.make('CartPole-v1', )

    policy = Policy(state_size, action_size).cuda()
    value = Value(state_size).cuda()
    optim = torch.optim.Adam(chain(policy.parameters(), value.parameters()), lr=lr)

    results_ppo = []
    policy_loss_ppo = []
    value_loss_ppo = []
    loop = tqdm(total=epochs, position=0, leave=False)

    for epoch in range(epochs):
        memory = []
        rewards = []

        for episode in range(env_samples):
            state = env.reset()
            done = False
            rollout = []
            cum_reward = 0

            while not done and cum_reward < 200:
                action, action_dist = get_action(policy, state)
                next_state, reward, done, _ = env.step(action)
                rollout.append((state, action, action_dist, reward))
                cum_reward += reward
                state = next_state

            memory = calc_return(memory, rollout, gamma)
            rewards.append(cum_reward)
    
        dataset = RLDataset(memory)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        policy_loss, value_loss = learn(optim, policy, value, loader, episilon, policy_epochs)
        policy_loss_ppo.append(policy_loss)
        value_loss_ppo.append(value_loss)

        results_ppo.extend(rewards)
        loop.update(1)
        loop.set_description('Epochs: {} Reward: {:.2f}'.format(epoch, results_ppo[-1]))

    return results_ppo, policy_loss_ppo, value_loss_ppo

results_ppo, policy_loss_ppo, value_loss_ppo = ppo_main()
plt.plot(policy_loss_ppo)
plt.title("PPO Policy Loss on Cartpole")
plt.ylabel("Mean PPO Policy Loss")
plt.xlabel("Training Epochs")
plt.show()
plt.plot(value_loss_ppo)
plt.title("PPO Value Loss on Cartpole")
plt.ylabel("Mean Value Loss (MSE)")
plt.xlabel("Training Epochs")
plt.show()
plt.plot(results_ppo)
plt.title("PPO Performance on Cartpole")
plt.ylabel("Reward (out of 200)")
plt.xlabel("Training Episodes (100 per epoch)")
plt.show()