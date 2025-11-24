import numpy as np
import pandas as pd


def index_diagnostic(master_index, other_index, n=10):
    master = np.asarray(pd.Index(master_index).astype(float))
    other = np.asarray(pd.Index(other_index).astype(float))

    print("master dtype:", master.dtype, "len:", len(master))
    print("other  dtype:", other.dtype,  "len:", len(other))
    print("master min/max:", master.min(), master.max())
    print("other  min/max:", other.min(), other.max())

    # Quick equality check
    if np.array_equal(master, other):
        print("Indices are exactly equal (np.array_equal).")
    else:
        print("Not exactly equal. Showing examples of mismatches:")
        # values in master not in other
        only_master = np.setdiff1d(master, other)[:n]
        only_other = np.setdiff1d(other, master)[:n]
        print("only in master (examples):", only_master)
        print("only in other  (examples):", only_other)

        # show nearest diffs for few master examples
        diffs = []
        for v in master[:n]:
            j = np.argmin(np.abs(other - v))
            diffs.append((v, other[j], float(v - other[j])))
        print("Nearest diffs (master_val, other_nearest, delta):")
        for a, b, d in diffs[:n]:
            print(a, b, d)
