from data_ingestion.ingest_geolife import ingest_geolife
from data_ingestion.ingest_hannover import ingest_hannover
from data_ingestion.database.DatabaseConnector import DatabaseConnector
from prefect import flow


@flow(name="run_ingestion")
def run_ingestion():
    with DatabaseConnector() as db:
        ingest_hannover(db)
        ingest_geolife(db)


if __name__ == "__main__":
    run_ingestion()
