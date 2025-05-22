"""
Launch InstanceGenerator.py several times with different gene lengths.

* Assumes InstanceGenerator/InstanceGenerator.py is located relative to
  this script.
* Each call produces one CSV file under the directory given by --output_dir.
"""
import subprocess

# ---------------------------------------------------------------------
# Fixed parameters
# ---------------------------------------------------------------------
OUTPUT_DIR       = "instance"
NUM_INSTANCES    = 1
MIN_WEIGHTS      = "[-25]"   # string because the generator expects [a,b] syntax
MAX_WEIGHTS      = "[25]"
NO_ZERO_FLAG     = "--no_zero"
DISCRETE_FLAG    = "--discrete"
POS_PERCENTAGE   = None      # e.g. 70 for 70 % positive weights

# ---------------------------------------------------------------------
# Gene-length sweep
# ---------------------------------------------------------------------
GENE_START  = 10_000          # first length
GENE_END    = 10_000          # last  length (inclusive)
STEP        = 250             # increment

for length in range(GENE_START, GENE_END + 1, STEP):
    cmd = [
        "python3", "InstanceGenerator/InstanceGenerator.py",
        "--output_dir",   OUTPUT_DIR,
        "--num_instances", str(NUM_INSTANCES),
        "--min_weights",  MIN_WEIGHTS,
        "--max_weights",  MAX_WEIGHTS,
        "--gene_lengths", f"[{length}]",
        NO_ZERO_FLAG,
        DISCRETE_FLAG,
    ]
    if POS_PERCENTAGE is not None:
        cmd.extend(["--pos_percentage", str(POS_PERCENTAGE)])

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)