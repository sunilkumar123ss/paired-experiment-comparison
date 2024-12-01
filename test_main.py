import unittest
from main import compare, percentile


def runs(values):
    return [{"seed": index, "metrics": {"score": value}} for index, value in enumerate(values)]


class ComparisonTests(unittest.TestCase):
    def test_constant_paired_gain(self):
        result = compare(runs([1, 2, 3]), runs([2, 3, 4]), {"score": "maximize"}, 100)["metrics"]["score"]
        self.assertEqual(result["mean_improvement"], 1)
        self.assertEqual(result["bootstrap_percentile_95_interval"], [1, 1])

    def test_minimize_and_reproducibility(self):
        args = (runs([3, 4, 5]), runs([2, 4, 3]), {"score": "minimize"}, 100)
        self.assertEqual(compare(*args), compare(*args))
        self.assertEqual(compare(*args)["metrics"]["score"]["mean_improvement"], 1)
        self.assertEqual(percentile([0, 10], 0.5), 5)

