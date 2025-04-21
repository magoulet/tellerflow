# Teller to CSV Exporter

A Python script to export transactions from Teller.io to CSV files, organized by financial institution and account type.

## Features

- Fetches transactions from multiple bank accounts via Teller API
- Generates timestamped CSV files in GnuCash-compatible format
- Supports checking, savings, and credit card accounts
- Secure credential management using YAML configuration

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure accounts**:
   - Place your Teller certificates in `certs/`
   - Edit `config/accounts.yaml` with your:
     - Teller app ID
     - Account tokens
     - Account IDs

3. **Run the exporter**:
   ```bash
   python teller_to_csv.py
   ```

   Outputs will be saved in `exports/` with naming convention:  
   `[Institution]_[AccountType]_[YYYYMMDD].csv`

## File Structure

```
.
├── certs/                  # Teller certificates (ignored by git)
│   ├── certificate.pem
│   └── private_key.pem
├── config/                 # Account configuration (ignored by git)
│   └── accounts.yaml
├── exports/                # Generated CSV files (ignored by git)
├── README.md
├── requirements.txt        # Python dependencies
└── teller_to_csv.py        # Main script
```

## Security Note

All sensitive files are excluded via `.gitignore`:
- Certificate files (`certs/`)
- Account configuration (`config/accounts.yaml`)
- Export directory (`exports/`)


## License

[MIT](LICENSE)
