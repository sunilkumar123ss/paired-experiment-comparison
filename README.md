# Paired experiment comparison

Compare baseline/candidate metric observations from the same random seeds. The included observations are synthetic, not measured model performance.

~~~sh
python3 main.py --input example.json --resamples 2000
python3 -m unittest -v
~~~

Choose maximize or minimize per metric. Improvement is positive in the favorable direction. The report shows paired deltas, the fraction of seeds with strict improvement, and a percentile bootstrap interval for mean improvement. Resampling preserves baseline/candidate pairs. A fixed local random seed makes the report reproducible.

At least two identical seed sets are required. Small numbers of seeds produce fragile intervals; the four-seed fixture illustrates computation only. The interval is not a paired test, multiplicity correction, deployment guarantee, or replacement for a well-designed evaluation.

## Scope

This is an educational implementation with synthetic fixtures. Run the tests and inspect the documented limits before adapting it.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
