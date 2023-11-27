from data_ingestion.ingest_geolife import iterate_geolife_dataset
from data_ingestion.ingest_hannover import ingest_hannover
from data_ingestion.database.DatabaseConnector import DatabaseConnector
from prefect import flow


@flow(name="run_ingestion")
def run_ingestion():
    with DatabaseConnector() as db:
        print('Begin truncating')
        db.truncate_and_restart_identity('point')
        print('trunating finished')
        ingest_hannover(db)
        iterate_geolife_dataset(db)


if __name__ == "__main__":
    run_ingestion()
