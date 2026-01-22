"""
PostgreSQL Database Connection Template using psycopg3
Reads configuration from .env file and SQL queries from external files
"""

import csv
import os
from datetime import datetime
from pathlib import Path

import psycopg
from dotenv import load_dotenv


def load_sql_file(filename: str) -> str:
    """Load SQL query from a file."""
    sql_path = Path(__file__).parent / "sql" / filename
    with open(sql_path, "r", encoding="utf-8") as f:
        return f.read()


def get_db_connection_string() -> str:
    """Build database connection string from environment variables."""
    load_dotenv()

    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([dbname, user, password]):
        raise ValueError("Missing required database credentials in .env file")

    return f"host={host} port={port} dbname={dbname} user={user} password={password}"


def execute_query(connection_string: str, sql: str):
    """Execute a SQL query and print results."""
    try:
        with psycopg.connect(connection_string, readonly=True) as conn:
            print("Connected (read-only mode)")

            with conn.cursor() as cur:
                cur.execute(sql)

                # Fetch and display results
                if cur.description:  # Check if query returns results
                    rows = cur.fetchall()
                    columns = [desc[0] for desc in cur.description]

                    # Generate filename with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_file = (
                        Path(__file__).parent / f"query_results_{timestamp}.csv"
                    )

                    # Write to CSV
                    with open(
                        output_file, "w", newline="", encoding="utf-8"
                    ) as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(columns)
                        writer.writerows(rows)

                        print(f"\nQuery returned {len(rows)} row(s)")
                        print(f"Results written to: {output_file}")
                else:
                    print(f"Query executed successfully. Rows affected: {cur.rowcount}")

    except psycopg.OperationalError as e:
        print(f"Connection Error: {e}")
    except psycopg.Error as e:
        print(f"Database Error: {e}")
    except (OSError, IOError) as e:
        print(f"File I/O Error: {e}")


def main():
    """Main function to run the database query example."""
    print("PostgreSQL Database Connection Example")
    print("=" * 80)

    # Get connection string
    try:
        conn_string = get_db_connection_string()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print(
            "\nPlease copy .env.example to .env and configure your database credentials."
        )
        return

    # Load SQL query from file
    sql_query = load_sql_file("queries.sql")

    # Split by semicolon and get the first non-empty query
    queries = [
        q.strip()
        for q in sql_query.split(";")
        if q.strip() and not q.strip().startswith("--")
    ]

    if queries:
        print("\nExecuting query from sql/queries.sql:\n")
        print(queries[0])
        print("\n" + "=" * 80 + "\n")

        execute_query(conn_string, queries[0])
    else:
        print("No queries found in sql/queries.sql")


if __name__ == "__main__":
    main()
