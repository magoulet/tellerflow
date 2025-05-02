import csv
import os
import sys
from datetime import datetime

import requests
import yaml

# Load YAML config
with open("config/accounts.yaml", "r") as f:
    config = yaml.safe_load(f)

# Fetch transactions for all accounts
for institution in config["accounts"]:

    cutoff_date = None
    if "cutoff_date" in institution:
        try:
            cutoff_date = datetime.strptime(institution["cutoff_date"], "%Y-%m-%d").date()
        except ValueError:
            print(f"Warning: Invalid cutoff date '{institution['cutoff_date']}'. Skipping filter.", file=sys.stderr)

    for account in institution["accounts"]:
        # Fetch transactions
        response = requests.get(
            f"https://api.teller.io/accounts/{account['id']}/transactions",
            cert=(config["teller"]["cert_path"], config["teller"]["key_path"]),
            auth=(institution["token"], "")
        )
        transactions = response.json()

        # Skip if no transactions
        if not transactions:
            continue

        # Filter by cutoff date
        if cutoff_date:
            filtered_transactions = [
                txn for txn in transactions
                if datetime.strptime(txn["date"], "%Y-%m-%d").date() >= cutoff_date
            ]
        else:
            filtered_transactions = transactions

        # Filter by status
        filtered_transactions = [
            txn for txn in filtered_transactions
            if txn["status"] == "posted"
        ]

        # Define CSV filename (e.g., "Chase_credit_card_20240520.csv")
        csv_name = f"{institution['institution']}_{account['type']}_{datetime.now().strftime('%Y%m%d')}.csv"
        csv_path = os.path.join("exports", csv_name)

        # Write CSV
        os.makedirs("exports", exist_ok=True)
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Description", "Amount", "Category", "Status"])
            for txn in filtered_transactions:
                writer.writerow([
                    txn["date"],
                    txn["description"],
                    txn["amount"],
                    txn["details"].get("category", ""),
                    txn["status"]
                ])

        print(f"Generated: {csv_path} (Filtered: {len(transactions) - len(filtered_transactions)} transactions excluded)")