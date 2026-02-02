import random
import csv

genes = ["TP53", "EGFR", "BRAF", "KRAS", "PIK3CA"]
tumor_types = ["lung", "breast", "colon", "melanoma"]

with open("data/mutations.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["sample_id", "gene", "variant", "vaf", "tumor_type"])

    for i in range(1000):
        writer.writerow([
            f"S{i}",
            random.choice(genes),
            f"p.V{random.randint(100,600)}E",
            round(random.uniform(0.05, 0.9), 2),
            random.choice(tumor_types),
        ])