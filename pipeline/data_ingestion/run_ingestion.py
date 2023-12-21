from data_ingestion.ingest_districts import ingest_districts
from data_ingestion.ingest_geolife import iterate_geolife_dataset
from data_ingestion.ingest_hannover import ingest_hannover
from prefect import flow
import database.sql_queries as sql
from database.connectors.StagingAreaConnector import StagingAreaConnector


@flow(name="run_ingestion")
def run_ingestion():
    with StagingAreaConnector() as connector:
        connector.execute_query(sql.drop_staging_area)
        connector.execute_query(sql.create_staging_area)
        ingest_hannover(connector)
        iterate_geolife_dataset(connector)
        ingest_districts(connector)
        connector.execute_query(sql.create_trajectory_from_points)
        connector.execute_query(sql.create_staging_area_indices)
        connector.execute_query(sql.spatial_join_trajectory_with_district)


if __name__ == "__main__":
    run_ingestion()
