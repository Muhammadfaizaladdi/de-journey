import os
import sys
import pandas as pd

import psycopg

INPUT = os.getenv('INPUT_PATH', '/app/data/customers.csv')
OUTPUT = os.getenv('OUTPUT_PATH', '/app/output/customers_clean.csv')
REJECT = os.getenv('REJECT_PATH', '/app/output/customers_reject.csv')

def run():
    df = pd.read_csv(INPUT)
    df['name'] = df['name'].str.strip()
    df['email'] = df['email'].str.strip().str.lower()
    df['country'] = df['country'].fillna('UNKNOWN')
    df = df.drop_duplicates(subset=['customer_id'], keep='first')
    valid_mask = df['email'].str.contains('@', na=False)
    df[valid_mask].to_csv(OUTPUT, index=False)
    df[~valid_mask].to_csv(REJECT, index=False)
    print(f'valid={valid_mask.sum()} rejected={(~valid_mask).sum()}')

    return df[valid_mask].values.tolist()


def load(rows):
    conninfo = (
        f"host={os.environ['DB_HOST']} "
        f"dbname={os.environ['DB_NAME']} "
        f"user={os.environ['DB_USER']} "
        f"password={os.environ['DB_PASSWORD']}"
    )
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    country TEXT NOT NULL,
                    signup_date DATE NOT NULL
                )
            ''')
            print("inserting data")
            for row in rows:
                cur.execute('''
                    INSERT INTO customers VALUES (%s,%s,%s,%s,%s)
                    ON CONFLICT (customer_id) DO UPDATE SET
                      name=EXCLUDED.name, email=EXCLUDED.email,
                      country=EXCLUDED.country, signup_date=EXCLUDED.signup_date
                ''', tuple(row))

if __name__ == '__main__':
    try:
        data = run()
        print(data)
        load(data)
        print("load success")
    except Exception as exc:
        print(f'pipeline_failed: {exc}', file=sys.stderr)
        sys.exit(1)
