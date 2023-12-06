from data_ingestion.ingest_districts import ingest_districts
from data_ingestion.ingest_geolife import iterate_geolife_dataset
from data_ingestion.ingest_hannover import ingest_hannover
from prefect import flow

from database.connectors.StagingAreaConnector import StagingAreaConnector


@flow(name="run_ingestion")
def run_ingestion():
    with StagingAreaConnector() as connector:
        print('Begin truncating')
        connector.truncate_and_restart_identity('point')
        print('trunating finished')
        ingest_hannover(connector)
        iterate_geolife_dataset(connector)
        ingest_districts()


if __name__ == "__main__":
    run_ingestion()
