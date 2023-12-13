import os
from sqlalchemy import create_engine
from nad_ch.infrastructure.database import ModelBase
from nad_ch.config import DATABASE_URL


def main():
    engine = create_engine(DATABASE_URL)

    # Check if the database file already exists
    if os.path.exists(DATABASE_URL.split('///')[1]):
        print('Database already exists.')
    else:
        # Create all tables
        ModelBase.metadata.create_all(engine)
        print('Database initialized and tables created.')


if __name__ == '__main__':
    main()
