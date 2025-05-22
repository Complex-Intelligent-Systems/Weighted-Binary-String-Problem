# InstanceGenerator.py
"""
Generate synthetic Weighted-Binary-String benchmark instances.

Each call can sweep several combinations of
  • weight range                (min_weights, max_weights)
  • string length(s)            (gene_lengths)
  • representation (float / int)
  • proportion of positive vs. negative weights
and stores every instance in CSV (one file per instance) and/or in an
aggregate TXT overview, depending on the --format flag.

The optimal bit string is written as “Genes,” followed by the weight
vector so that downstream experiments know the true optimum.
"""

from __future__ import annotations
import itertools
import os
import sys
import getopt
import numpy as np


# ----------------------------------------------------------------------
# Core generator
# ----------------------------------------------------------------------
def generate_instances(
    output_dir: str,
    num_instances: int,
    min_weights: list[float],
    max_weights: list[float],
    gene_lengths: list[int],
    *,
    discrete: bool = False,
    fmt: int = 1,
    no_zero: bool = False,
    pos_percentage: float | None = None,
) -> None:
    """
    Parameters
    ----------
    output_dir : str
        Destination folder (created if necessary).
    num_instances : int
        How many independent instances per (min,max,length) combination.
    min_weights / max_weights : list[float]
        Lower / upper bounds for the weight interval.  Provide lists of
        equal length to sweep several ranges (cartesian product is taken).
    gene_lengths : list[int]
        List of binary-string lengths to generate.
    discrete : bool, default False
        * True  → integer weights  via np.random.randint
        * False → floating weights via np.random.uniform
    fmt : {0,1,2}, default 1
        0 → single TXT overview only
        1 → individual CSV per instance only
        2 → both representations
    no_zero : bool, default False
        Re-sample until no weight equals zero.
    pos_percentage : float | None, default None
        If given (e.g. 70.0), exactly that percentage of the weights
        will be positive and the rest negative.

    Notes
    -----
    * Weights are rounded to two decimals in the continuous case.
    * The optimal gene (bit = 1  ⇔  weight > 0) and its fitness value
      are stored inside each CSV for reproducibility.
    """
    os.makedirs(output_dir, exist_ok=True)

    combinations = list(itertools.product(min_weights, max_weights, gene_lengths))
    use_overview = fmt in (0, 2)
    use_single   = fmt in (1, 2)

    for min_w, max_w, length in combinations:

        # ------------------------------------------------------------------
        # Optional overview file (TXT)
        # ------------------------------------------------------------------
        if use_overview:
            overview_path = os.path.join(
                output_dir,
                f"Instance_length_{length}"
                f"_weights_{min_w}_to_{max_w}"
                f"_{'D' if discrete else 'C'}.txt",
            )
            overview_fp = open(overview_path, "w", encoding="utf-8")

        for _ in range(num_instances):

            # --------------------------------------------------------------
            # 1. generate a weight vector
            # --------------------------------------------------------------
            if pos_percentage is None:          # “fully random” scenario
                weights = _sample_weights(min_w, max_w, length, discrete, no_zero)
            else:                               # controlled positive ratio
                weights = _sample_with_ratio(
                    min_w, max_w, length, pos_percentage, discrete, no_zero
                )

            # --------------------------------------------------------------
            # 2. derive optimal gene & fitness
            # --------------------------------------------------------------
            optimal_gene = (weights > 0).astype(int)
            max_fitness  = weights[optimal_gene == 1].sum()

            # --------------------------------------------------------------
            # 3. write CSV (one file per instance)
            # --------------------------------------------------------------
            if use_single:
                file_idx = _next_available_index(output_dir)
                csv_path = os.path.join(output_dir, f"instance_{file_idx}.csv")

                with open(csv_path, "w", encoding="utf-8") as fp:
                    fp.write(f"Max Fitness,{max_fitness}\n")
                    fp.write(f"String Length,{length}\n")
                    fp.write(f"Min Weight,{min_w}\n")
                    fp.write(f"Max Weight,{max_w}\n")
                    fp.write(f"Discrete,{discrete}\n")
                    fp.write(f"No Zero,{no_zero}\n")
                    fp.write(f"Pos Percentage,{pos_percentage}\n")
                    fp.write("Genes,"   + ",".join(map(str, optimal_gene)) + "\n")
                    fp.write("Weights," + ",".join(map(str, weights))      + "\n")

            # --------------------------------------------------------------
            # 4. append to overview file
            # --------------------------------------------------------------
            if use_overview:
                overview_fp.write(f"Genes:   {' '.join(map(str, optimal_gene))}\n")
                overview_fp.write(f"Weights: {' '.join(map(str, weights))}\n\n")

            print(f"Generated WBS({length}) in [{min_w},{max_w}]")

        if use_overview:
            overview_fp.close()


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _sample_weights(
    min_w: float, max_w: float, length: int, discrete: bool, no_zero: bool
) -> np.ndarray:
    """Return an array of weights without enforcing a positive/negative ratio."""
    if discrete:
        weights = np.random.randint(min_w, max_w + 1, length, dtype=int)
    else:
        weights = np.round(np.random.uniform(min_w, max_w, length), 2)

    if no_zero:
        mask = weights == 0
        while mask.any():
            if discrete:
                weights[mask] = np.random.randint(min_w, max_w + 1, mask.sum())
            else:
                weights[mask] = np.round(np.random.uniform(min_w, max_w, mask.sum()), 2)
            mask = weights == 0
    return weights


def _sample_with_ratio(
    min_w: float,
    max_w: float,
    length: int,
    pos_percentage: float,
    discrete: bool,
    no_zero: bool,
) -> np.ndarray:
    """Sample exactly pos_percentage positive and the rest negative weights."""
    pos_cnt = int(round(pos_percentage / 100 * length))
    neg_cnt = length - pos_cnt
    indices = np.random.permutation(length)
    pos_idx, neg_idx = indices[:pos_cnt], indices[pos_cnt:]

    weights = np.zeros(length, dtype=float)

    # positive part
    if discrete:
        weights[pos_idx] = np.random.randint(1 if no_zero else 0, max_w + 1, pos_cnt)
    else:
        weights[pos_idx] = np.round(np.random.uniform(0, max_w, pos_cnt), 2)

    # negative part
    if discrete:
        weights[neg_idx] = np.random.randint(min_w, 0, neg_cnt)
    else:
        weights[neg_idx] = np.round(np.random.uniform(min_w, 0, neg_cnt), 2)

    if no_zero:
        mask = weights == 0
        while mask.any():
            if discrete:
                weights[mask] = np.random.randint(min_w if mask.any() else 1, max_w + 1, mask.sum())
            else:
                weights[mask] = np.round(np.random.uniform(min_w, max_w, mask.sum()), 2)
            mask = weights == 0
    return weights


def _next_available_index(output_dir: str) -> int:
    """Return the first integer i such that instance_i.csv does not exist."""
    i = 0
    while os.path.exists(os.path.join(output_dir, f"instance_{i}.csv")):
        i += 1
    return i


# ----------------------------------------------------------------------
# Command-line interface
# ----------------------------------------------------------------------
def main(argv: list[str]) -> None:
    """
    Usage example
    -------------
    python InstanceGenerator.py
           --output_dir Instances
           --num_instances 2
           --min_weights [-10]
           --max_weights [10]
           --gene_lengths [500,1000,1500]
           --discrete
           --no_zero
           --pos_percentage 70
           --format 2
    """
    # defaults
    args = {
        "num_instances": 1,
        "min_weights":  [-10.0],
        "max_weights":  [10.0],
        "gene_lengths": [1000],
        "output_dir":   "Instances",
        "discrete":     True,
        "format":       1,
        "no_zero":      False,
        "pos_percentage": None,
    }

    opts, _ = getopt.getopt(
        argv,
        "n:a:b:l:o:wdzp:f:",
        [
            "num_instances=",
            "min_weights=",
            "max_weights=",
            "gene_lengths=",
            "output_dir=",
            "discrete",
            "no_zero",
            "pos_percentage=",
            "format=",
        ],
    )

    for opt, val in opts:
        if opt in ("-n", "--num_instances"):
            args["num_instances"] = int(val)
        elif opt in ("-a", "--min_weights"):
            args["min_weights"] = list(map(float, val.strip("[]").split(",")))
        elif opt in ("-b", "--max_weights"):
            args["max_weights"] = list(map(float, val.strip("[]").split(",")))
        elif opt in ("-l", "--gene_lengths"):
            args["gene_lengths"] = list(map(int, val.strip("[]").split(",")))
        elif opt in ("-o", "--output_dir"):
            args["output_dir"] = val
        elif opt in ("-w", "--discrete"):
            args["discrete"] = True
        elif opt in ("-z", "--no_zero"):
            args["no_zero"] = True
        elif opt in ("-p", "--pos_percentage"):
            args["pos_percentage"] = float(val)
        elif opt in ("-f", "--format"):
            args["format"] = int(val)

    generate_instances(
        args["output_dir"],
        args["num_instances"],
        args["min_weights"],
        args["max_weights"],
        args["gene_lengths"],
        discrete=args["discrete"],
        fmt=args["format"],
        no_zero=args["no_zero"],
        pos_percentage=args["pos_percentage"],
    )


if __name__ == "__main__":
    main(sys.argv[1:])
