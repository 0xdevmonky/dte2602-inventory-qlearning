import numpy as np
from parameters import (
    MAX_INVENTORY,
    MAX_ORDER,
    HOLDING_COST,
    STOCKOUT_COST,
    ORDER_COST,
    DEMAND_MEAN,
    ITEM_SALE_PRICE,
)


class InventoryEnv:
    def __init__(self, seed=1):
        # Reproducable random demand
        self.rng = np.random.default_rng(seed)
        self.inventory = 0

    def reset(self):
        # Empty warehouse at start of episode
        self.inventory = 0
        return self.inventory

    def step(self, action):
        # Cap order and inventory
        order = min(action, MAX_ORDER)
        self.inventory = min(self.inventory + order, MAX_INVENTORY)

        # Random demand and sales
        demand = self.rng.poisson(DEMAND_MEAN)
        sold = min(self.inventory, demand)
        self.inventory -= sold

        # Holding, stockout and order costs
        holding = self.inventory * HOLDING_COST
        stockout = max(0, demand - sold) * STOCKOUT_COST
        order_cost = order * ORDER_COST

        # Profit from sales minus costs
        reward = sold * ITEM_SALE_PRICE - holding - stockout - order_cost

        # Fixed-length episodes (done controlled outside)
        done = False
        return self.inventory, reward, done
