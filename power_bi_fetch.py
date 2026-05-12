# power_bi_fetch.py
import requests

# 1. 액세스 토큰 발급
def get_token(tenant_id, client_id, client_secret):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://analysis.windows.net/powerbi/api/.default"
    }
    return requests.post(url, data=data).json()["access_token"]

# 2. DAX 쿼리로 데이터 가져오기
def fetch_data(token, dataset_id, dax_query):
    url = f"https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/executeQueries"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {"queries": [{"query": dax_query}], "serializerSettings": {"includeNulls": True}}
    return requests.post(url, headers=headers, json=body).json()