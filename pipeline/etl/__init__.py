from etl.database.DatabaseConnector import DatabaseConnector


def truncate_all_tables(db: DatabaseConnector):
    print('Begin truncating')
    db.truncate_and_restart_identity('trajectory')
    db.truncate_and_restart_identity('weather')
    db.truncate_and_restart_identity('economy_indicator')
    db.truncate_and_restart_identity('district')
    db.truncate_and_restart_identity('city')
    db.truncate_and_restart_identity('fuel')
    db.truncate_and_restart_identity('date')
    print('truncating finished')


def run_etl():
    with DatabaseConnector() as db:
        truncate_all_tables(db)


if __name__ == "__main__":
    run_etl()
