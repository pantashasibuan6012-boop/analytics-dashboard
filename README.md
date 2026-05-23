# Analytics Dashboard

Real-time data analytics dashboard with natural language querying. Connect multiple data sources and get instant visualizations.

## Features
- Natural language query interface
- Multi-source connections (PostgreSQL, BigQuery, CSV)
- Auto-generated charts and visualizations
- Anomaly detection and alerts
- Scheduled report generation

## Installation
```
pip install -r requirements.txt
```

## Usage
```
python main.py query "Show me revenue by month for 2024"
python main.py connect postgresql://user:pass@host/db
python main.py export --format csv
```

## License
MIT