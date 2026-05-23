#!/usr/bin/env python3
"""Analytics Dashboard - Natural language data analytics."""

import json, sys, csv
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class DataSource:
    name: str
    type: str
    connection: str
    tables: list = field(default_factory=list)

@dataclass
class QueryResult:
    query: str
    columns: list
    rows: list
    chart_type: str = "table"
    execution_time: float = 0.0

class AnalyticsEngine:
    def __init__(self):
        self.sources = {}
        self.history = []

    def connect(self, name: str, conn_str: str):
        if "postgresql" in conn_str:
            dtype = "postgresql"
        elif conn_str.endswith(".csv"):
            dtype = "csv"
        else:
            dtype = "unknown"
        self.sources[name] = DataSource(name=name, type=dtype, connection=conn_str)
        return self.sources[name]

    def query(self, natural_language: str, source: str = None) -> QueryResult:
        parsed = self._parse_intent(natural_language)
        result = QueryResult(
            query=natural_language,
            columns=parsed["columns"],
            rows=parsed.get("sample_data", []),
            chart_type=parsed.get("chart", "table"),
        )
        self.history.append(result)
        return result

    def _parse_intent(self, text: str) -> dict:
        lower = text.lower()
        if "revenue" in lower or "sales" in lower:
            return {"columns": ["month", "revenue"], "chart": "line",
                    "sample_data": [["Jan", 12000], ["Feb", 15000], ["Mar", 18000]]}
        elif "count" in lower or "number" in lower:
            return {"columns": ["category", "count"], "chart": "bar",
                    "sample_data": [["A", 45], ["B", 32], ["C", 67]]}
        elif "distribution" in lower or "percentage" in lower:
            return {"columns": ["segment", "percentage"], "chart": "pie",
                    "sample_data": [["Direct", 35], ["Organic", 45], ["Referral", 20]]}
        return {"columns": ["metric", "value"], "chart": "table",
                "sample_data": [["Result", "See data source"]]}

    def detect_anomalies(self, data: list, threshold: float = 2.0) -> list:
        if len(data) < 3:
            return []
        mean = sum(data) / len(data)
        std = (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5
        anomalies = []
        for i, val in enumerate(data):
            if std > 0 and abs(val - mean) / std > threshold:
                anomalies.append({"index": i, "value": val, "z_score": round((val - mean) / std, 2)})
        return anomalies

    def export_csv(self, result: QueryResult, output: str):
        with open(output, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(result.columns)
            w.writerows(result.rows)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [query|connect|export] ...")
        sys.exit(1)

    engine = AnalyticsEngine()
    cmd = sys.argv[1]

    if cmd == "query":
        text = " ".join(sys.argv[2:])
        result = engine.query(text)
        print(f"Query: {result.query}")
        print(f"Chart: {result.chart_type}")
        print(f"Columns: {result.columns}")
        for row in result.rows:
            print(f"  {row}")
    elif cmd == "connect":
        source = engine.connect("default", sys.argv[2])
        print(f"Connected: {source.name} ({source.type})")

if __name__ == "__main__":
    main()
