# Cache Block Size Research

This project studies how cache block size changes cache hit rate and memory traffic for sequential, strided, and random memory access.

## Research question

How does changing CPU cache block size affect cache hit rate and memory traffic under sequential, strided, and random memory access patterns?

## Model

The experiment uses a Python cache simulator. It models a 32 KiB, four-way set-associative cache with least-recently-used replacement. The tested block sizes are 16, 32, 64, 128, and 256 bytes.

The sequential workload reads 4-byte words through a 64 KiB address range. The strided workload reads one address every 64 bytes through the same range. The random workload makes 10,000 aligned 4-byte accesses within a 1 MiB address range. Five fixed random seeds are used for each block size.

This is a simulation, not a measurement of a physical processor. The results depend on the assumptions and workloads defined in the script.

## Run the experiment

Python 3 is required for the simulator. Matplotlib is needed only to regenerate the charts.

```bash
python cache_experiment.py
```

The command creates `results.csv` in the current folder. To choose another output file:

```bash
python cache_experiment.py --output results.csv
```

To regenerate the charts after creating `results.csv`, install the package in `requirements.txt` and run:

```bash
pip install -r requirements.txt
python make_charts.py
```

## Output

The CSV contains one record for each workload and block-size combination. Random workloads have five records per block size, one for each seed. Each record includes the number of hits and misses, hit and miss rates, and estimated memory traffic.

Memory traffic is estimated as:

`number of cache misses × cache block size`

This estimate counts bytes transferred on cache-line fills. It does not model writebacks, prefetching, multi-level caches, or timing.

## Reproducibility

The random workloads use fixed seeds: 11, 22, 33, 44, and 55. Running the script with the same Python implementation and settings produces the same access sequences and results.

## Files

- `cache_experiment.py` — cache simulator and experiment runner
- `results.csv` — generated experiment data
- `make_charts.py` — creates the charts from the CSV file
- `requirements.txt` — charting dependency
- `charts/` — plots generated from the CSV
