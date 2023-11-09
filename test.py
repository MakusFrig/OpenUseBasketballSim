#just a test file

import random


DISTANCES = [4, 10, 15, 24]

DISTANCES_WEIGHT = [0.2, 0.2, 0.3, 0.3]

print(random.choices(DISTANCES, weights=DISTANCES_WEIGHT)[0])
