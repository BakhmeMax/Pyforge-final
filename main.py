import requests
import json
import pandas as pd
import time
import logging

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

def create_url(compound):
    logging.debug(f"Start creating URL with {compound}")

    defoult_url = "https://www.ebi.ac.uk/pdbe/graph-api/compound/summary"
    url = f"{defoult_url}/{compound}"
    logging.info(f"Create URL: {url}")
    return url

def get_json(url):
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
    logging.debug(f"Set options for printing DataFrame")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 14)
    logging.info(f"Print DataFrame")
    print(df)

def main(*args, **kwargs):
    compounds = ['ADP', 'ATP', 'STI', 'ZID', 'DPM', 'XP9', '18W', '29P']
    cols = ['compound', 'name', 'formula', 'inchi', 'inchi_key', 'smiles', 'cross_links_count']
    data = []

    for comp in compounds:
        url = create_url(comp)
        json_text = get_json(url)

        for i in range(len(json_text[comp])):
            data += make_row(comp, json_text[comp][i])

    logging.info(f"Create DataFrame")
    df = pd.DataFrame(data, columns=cols)

    print_df(df)

if __name__ == "__main__":
    main()