import csv
import os


class Table:
    def __init__(self, csv_path: str):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        self.name = os.path.splitext(os.path.basename(csv_path))[0]
        self.rows = []

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError("CSV file has no header")

            for row in reader:
                self.rows.append(row)


class QueryEngine:
    def __init__(self, table: Table):
        self.table = table

    def execute(self, parsed_query: dict):
        rows = self.table.rows

        # 1️ WHERE filtering
        if parsed_query["where"]:
            rows = self._apply_where(rows, parsed_query["where"])

        # 2️ COUNT aggregation
        if parsed_query["count"] is not None:
            return self._apply_count(rows, parsed_query["count"])

        # 3️ SELECT projection
        return self._apply_select(rows, parsed_query["select"])

    def _apply_where(self, rows, where):
        col = where["column"]
        op = where["operator"]
        val = where["value"]

        if col not in rows[0]:
            raise ValueError(f"Column not found in WHERE: {col}")

        def compare(row_value):
            try:
                row_value = float(row_value)
                compare_value = float(val)
            except ValueError:
                row_value = str(row_value)
                compare_value = str(val)

            if op == "=":
                return row_value == compare_value
            if op == "!=":
                return row_value != compare_value
            if op == ">":
                return row_value > compare_value
            if op == "<":
                return row_value < compare_value
            if op == ">=":
                return row_value >= compare_value
            if op == "<=":
                return row_value <= compare_value

            raise ValueError(f"Unsupported operator: {op}")

        return [row for row in rows if compare(row[col])]

    def _apply_count(self, rows, column):
        if column == "*":
            return len(rows)

        if column not in rows[0]:
            raise ValueError(f"Column not found in COUNT(): {column}")

        return sum(1 for row in rows if row[column] not in ("", None))

    def _apply_select(self, rows, columns):
        if columns == ["*"]:
            return rows

        for col in columns:
            if col not in rows[0]:
                raise ValueError(f"Column not found in SELECT: {col}")

        result = []
        for row in rows:
            projected = {col: row[col] for col in columns}
            result.append(projected)

        return result
