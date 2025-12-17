from engine import Table, QueryEngine
from parser import parse_sql, SQLParseError


def print_result(result):
    if isinstance(result, int):
        print(result)
        return

    if not result:
        print("No rows found.")
        return

    # Print header
    headers = result[0].keys()
    print(" | ".join(headers))
    print("-" * (len(headers) * 10))

    # Print rows
    for row in result:
        print(" | ".join(str(row[h]) for h in headers))


def main():
    print("Mini SQL Database")
    print("Type 'exit' or 'quit' to quit")

    try:
        table = Table("data/employees.csv")
        engine = QueryEngine(table)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    while True:
        query = input("sql> ").strip()

        if query.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not query:
            continue

        try:
            parsed = parse_sql(query)
            result = engine.execute(parsed)
            print_result(result)
        except SQLParseError as e:
            print(f"SQL Error: {e}")
        except Exception as e:
            print(f"Execution Error: {e}")


if __name__ == "__main__":
    main()
