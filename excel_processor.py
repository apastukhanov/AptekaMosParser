from datetime import datetime
from difflib import get_close_matches
from pathlib import Path

import pandas as pd
from model import Model


def create_output_excel(model: Model):
    prices = pd.DataFrame(model.fetchall('prices',
                                         ['drug_id', 'drug_name',
                                          'store_name', 'producers', 'price']))
    info = model.fetchall('drugs_info', ['drugId', 'drugName'])

    def find(drug: str):
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

    prices['drug_id_egk'] = prices['drug_name'].apply(find)
    return prices[['drug_id_egk', 'drug_name', 'store_name', 'producers', 'price']].copy()


def save_excel(df: pd.DataFrame, dir_path: str):
    path = Path(dir_path) / f'prices_{datetime.now().date()}.xlsx'
    with pd.ExcelWriter(path, engine='openpyxl') as w:
        df.to_excel(w, index=False, sheet_name='prices')