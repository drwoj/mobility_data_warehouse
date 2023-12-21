from database.connectors.MobilityDWConnector import MobilityDWConnector
from database.sql_queries import insert_date, drop_mobility_db, create_mobility_dw
from etl.etl_process import main_etl


def prepare_etl():
    with MobilityDWConnector() as connector:
        connector.execute_query(drop_mobility_db)
        connector.execute_query(create_mobility_dw)
        connector.execute_query(insert_date)


if __name__ == "__main__":
    prepare_etl()
    main_etl()
