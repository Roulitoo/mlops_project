import csv
import os
import json
from datetime import datetime, UTC

def json_to_csv(json_path, csv_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    
    # Accès aux données horaires
    hourly = data["hourly"]
    times = hourly["time"]
    variable_names = [k for k in hourly.keys() if k != "time"]
    
    # Construction des lignes
    rows = []
    for i in range(len(times)):
        row = [times[i]] + [hourly[var][i] for var in variable_names]
        rows.append(row)

    # Création du CSV
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time"] + variable_names)
        writer.writerows(rows)

# Exemple d'utilisation :
json_file = f"data/raw/{datetime.now(UTC):%Y-%m-%d}.json"
csv_file = f"data/processed/{datetime.now(UTC):%Y-%m-%d}.csv"
os.makedirs("data/processed", exist_ok=True)
json_to_csv(json_file, csv_file)
