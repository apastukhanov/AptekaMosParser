from datetime import datetime
from difflib import get_close_matches
from functools import partial
from multiprocessing import Pool
from pathlib import Path

from typing import List

import pandas as pd
from model import Model


def find(drug: str, info: List):
    drug_1st_word = ' '.join(drug.split(' ')[:2])
    search = list(filter(lambda x: str(x['drugName']).startswith(drug_1st_word),
                         info))
    if search:
        if len(search) > 1:
            names = [x['drugName'] for x in search]
            match = get_close_matches(drug, names)
            if match:
                return list(filter(lambda x: x['drugName'] == match[0],
                                   search))[0]['drugId']
        return search[0]['drugId']
    return None


def create_output_excel(model: Model):
    prices = pd.DataFrame(model.fetchall('prices',
                                         ['drug_id', 'parse_date', 'drug_name',
                                          'store_name', 'producers', 'price']))
    if prices.empty:
        return pd.DataFrame()

    prices['parse_date'] = pd.to_datetime(prices['parse_date'])
    dt = datetime.now().date()
    prices = prices.loc[prices['parse_date'].dt.date == dt].copy()

    drug_name = prices['drug_name'].values
    info = model.fetchall('drugs_info', ['drugId', 'drugName'])
    fn = partial(find, info=info)

    with Pool(10) as p:
        drug_ids = p.map(fn, drug_name)

    prices['drug_id_egk'] = drug_ids
    return prices[['drug_id_egk', 'drug_name', 'store_name', 'producers', 'price']].copy()


def save_excel(df: pd.DataFrame, dir_path: str):
    ts = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    path = Path(dir_path) / f'prices_{ts}.xlsx'
    with pd.ExcelWriter(path, engine='openpyxl') as w:
        df.to_excel(w, index=False, sheet_name='prices')