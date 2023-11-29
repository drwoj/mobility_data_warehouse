from database.connectors.MobilityDWConnector import MobilityDWConnector
from database.sql_queries import insert_date

tables_to_truncate = ['trajectory', 'weather', 'economy_indicator', 'district', 'city', 'fuel', 'date']


def run_etl():
    with MobilityDWConnector() as connector:
        for table in tables_to_truncate:
            connector.truncate_and_restart_identity(table)

        connector.execute_insert_query(insert_date)


if __name__ == "__main__":
    run_etl()
