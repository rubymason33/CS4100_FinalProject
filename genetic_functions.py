import numpy as np


# -------------------- Fitness functions --------------------

# ideas: avg row/col/box sum, # conflicts in each row/col/box
def row_conflicts(arr):
    return np.sum(9 - np.apply_along_axis(lambda row: len(np.unique(row)), axis=1, arr=arr))


def col_conflicts(arr):
    return np.sum(9 - np.apply_along_axis(lambda col: len(np.unique(col)), axis=0, arr=arr))


def box_conflicts(arr):
    conflicts = 0
    for i in range(3):
        for j in range(3):
            block = arr[i*3:(i+1)*3, j*3:(j+1)*3].flatten()
            conflicts += 9 - len(np.unique(block))
    return conflicts


def total_conflicts(arr):
    return row_conflicts(arr) + col_conflicts(arr) + box_conflicts(arr)


# --------------------- Agent functions ---------------------

# ideas: randomly swap any two values, randomly change a value,
# replace duplicate value with random number, if row/col sum > correct --> np.min(rand_idx, rand_idx-1)

def shuffle_row(arr, mutable, k=1):
    for i in range(k):
        row_idx = np.random.randint(0, 9)
        row_mutables = np.array([col for (r, col) in mutable if r == row_idx])
        col1, col2 = np.random.choice(row_mutables, 2, replace=False)
        arr[row_idx, col1], arr[row_idx, col2] = arr[row_idx, col2], arr[row_idx, col1]
    return arr


def greedy_shuffle_row(arr, mutable, k=1):
    for i in range(k*5):
        num_conflicts = total_conflicts(arr)
        row_idx = np.random.randint(0, 9)
        row_mutables = np.array([col for (r, col) in mutable if r == row_idx])
        col1, col2 = np.random.choice(row_mutables, 2, replace=False)
        arr[row_idx, col1], arr[row_idx, col2] = arr[row_idx, col2], arr[row_idx, col1]
        if total_conflicts(arr) > num_conflicts:
            rnd = np.random.randn()
            if rnd < 0.9:
                arr[row_idx, col1], arr[row_idx, col2] = arr[row_idx, col2], arr[row_idx, col1]
    return arr


def greedy_swap(arr, mutable, k=1):
    for i in range(k):
        num_conflicts = total_conflicts(arr)
        idx1, idx2 = [mutable[idx] for idx in np.random.choice(len(mutable), 2, replace=False)]
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
        if total_conflicts(arr) > num_conflicts:
            rnd = np.random.randn()
            if rnd < 0.9:
                arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr


def greedy_change(arr, mutable, k=1):
    for i in range(10):
        num_conflicts = total_conflicts(arr)
        idx = mutable[np.random.choice(len(mutable), 1).item()]
        original = arr[idx]
        arr[idx] = np.random.randint(1, 10)
        if total_conflicts(arr) > num_conflicts:
            rnd = np.random.randn()
            if rnd < 0.9:
                arr[idx] = original
    return arr


def random_swap(arr, mutable, k=1):
    idx1, idx2 = [mutable[idx] for idx in np.random.choice(len(mutable), 2, replace=False)]
    arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr


def random_change(arr, mutable, k=1):
    idx = mutable[np.random.choice(len(mutable), 1).item()]
    arr[idx] = np.random.randint(1, 10)
    return arr


def replace_dup_rows(arr, mutable, k=1):
    for row_idx in range(9):
        row = arr[row_idx]
        row_mutables = np.array([col for (r, col) in mutable if r == row_idx])
        included, counts = np.unique(row, return_counts=True)
        if len(included) == 9:
            continue

        duplicates = included[counts > 1]
        dup_mutable_idx = row_mutables[np.isin(row[row_mutables], duplicates)]

        duplicate_idx = np.random.choice(dup_mutable_idx)
        excluded_val = np.random.choice(np.setdiff1d(np.arange(1, 10), included))

        arr[row_idx, duplicate_idx] = excluded_val
    return arr


def replace_dup_cols(arr, mutable, k=1):
    for col_idx in range(9):
        col = arr[:, col_idx]
        col_mutables = np.array([row for (row, c) in mutable if c == col_idx])
        included, counts = np.unique(col, return_counts=True)

        if len(included) == 9:
            continue

        duplicates = included[counts > 1]
        dup_mutable_idx = col_mutables[np.isin(col[col_mutables], duplicates)]

        duplicate_idx = np.random.choice(dup_mutable_idx)
        excluded_val = np.random.choice(np.setdiff1d(np.arange(1, 10), included))

        arr[duplicate_idx, col_idx] = excluded_val
    return arr


def replace_dup_boxes(arr, mutable, k=1):
    for box_row in range(3):
        for box_col in range(3):
            box_start_row, box_start_col = box_row * 3, box_col * 3
            box_values = arr[box_start_row:box_start_row + 3, box_start_col:box_start_col + 3]

            box_mutables = [(r, c) for (r, c) in mutable if
                            box_start_row <= r < box_start_row + 3 and box_start_col <= c < box_start_col + 3]

            included, counts = np.unique(box_values, return_counts=True)
            if len(included) == 9:
                continue

            duplicates = included[counts > 1]
            dup_mutable_idx = [(r, c) for (r, c) in box_mutables if arr[r, c] in duplicates]

            duplicate_idx = dup_mutable_idx[np.random.choice(len(dup_mutable_idx))]
            excluded_val = np.random.choice(np.setdiff1d(np.arange(1, 10), included))

            arr[duplicate_idx] = excluded_val

    return arr


def shuffle_boxes(arr, mutable, k=1):
    for _ in range(k):
        i, j = np.random.randint(0, 3, 2)
    # for i in range(3):
    #     for j in range(3):
        box_indices = [(r, c) for r in range(i*3, (i+1)*3)
                             for c in range(j*3, (j+1)*3)
                             if (r, c) in mutable]
        values = [arr[r, c] for (r, c) in box_indices]
        if len(values) > 1:
            np.random.shuffle(values)
            for (r, c), val in zip(box_indices, values):
                arr[r, c] = val
    return arr

# --------------------------------------------------------------------------------