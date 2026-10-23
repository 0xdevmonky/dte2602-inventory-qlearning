import random
import numpy as np
from environment import InventoryEnv
from parameters import (
    ALPHA,
    EPSILON_START,
    GAMMA,
    MAXSTEPS,
    MAX_INVENTORY,
    MAX_ORDER,
    EPSILON_DECAY,
    EPSILON_DECAY_ENABLE,
    EPSILON_END,
)


class QLearningAgent:
    def __init__(self, seed=1):
        self.epsilon = EPSILON_START
        self.env = InventoryEnv(seed)
        self.q = np.zeros((MAX_INVENTORY + 1, MAX_ORDER + 1))
        self.rng = random.Random(seed)
        self.history = []

    def choose(self, state):
        # Epsilon-greedy: explore or exploit
        if self.rng.random() < self.epsilon:
            return self.rng.randrange(MAX_ORDER + 1), True

        values = self.q[state]
        best_actions = [
            action
            for action in range(MAX_ORDER + 1)
            if values[action] == values.max()
        ]
        return self.rng.choice(best_actions), False

    def episode(self, learn=True):
        state = self.env.reset()
        total_reward = 0
        done = False
        step_number = 0

        while not done and step_number < MAXSTEPS:
            action, _ = self.choose(state)
            next_state, reward, done = self.env.step(action)

            if learn:
                # Q-learning update: move toward reward + discounted best next value
                old = self.q[state][action]
                best_next = self.q[next_state].max()
                self.q[state][action] = old + ALPHA * (
                    reward + GAMMA * best_next - old
                )

            state = next_state
            total_reward += reward
            step_number += 1
 
        if learn:
            self.history.append(total_reward)
        return total_reward

    def train(self, episodes):
        for _ in range(episodes):
            self.episode()
            if EPSILON_DECAY_ENABLE:
                self.epsilon = max(EPSILON_END, self.epsilon * EPSILON_DECAY)

    def evaluate(self, episodes):
        # Run greedy policy only (no learning or exploration)
        old_epsilon = self.epsilon
        self.epsilon = 0.0

        rewards = []
        for _ in range(episodes):
            reward = self.episode(learn=False)
            rewards.append(reward)

        self.epsilon = old_epsilon
        return rewards
