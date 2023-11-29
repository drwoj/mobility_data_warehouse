from etl.database.DatabaseConnector import DatabaseConnector
from etl.sql_queries import insert_date

tables_to_truncate = ['trajectory', 'weather', 'economy_indicator', 'district', 'city', 'fuel', 'date']


def run_etl():
    with DatabaseConnector() as db:
        for table in tables_to_truncate:
            db.truncate_and_restart_identity(table)
        db.execute_insert_query(insert_date)


if __name__ == "__main__":
    run_etl()
