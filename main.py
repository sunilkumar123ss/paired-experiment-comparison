"""Paired-seed experiment comparison with deterministic bootstrap intervals."""
import argparse
import json
from pathlib import Path
import math
import random
import statistics
import sys


def percentile(values, probability):
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    low, high = math.floor(position), math.ceil(position)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def compare(baseline, candidate, goals, resamples=2000, random_seed=7):
    if type(resamples) is not int or not 100 <= resamples <= 100000:
        raise ValueError("resamples must be an integer from 100 to 100000")
    if type(random_seed) is not int:
        raise ValueError("random_seed must be an integer")
    if not isinstance(goals, dict) or not goals or any(v not in ("maximize", "minimize") for v in goals.values()):
        raise ValueError("goals must map metric names to maximize or minimize")

    def index(rows):
        if not isinstance(rows, list) or len(rows) < 2:
            raise ValueError("each experiment needs at least two paired seeds")
        result = {}
        for row in rows:
            seed = row["seed"]
            if type(seed) is not int or seed in result:
                raise ValueError("seeds must be unique integers")
            metrics = row["metrics"]
            for metric in goals:
                value = metrics[metric]
                if type(value) not in (int, float) or not math.isfinite(value):
                    raise ValueError("metric values must be finite numbers")
            result[seed] = metrics
        return result

    base, new = index(baseline), index(candidate)
    if base.keys() != new.keys():
        raise ValueError("baseline and candidate must contain identical seeds")
    seeds, output = sorted(base), {}
    for metric in sorted(goals):
        before = [base[seed][metric] for seed in seeds]
        after = [new[seed][metric] for seed in seeds]
        sign = 1 if goals[metric] == "maximize" else -1
        improvements = [sign * (b - a) for a, b in zip(before, after)]
        rng = random.Random(random_seed)
        draws = [statistics.mean(rng.choices(improvements, k=len(improvements))) for _ in range(resamples)]
        output[metric] = {
            "direction": goals[metric], "baseline_mean": statistics.mean(before),
            "candidate_mean": statistics.mean(after), "mean_improvement": statistics.mean(improvements),
            "paired_improvements": dict(zip(map(str, seeds), improvements)),
            "improved_seed_fraction": sum(x > 0 for x in improvements) / len(improvements),
            "bootstrap_percentile_95_interval": [percentile(draws, 0.025), percentile(draws, 0.975)],
        }
    return {"paired_seeds": seeds, "resamples": resamples, "random_seed": random_seed, "metrics": output}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--resamples", type=int, default=2000)
    args = parser.parse_args()
    try:
        input_path = Path(args.input)
        if not input_path.is_absolute():
            input_path = Path(__file__).resolve().parent / input_path
        with input_path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        print(json.dumps(compare(data["baseline"], data["candidate"], data["goals"], args.resamples),
                         indent=2, allow_nan=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"Invalid experiment comparison: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
