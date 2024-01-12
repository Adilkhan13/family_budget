import pandas as pd
from google_drive import SpreadSheet, DrivePDFtoDF, Datasets

from config import PDF_FOLDER_ID_LIST

def get_last_rdate(data:pd.DataFrame, name:str)->str:
    """возвращает последний отчетный период за которые были загружены данные"""
    name = name.capitalize()
    data['date'] = pd.to_datetime(data['date'],format = '%Y-%m-%d')
    return data[data['name'] == name]['date'].max()

def transfer_data_from_drive_by_user(user_name:str, user_pdf_folde_id:str)->None:
    """Загружает данные с пдф в spreadsheet, убирает последний период и проверяет наличие предыдущих"""
    # pdf to dataframe
    g_drive = DrivePDFtoDF()
    # open spreadsheet
    used_files = SpreadSheet('used_files')
    main_sheet = SpreadSheet('main')
    
    # открывает директорию и проверяет на наличие новых файлов
    for file_name, file_id in g_drive.get_pdf_listdir(user_pdf_folde_id):
        # Уже прочитанные файлы пропускаются
        if file_id in used_files.get_df()['file_id'].unique():
            continue
        # последняя отчетная дата, если отчет уже был, то данные не будут меняться
        last_rdate = get_last_rdate(data = main_sheet.get_df(),name = user_name)

        # Базовая трансформация с pdf в pd.DataFrame
        raw_df = g_drive.pdf_to_df(file_id)
        # Категоризация и придание формата данным
        df = transform_kaspidf(raw_df,user_name)
        df['date'] = pd.to_datetime(df['date'])


        assert last_rdate > df['date'].min(), f'Не хватает промежутка, возьми период побольше last dwh date {last_rdate}, kaspi {df["date"].min()}'  

        # последняя дата отчета не берется так как она обычно не полная
        df = df[
                (df['date']<df['date'].max())&
                (df['date']>last_rdate)
            ].sort_values('date',ascending=True)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        # загружаем данные
        main_sheet.append_data(df)
        # отмечаем файл pdf как прочитанный
        used_files.append_data(pd.DataFrame({'file_name':[file_name],'file_id':[file_id]}))

def transfer_data_from_drive()->None:
    """
    Загружает данные с пдф в spreadsheet, убирает последний период и проверяет наличие предыдущих
    по всем пользователям
    """
    for user_name, user_pdf_folde_id in PDF_FOLDER_ID_LIST:
        transfer_data_from_drive_by_user(user_name, user_pdf_folde_id)


def transform_kaspidf(df:pd.DataFrame, name:str)-> pd.DataFrame:
    """
    Функция читает данные со стандартного отчета по затратам Каспи
    переименовывает указанные показатели в словаре
    и возвращает датафрейм
    """
    data = Datasets()
    replace_keys = data.get_keys()

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
    df['operation'] = df['operation'].str.upper()
    # add some new cols
    df['name'] = name.capitalize()
    df['comments'] = None
    
    df = df.sort_values('date',ascending = False)[['date','name','category_raw','category','operation','price','comments']]
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    return df