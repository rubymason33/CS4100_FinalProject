import numpy as np


# -------------------- Fitness functions --------------------

# ideas: avg row/col/box sum, # conflicts in each row/col/box
def row_conflicts(arr):
    return np.sum(9 - np.apply_along_axis(lambda row: len(np.unique(row)), axis=1, arr=arr))


def col_conflicts(arr):
    return np.sum(9 - np.apply_along_axis(lambda col: len(np.unique(col)), axis=0, arr=arr))


def row_sum_mse(arr):
    return np.mean((np.sum(arr, axis=1) - np.sum(np.arange(1, 10)))**2)


def col_sum_mse(arr):
    return np.mean((np.sum(arr, axis=0) - np.sum(np.arange(1, 10))) ** 2)

# --------------------- Agent functions ---------------------

# ideas: randomly swap any two values, randomly change a value,
# replace duplicate value with random number, if row/col sum > correct --> np.min(rand_idx, rand_idx-1)