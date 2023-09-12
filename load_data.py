import pandas as pd
from google_drive import SpreadSheet, DrivePDFtoDF
from config import ADILKHAN_PDF_FOLDER_ID, BALZHAN_PDF_FOLDER_ID
from transform import transform_kaspidf


def get_last_rdate(data:pd.DataFrame, name:str)->str:
    """возвращает последний отчетный период за которые были загружены данные"""
    name = name.capitalize()
    data['date'] = pd.to_datetime(data['date'],format = '%Y-%m-%d')
    return data[data['name'] == name]['date'].max().strftime('%Y-%m-%d')

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

        assert last_rdate > df['date'].min(), 'Не хватает промежутка, возьми период побольше'

        # последняя дата отчета не берется так как она обычно не полная
        df = df[
                (df['date']<df['date'].max())&
                (df['date']>last_rdate)
            ].sort_values('date',ascending=True)
        
        # загружаем данные
        main_sheet.append_data(df)
        # отмечаем файл pdf как прочитанный
        used_files.append_data(pd.DataFrame({'file_name':[file_name],'file_id':[file_id]}))

def transfer_data_from_drive()->None:
    """
    Загружает данные с пдф в spreadsheet, убирает последний период и проверяет наличие предыдущих
    по всем пользователям
    """
    for user_name, user_pdf_folde_id in [
            ('Adilkhan', ADILKHAN_PDF_FOLDER_ID),
            ('Balzhan', BALZHAN_PDF_FOLDER_ID)
        ]:
        transfer_data_from_drive_by_user(user_name, user_pdf_folde_id)