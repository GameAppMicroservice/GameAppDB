import time
from pathlib import Path
from urllib.parse import quote

import psycopg

# Replace these placeholders with your Amazon RDS PostgreSQL connection values.
RDS_HOST = 'database-1.c7me6e2egbky.ap-northeast-1.rds.amazonaws.com'
RDS_PORT = 5432
RDS_DATABASE = 'postgres'
RDS_USERNAME = 'manoj'
RDS_PASSWORD = 'Manoj1234'
CONNECT_ATTEMPTS = 12


def database_url() -> str:
    return (
        f'postgresql://{quote(RDS_USERNAME, safe="")}:{quote(RDS_PASSWORD, safe="")}'
        f'@{RDS_HOST}:{RDS_PORT}/{RDS_DATABASE}?sslmode={RDS_SSLMODE}'
    )


def connect_with_retry() -> psycopg.Connection:
    for attempt in range(1, CONNECT_ATTEMPTS + 1):
        try:
            return psycopg.connect(database_url())
        except psycopg.OperationalError as error:
            if attempt == CONNECT_ATTEMPTS:
                raise
            print(f'Database connection attempt {attempt}/{CONNECT_ATTEMPTS} failed: {error}', flush=True)
            time.sleep(5)
    raise RuntimeError("Unable to connect to PostgreSQL.")


def main() -> None:
    schema = Path(__file__).with_name('schema.sql').read_text(encoding='utf-8')
    with connect_with_retry() as connection:
        with connection.cursor() as cursor:
            cursor.execute(schema)
        connection.commit()
    print('Database migration completed successfully.', flush=True)


if __name__ == '__main__':
    main()