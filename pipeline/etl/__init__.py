from data_ingestion.ingest_geolife import ingest_geolife
from data_ingestion.ingest_hannover import ingest_hannover
from database.DatabaseConnector import DatabaseConnector

if __name__ == "__main__":
    with DatabaseConnector() as db:
        ingest_hannover(db)
        ingest_geolife(db)
