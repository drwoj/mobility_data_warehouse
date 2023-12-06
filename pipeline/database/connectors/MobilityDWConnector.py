from database.connectors.GenericDatabaseConnector import GenericDatabaseConnector


class MobilityDWConnector(GenericDatabaseConnector):
    def __init__(self, section='database_mobility_dw'):
        super().__init__(section)
