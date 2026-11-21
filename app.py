import math
import random
from statistics import mean

def analyze(data):
    before, after = data["before"], data["after"]
    draws, seed = data["draws"], data["seed"]
    if len(before) != len(after) or not 2 <= len(before) <= 500 or not isinstance(draws,int) or not 100 <= draws <= 10000:
        raise ValueError("Provide 2–500 paired values and 100–10,000 draws")
    differences = [b-a for a,b in zip(before,after)]
    if not all(map(math.isfinite,differences)):
        raise ValueError("Differences must be finite")
    rng = random.Random(seed)
    means = sorted(mean(rng.choices(differences, k=len(differences))) for _ in range(draws))
    return {"mean":mean(differences),"lower":means[int(.025*(draws-1))],"upper":means[int(.975*(draws-1))]}

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
