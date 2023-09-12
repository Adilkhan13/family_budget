from google_drive import SpreadSheet
import pandas as pd 

def get_keys()->dict:
    keys_sheet = SpreadSheet(sheet_name='cat_keys')
    df = keys_sheet.get_df()
    df['category_raw'] = df['category_raw'].str.upper()
    keys_dict = df.set_index('category_raw')['category'].to_dict()
    return keys_dict

def get_categories()->list:
    keys_sheet = SpreadSheet(sheet_name='cat_keys')
    df = keys_sheet.get_df()
    return df['category'].unique().tolist()

def transform_kaspidf(df:pd.DataFrame, name:str, replace_keys:dict = get_keys())-> pd.DataFrame:
    """
    Функция читает данные со стандартного отчета по затратам Каспи
    переименовывает указанные показатели в словаре
    и возвращает датафрейм
    """

    df = df.rename(columns = {
            'Сумма':'price',
            'Детали':'category_raw',
            'Дата':'date',
            'Операция':'operation'
        })
    
    # set formats
    df['date'] = pd.to_datetime(df['date'],format = "%d.%m.%y")
    df['category_raw'] = df['category_raw'].astype(str).str.replace('\r',' ')
    df['price'] = df['price'].astype(str).str.split('\r').str[0]
    df['price'] = df['price'].astype(str).str.replace(" ₸",'').str.replace(" ",'').str.replace(",",'.').astype(float)
    # rename known cattegories
    # can be added in google sheet
    df['category'] = df['category_raw'].str.upper().replace(replace_keys)

    # add some new cols
    df['name'] = name.capitalize()
    df['comments'] = None
    
    df = df.sort_values('date',ascending = False)[['date','name','category_raw','category','price','comments']]
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    return df
