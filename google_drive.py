from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread
import pandas as pd
from io import BytesIO
import tabula

from config import GOOGLE_API_CREDS, GOOGLE_SPREADSHEET_KEY


class SpreadSheet():
    def __init__(self,sheet_name) -> None:
        # AUTH
        gc = gspread.service_account_from_dict(GOOGLE_API_CREDS)
        file = gc.open_by_key(GOOGLE_SPREADSHEET_KEY)
        # open sheet
        self.worksheet = file.worksheet(sheet_name)
        self.data = self.worksheet.get_all_values()
        self._row_count = len(self.data)
        self._start_row = self._row_count + 1

    def get_df(self) -> pd.DataFrame:
        """return data from SpreadSheet as pandas DataFrame"""
        df = pd.DataFrame(self.data[1:], columns=self.data[0])
        return df
    
    def append_data(self,df:pd.DataFrame) -> None:
        """append data without changing  old data"""
        self.worksheet.insert_rows(
            df.values.tolist(),
            self._start_row
            )
    
    def relace_data(self,df:pd.DataFrame) -> None:
        """clear all sheet and replace it with new data"""
        data  = [df.columns.to_list()] + df.values.tolist()
        self.worksheet.clear()
        self.worksheet.update(data)


class DrivePDFtoDF():
    def __init__(self) -> None:
        self.drive_service = self.auth()

    def auth(self):
        creds = service_account.Credentials.from_service_account_info(
            GOOGLE_API_CREDS, scopes=['https://www.googleapis.com/auth/drive']
            )
        drive_service = build('drive', 'v3', credentials=creds)
        return drive_service
    
    def get_pdf_listdir(self, folder_id)->list[str]:
        """
        list of pdf files in dir
            return (file_name,file_id) 
        """

        # List PDF files in the specified folder
        query = f"'{folder_id}' in parents and mimeType='application/pdf'"
        results = self.drive_service.files().list(q=query).execute()
        files_list = []
        for file in results.get('files', []):
            files_list.append((file['name'],file['id']))
        return files_list

    def pdf_to_df(self, pdf_file_id) ->pd.DataFrame:
        """transform pdf to df"""
        request = self.drive_service.files().get_media(fileId=pdf_file_id)
        pdf_bytes = request.execute()
        df_list = tabula.read_pdf(BytesIO(pdf_bytes), pages='all',pandas_options ={'header':None})

        # пропускаем блок с общими данными
        df = pd.concat(df_list[1:])
        # Вытаскиваем наименования колонок
        col_names = df.iloc[0]
        df = df.rename(columns = col_names)
        # Скипаем наименования колонок
        df = df.iloc[1:]
        assert df.columns.to_list() == ['Дата', 'Сумма', 'Операция', 'Детали'], 'Колонки встали неправильно'
        return df


# main_sheet = SpreadSheet(sheet_name='main')
# main_sheet.append_data(pd.DataFrame({
#     'Date':['01-01-2023'],
#     'name':['TEST'],
#     'category_raw':['TEST'],
#     'category':['TEST'],
#     ' price':[-1000],
#     'comments':['']}))
# main_sheet.relace_data(main_sheet.get_df())