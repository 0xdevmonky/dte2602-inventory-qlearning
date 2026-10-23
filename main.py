from q_learning import QLearningAgent
from environment import InventoryEnv
import numpy as np
import matplotlib.pyplot as plt
from parameters import (
    EPISODES,
    EVAL_EPISODES,
    MAXSTEPS,
    MAX_ORDER,
    NR_OF_SEEDS,
    ALPHA,
    GAMMA,
    EPSILON_START,
    EPSILON_DECAY_ENABLE,
    MAX_INVENTORY,
    DEMAND_MEAN,
    ITEM_SALE_PRICE,
)


def baseline_random(env, episodes):
    # Always order random amouts (within max-order range)
    rewards = []
    for _ in range(episodes):
        state = env.reset()
        total = 0
        for _ in range(MAXSTEPS):
            action = env.rng.integers(0, MAX_ORDER + 1)
            state, reward, _ = env.step(action)
            total += reward
        rewards.append(total)
    return rewards

def baseline_fixed(env, episodes, order=DEMAND_MEAN):
    # Always order the average demand
    rewards = []
    for _ in range(episodes):
        state = env.reset()
        total = 0
        for _ in range(MAXSTEPS):
            state, reward, _ = env.step(order)
            total += reward
        rewards.append(total)
    return rewards

def plot_learning_curve(history, filename="learning_curve.png"):
    window = 20
    smoothed = np.convolve(history, np.ones(window) / window, mode="valid")

    plt.figure()
    plt.plot(history, alpha=0.3, label="Raw")
    plt.plot(range(window - 1, len(history)), smoothed, label="Smoothed")
    plt.title("Learning curve")
    plt.xlabel("Episode")
    plt.ylabel("Total reward")
    plt.legend()
    plt.savefig(filename)
    plt.close()

def print_policy(agent):
    # Show the learned policy for all inventory levels
    print("\nLearned policy (inventory -> best order):")
    for inv in range(MAX_INVENTORY + 1):
        best = int(agent.q[inv].argmax())
        print(f"  Inventory {inv:2d} -> order {best}")

def main():
    seeds = list(range(1, NR_OF_SEEDS + 1))
    ql_means = []
    rand_means = []
    fixed_means = []
    last_history = None

    for seed in seeds:
        agent = QLearningAgent(seed)
        agent.train(EPISODES)
        eval_rewards = agent.evaluate(EVAL_EPISODES)
        ql_means.append(np.mean(eval_rewards))

        env = InventoryEnv(seed)
        rand_means.append(np.mean(baseline_random(env, EVAL_EPISODES)))
        fixed_means.append(np.mean(baseline_fixed(env, EVAL_EPISODES)))
 
        last_history = agent.history
        print(f"Seed {seed} done")

    print("\n=== Parameters ===")
    print(f"ALPHA:            {ALPHA}")
    print(f"GAMMA:            {GAMMA}")
    print(f"EPSILON_START:    {EPSILON_START}")
    print(f"EPSILON_DECAY:    {EPSILON_DECAY_ENABLE}")
    print(f"EPISODES:         {EPISODES}")
    print(f"EVAL_EPISODES:    {EVAL_EPISODES}")
    print(f"NR_OF_SEEDS:      {NR_OF_SEEDS}")
    print(f"MAXSTEPS:         {MAXSTEPS}")
    print(f"MAX_INVENTORY:    {MAX_INVENTORY}")
    print(f"MAX_ORDER:        {MAX_ORDER}")
    print(f"DEMAND_MEAN:      {DEMAND_MEAN}")
    print(f"ITEM_SALE_PRICE:  {ITEM_SALE_PRICE}")
    print("==================\n")

    print(f"Q-learning: {np.mean(ql_means):.0f} ± {np.std(ql_means):.1f}")
    print(f"Random:     {np.mean(rand_means):.0f} ± {np.std(rand_means):.1f}")
    print(f"Fixed:      {np.mean(fixed_means):.0f} ± {np.std(fixed_means):.1f}")

    # Comparison plot
    labels = ["Q-learning", "Random", "Fixed"]
    means = [np.mean(ql_means), np.mean(rand_means), np.mean(fixed_means)]
    stds = [np.std(ql_means), np.std(rand_means), np.std(fixed_means)]

    plt.figure()
    plt.bar(labels, means, yerr=stds, capsize=5)
    plt.ylabel("Mean reward")
    plt.title("Comparison across seeds")
    plt.savefig("comparison.png")
    plt.close()

    # Learning curve from last seed
    if last_history is not None:
        print_policy(agent)
        plot_learning_curve(last_history)
        print("Plots saved: comparison.png and learning_curve.png")

if __name__ == "__main__":
    main()
