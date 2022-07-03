import requests
import json
import pandas as pd
import time
import logging
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer

"Create file to write logs. Default log_level - DEBUG"
logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)

"Set global var for connect to PostgreSQL "
db_name = 'database'
db_user = 'username'
db_pass = 'password'
db_host = 'db'
db_port = '5432'
db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
table_name = 'parsed_data'


def create_url(compound):
    """
    Create URL to download json.
    Main part of URL is the same in this task.
    :param compound: String. Last part of URL, with different in each URL.
    :return: String. Full URL.
    """
    logging.debug(f"Start creating URL with {compound}")

    default_url = "https://www.ebi.ac.uk/pdbe/graph-api/compound/summary"
    url = f"{default_url}/{compound}"
    logging.info(f"Created URL: {url}")
    return url


def get_json(url):
    """
    Download text from site and create json.
    Before making request it will wait 1 sec to not crush the opensource API.
    :param url: String. Full URL to connect.
    :return: String or None. Loaded data in json format or None to catch it later.
    """
    logging.debug(f"Wait 1 sec before making request to {url}")
    time.sleep(1)
    logging.info(f"Try to make request to {url}")
    try:
        req = requests.get(url)
        json_text = json.loads(req.text)

        return json_text
    except Exception as e:
        logging.error(f"Can`t reach {url}: {str(e)}")
        return None


def make_row(comp, short):
    """
    Create 1 row for DataFrame by parsing json.
    :param comp: String. Compound to insert in 1st column.
    :param short: dict. One name part of json.
    :return: list. One row to insert in DataFrame.
    """
    logging.debug(f"Parse {comp} json to one row")
    row = [
        comp,
        short['name'],
        short['formula'],
        short['inchi'],
        short['inchi_key'],
        short['smiles'],
        len(short['cross_links'])
    ]
    return [row]


def print_df(df):
    """
    Set options to correct print DataFrame.
    No limits in row/columns. Display 10 chars if string longer.
    :param df: DataFrame. What to print.
    :return: None.
    """
    logging.debug(f"Set options for printing DataFrame")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 14)
    print(df)


def create_table(db_engine):
    """
    Check if table not exist in database and create it.
    :param db_engine: MockConnection. Sqlalchemy engine to database.
    :return: None.
    """
    logging.debug(f"Check if table {table_name} exist")
    if not db_engine.dialect.has_table(db_engine.connect(), table_name):
        logging.debug(f"Creating table {table_name}")
        metadata = MetaData(db_engine)
        Table(table_name, metadata,
              Column('compound', String),
              Column('name', String),
              Column('formula', String),
              Column('inchi', String),
              Column('inchi_key', String),
              Column('smiles', String),
              Column('cross_links_count', Integer),
              )
        metadata.create_all()
    logging.info(f"Table {table_name} exist")


def main(*args, **kwargs):
    logging.info(f"Start program")
    # List of compounds from task
    compounds = ['ADP', 'ATP', 'STI', 'ZID', 'DPM', 'XP9', '18W', '29P']
    # List of columns of DataFrame
    cols = ['compound', 'name', 'formula', 'inchi', 'inchi_key', 'smiles', 'cross_links_count']
    # List to insert rows of DataFrame
    data = []

    # For itch compound create URL, connect, load data, parse and add to data list
    for comp in compounds:
        url = create_url(comp)
        json_text = get_json(url)

        if json_text:
            for i in range(len(json_text[comp])):
                data += make_row(comp, json_text[comp][i])

    # Create DataFrame from loaded data
    logging.info(f"Create DataFrame")
    df = pd.DataFrame(data, columns=cols)

    print_df(df)

    # Create SQLalchemy engine to postgreSQL
    logging.info(f"Create SQLalchemy engine to {db_host} {db_name}")
    db_engine = create_engine(db_url)

    # Create table if not exist
    create_table(db_engine)

    # Insert DataFrame to existed table
    logging.info(f"Insert DataFrame into table {table_name}")
    df.to_sql(table_name, con=db_engine, index=False, if_exists='append')

    logging.info(f"End program")


if __name__ == "__main__":
    main()
