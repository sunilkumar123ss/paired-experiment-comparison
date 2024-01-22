import unittest
from main import compare, percentile


def runs(values):
    return [{"seed": index, "metrics": {"score": value}} for index, value in enumerate(values)]


class ComparisonTests(unittest.TestCase):
    def test_constant_paired_gain(self):
        result = compare(runs([1, 2, 3]), runs([2, 3, 4]), {"score": "maximize"}, 100)["metrics"]["score"]
        self.assertEqual(result["mean_improvement"], 1)
        self.assertEqual(result["bootstrap_percentile_95_interval"], [1, 1])

