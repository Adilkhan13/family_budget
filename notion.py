from config import NOTION_API_KEY, NOTION_DB_ID
from notion_client import Client
import json
# import httpx

notion = Client(
    auth=NOTION_API_KEY,
#    client=httpx.Client(verify=False)
)

with open('./queries/test','r') as f:
    query = json.loads(f.read())

# Выполнение запроса
results = notion.databases.query(query=query, database_id=NOTION_DB_ID)
print(results)
