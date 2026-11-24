import argparse
import csv
import random
from pathlib import Path

CACHE_CAPACITY = 32 * 1024
ASSOCIATIVITY = 4
BLOCK_SIZES = [16, 32, 64, 128, 256]
DATA_SIZE = 64 * 1024
WORD_SIZE = 4
RANDOM_MEMORY_SIZE = 1024 * 1024
RANDOM_ACCESSES = 10000
RANDOM_SEEDS = [11, 22, 33, 44, 55]


class Cache:
    def __init__(self, capacity, block_size, associativity):
        self.block_size = block_size
        self.associativity = associativity
        self.set_count = capacity // (block_size * associativity)
        self.sets = [[] for _ in range(self.set_count)]
        self.hits = 0
        self.misses = 0

    def access(self, address):
        block_number = address // self.block_size
        set_index = block_number % self.set_count
        tag = block_number // self.set_count
        current_set = self.sets[set_index]

        if tag in current_set:
            self.hits += 1
            current_set.remove(tag)
            current_set.insert(0, tag)
        else:
            self.misses += 1
            if len(current_set) == self.associativity:
                current_set.pop()
            current_set.insert(0, tag)

    def result(self, pattern, seed, accesses):
        hit_rate = self.hits / accesses * 100
        miss_rate = self.misses / accesses * 100
        traffic = self.misses * self.block_size
        return {
            "pattern": pattern,
            "seed": seed,
            "block_size_bytes": self.block_size,
            "cache_capacity_bytes": CACHE_CAPACITY,
            "associativity": self.associativity,
            "accesses": accesses,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_percent": round(hit_rate, 4),
            "miss_rate_percent": round(miss_rate, 4),
            "memory_traffic_bytes": traffic,
        }


def run_workload(pattern, block_size, addresses, seed=""):
    cache = Cache(CACHE_CAPACITY, block_size, ASSOCIATIVITY)
    for address in addresses:
        cache.access(address)
    return cache.result(pattern, seed, len(addresses))


def build_results():
    rows = []

    sequential = range(0, DATA_SIZE, WORD_SIZE)
    strided = range(0, DATA_SIZE, 64)

    for block_size in BLOCK_SIZES:
        rows.append(run_workload("sequential", block_size, sequential))
        rows.append(run_workload("strided_64_bytes", block_size, strided))

        for seed in RANDOM_SEEDS:
            generator = random.Random(seed)
            addresses = [
                generator.randrange(0, RANDOM_MEMORY_SIZE // WORD_SIZE) * WORD_SIZE
                for _ in range(RANDOM_ACCESSES)
            ]
            rows.append(
                run_workload("random", block_size, addresses, seed)
            )

    return rows


def save_results(rows, output_path):
    fieldnames = list(rows[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="results.csv",
        help="CSV output file"
    )
    args = parser.parse_args()

    rows = build_results()
    output_path = Path(args.output)
    save_results(rows, output_path)
    print(f"Saved {len(rows)} experiment records to {output_path}")


if __name__ == "__main__":
    main()
