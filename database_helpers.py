""" Database helper functions """

import os
import psycopg2
import sqlalchemy
import pandas as pd
from dotenv import load_dotenv
from typing import List, Dict


load_dotenv()
DATABASE = os.environ["DATABASE"]
USER = os.environ["USER"]
HOST = os.environ["HOST"]
PASS = os.environ["PASS"]
PORT = os.environ["PORT"]


def validate_pgql() -> List:
    """
    Connects to pgql, fetches all aggregate data for validation
    """
    with psycopg2.connect(
            database=DATABASE,
            user=USER,
            host=HOST,
            password=PASS,
            port=PORT
        ) as conn:

        cur = conn.cursor()
        cur.execute(
            """
            select * from tissue_aggregates
            """
        )
        result = cur.fetchall()

        return result


def import_data_pgql(
        mouse_tissue_atlas: pd.DataFrame,
        mouse_tissue_atlas_aggregates: pd.DataFrame
        ) -> None:
    """
    Uploads data to pgql
    """
    database_url = "postgresql+psycopg2://justinguiel:pass123@localhost:5432/test_db"
    db_engine = sqlalchemy.create_engine(database_url)
    mouse_tissue_atlas.to_sql("mouse_tissue_atlas", db_engine, if_exists='replace')
    mouse_tissue_atlas_aggregates.to_sql("tissue_aggregates", db_engine, if_exists='replace')
    db_engine.dispose()


def manual_dataframe_setup(atlas_cols: List[str]) -> Dict:
    """
    Manual creates columns and dtype
    """

    data_types = [sqlalchemy.types.String(length=256)]*7
    data_types.extend([sqlalchemy.types.Float()]*10)
    data_type_dict = {atlas_cols[i]: data_types[i] for i in range(len(data_types))}
    
    return data_type_dict

print((validate_pgql()))