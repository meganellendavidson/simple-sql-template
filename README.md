# PostgreSQL Database Template with psycopg3

A template for connecting to PostgreSQL databases using psycopg3 with Poetry dependency management.

## Setup

### 1. Install Poetry (if not already installed)

### 2. Install Dependencies

```bash
poetry install
```

### 3. Configure Database Connection

Edit `.env` with your actual database credentials:

### 4. Add Your SQL Queries

Edit `src/sql/queries.sql` to add your SQL queries.

## Usage

Run the script using Poetry:

```bash
poetry run python src/main.py
```

Or activate the virtual environment first:

```bash
poetry shell
python src/main.py
```

## Customization

### Execute a Specific Query

Modify [src/main.py](src/main.py) to select which query from `queries.sql` to execute, or pass query files as arguments.

### Add More SQL Files

Create additional `.sql` files in the `src/sql/` directory and use `load_sql_file()` to load them.

## Dependencies

- **psycopg[binary]** ^3.1.18 - PostgreSQL adapter (with C optimizations)
- **python-dotenv** ^1.0.0 - Environment variable management

## Notes

- The `.env` file is excluded from git (see `.gitignore`)
- Never commit database credentials to version control
- psycopg3 uses context managers for automatic connection cleanup
