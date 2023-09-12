from google_drive import SpreadSheet
import datetime
import pandas as pd 

def get_keys():
    keys_sheet = SpreadSheet(sheet_name='cat_keys')
    df = keys_sheet.get_df()
    keys_dict = df.set_index('category_raw')['category'].to_dict()
    return keys_dict

def get_categories():
    keys_sheet = SpreadSheet(sheet_name='cat_keys')
    df = keys_sheet.get_df()
    return df['category'].unique().tolist()

def get_kzdate():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    return now.date()

def transform_kaspidf(df,name,replace_keys = get_keys()):
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
    df['price'] = df['price'].astype(str).str.replace(" ₸",'').str.replace(" ",'').str.replace(",",'.').astype(float)
    # rename known cattegories
    # can be added in google sheet
    df['category'] = df['category_raw'].replace(replace_keys)

    # add some new cols
    df['name'] = name
    df['comments'] = None
    
    df = df[['date','name','category_raw','category','price','comments']].sort_values('date',ascending = False)
    df['date'] = df['date'].strftime('%Y-%m-%d')
    return df

def set_dtype(df):
    df['date'] = pd.to_datetime(df['date'],format = '%Y-%m-%d')
    df['price'] = df['price'].astype(str).str.replace("\xa0",'').str.replace(" ",'').str.replace(",",'.').astype(float)
    return df

def cut_dataset(df,mindate,maxdate = get_kzdate()):
    mask = (
        (df['date'].dt.date>mindate)&
        (df['date'].dt.date<maxdate)
    )
    df = df[mask]
