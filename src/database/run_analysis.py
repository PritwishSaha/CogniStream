
from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "cognistream.duckdb"
SQL_PATH = PROJECT_ROOT / "sql" / "cognistream_analysis.sql"


def main():
    if not DATABASE_PATH.is_file():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    if not SQL_PATH.is_file():
        raise FileNotFoundError(
            f"SQL file not found: {SQL_PATH}"
        )

    sql_text = SQL_PATH.read_text(encoding="utf-8")

    # Each query in this file is separated by a semicolon.
    queries = [
        query.strip()
        for query in sql_text.split(";")
        if query.strip()
    ]

    connection = duckdb.connect(
        str(DATABASE_PATH),
        read_only=True,
    )

    try:
        print("=" * 70)
        print("COGNISTREAM SQL ANALYSIS")
        print("=" * 70)

        for number, query in enumerate(queries, start=1):
            print(f"\n{'=' * 70}")
            print(f"QUERY {number}")
            print("=" * 70)

            result = connection.execute(query)

            if result.description is not None:
                columns = [
                    description[0]
                    for description in result.description
                ]

                rows = result.fetchmany(20)

                if not rows:
                    print("No rows returned.")

                else:
                    print(" | ".join(columns))
                    print("-" * 70)

                    for row in rows:
                        print(" | ".join(
                            str(value) for value in row
                        ))

                    if len(rows) == 20:
                        print(
                            "\nShowing the first 20 rows "
                            "when more results may exist."
                        )

        print(f"\n{'=' * 70}")
        print("SQL ANALYSIS COMPLETED")
        print("=" * 70)

    finally:
        connection.close()


if __name__ == "__main__":
    main()

