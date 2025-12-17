import re


class SQLParseError(Exception):
    pass


def parse_sql(query: str) -> dict:
    """
    Parse a simplified SQL SELECT query.
    """

    query = query.strip().rstrip(";")

    # Normalize whitespace
    query = re.sub(r"\s+", " ", query)

    parsed = {
        "select": None,
        "from": None,
        "where": None,
        "count": None
    }

    # --- SELECT + FROM ---
    match = re.match(r"(?i)^select (.+?) from (.+)$", query)
    if not match:
        raise SQLParseError("Invalid SQL syntax. Expected SELECT ... FROM ...")

    select_part = match.group(1).strip()
    remainder = match.group(2).strip()

    # --- COUNT ---
    if select_part.lower().startswith("count("):
        parsed["count"] = select_part[6:-1].strip()
    else:
        if select_part == "*":
            parsed["select"] = ["*"]
        else:
            parsed["select"] = [c.strip() for c in select_part.split(",")]

    # --- WHERE ---
    where_match = re.search(r"(?i)\swhere\s", remainder)
    if where_match:
        table_part, where_part = re.split(r"(?i)\swhere\s", remainder, 1)
        parsed["from"] = table_part.strip()
        parsed["where"] = _parse_where(where_part.strip())
    else:
        parsed["from"] = remainder.strip()

    return parsed


def _parse_where(condition: str) -> dict:
    """
    Parse WHERE clause: column operator value
    """

    operators = ["<=", ">=", "!=", "=", "<", ">"]

    for op in operators:
        if op in condition:
            left, right = condition.split(op, 1)
            value = right.strip()

            # Parse value type
            if value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            else:
                try:
                    if "." in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass

            return {
                "column": left.strip(),
                "operator": op,
                "value": value
            }

    raise SQLParseError("Invalid WHERE clause")
