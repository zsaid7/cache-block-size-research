import csv
from pathlib import Path
import matplotlib.pyplot as plt

with open("results.csv", newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

patterns = {
    "sequential": "Sequential access",
    "strided_64_bytes": "Strided access (64-byte stride)",
    "random": "Random access",
}

Path("charts").mkdir(exist_ok=True)

for pattern, title in patterns.items():
    sizes = [16, 32, 64, 128, 256]
    rates = []

    for size in sizes:
        values = [
            float(row["hit_rate_percent"])
            for row in rows
            if row["pattern"] == pattern
            and int(row["block_size_bytes"]) == size
        ]
        rates.append(sum(values) / len(values))

    plt.figure()
    plt.plot(sizes, rates, marker="o")
    plt.xlabel("Cache block size (bytes)")
    plt.ylabel("Cache hit rate (%)")
    plt.title(title)
    plt.xticks(sizes)
    plt.grid(True)
    plt.savefig(
        Path("charts") / f"{pattern}_hit_rate.png",
        dpi=160,
        bbox_inches="tight"
    )
    plt.close()
