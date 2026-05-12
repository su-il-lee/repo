import pyodbc
import pandas as pd
import sys
import datetime

# 쿼리를 stdin 또는 첫 번째 인자로 받음
if len(sys.argv) >= 2:
    query = sys.argv[1]
else:
    query = sys.stdin.read().strip()

if not query:
    print("Usage: python 2ndStep.py \"<SQL 쿼리>\"  또는 stdin으로 쿼리 전달")
    sys.exit(1)

# InfoU.ini 파일에서 username과 password 읽기
with open("InfoU.ini", "r") as f:
    first_line = f.readline().strip()

slash_index = first_line.index("/")
username = first_line[:slash_index]
password = first_line[slash_index + 1:]

# Azure SQL 연결 정보
server = "synapse-workspace-si.sql.azuresynapse.net"
database = "sibidb"

conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Authentication=ActiveDirectoryPassword;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# 쿼리 실행 및 CSV 저장
with pyodbc.connect(conn_str) as conn:
    df = pd.read_sql(query, conn)

now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
output_file = f"{now_str}.csv"

df.to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"DONE: {len(df)} rows saved to {output_file}")
