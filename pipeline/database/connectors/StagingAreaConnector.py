from database.connectors.GenericDatabaseConnector import GenericDatabaseConnector


class StagingAreaConnector(GenericDatabaseConnector):
    def __init__(self, section='database_staging_area'):
        super().__init__(section)
