# Q-learning parameters
ALPHA           = 0.05  # learning rate
GAMMA           = 0.3   # discount factor
EPSILON_START   = 0.6   # exploration probability

MAXSTEPS        = 100   # episode length
EPISODES        = 1000
EVAL_EPISODES   = 100   # number of episodes used by evaluation functions in main
NR_OF_SEEDS     = 25    # seed-pool size [0, 1 , 2, ..., n - 1]

# Optional improvements
EPSILON_DECAY_ENABLE    = True
EPSILON_END             = 0.05
EPSILON_DECAY           = 0.995

# Inventory and reward parameters
MAX_INVENTORY   = 30
MAX_ORDER       = 20
HOLDING_COST    = 4
STOCKOUT_COST   = 12
ORDER_COST      = 2
DEMAND_MEAN     = 10
ITEM_SALE_PRICE = 22
