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

