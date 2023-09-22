### This project allows you to visualize and track family income and expenses using open and free resources.

The project is based on a PDF bank statement from Kaspi Bank (most popular bank in Kazakhstan).
* **Streamlit**, a free hosting and visualization service, is used to host and visualize data.
* Data is stored in **Google Drive**, a free storage service.
* Integration with **Notion** also available, but not used. 

For integration you should specify secrets in Fastapi in yaml format: 
~~~yaml
[NOTION]
# Optional
NOTION_API_KEY = "secret_***"
NOTION_DB_ID = "***"

[GOOGLE]
GOOGLE_SPREADSHEET_KEY = "***"

[GOOGLE.GOOGLE_API_CREDS]
# get from google account manager
type = 
project_id = 
private_key_id = 
private_key = 
client_email = 
client_id = 
auth_uri = 
token_uri = 
auth_provider_x509_cert_url = 
client_x509_cert_url = 
universe_domain = 

[GOOGLE.GOOGLE_PDF_FOLDER_IDS]
# user pdf files from kaspi, separate for every user
ADILKHAN_PDF_FOLDER_ID = "***"
USER2_PDF_FOLDER_ID = "***"
...
~~~