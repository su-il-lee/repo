import pyodbc
import pandas as pd
import datetime

# InfoU.ini 파일에서 username과 password 읽기
with open("InfoU.ini", "r") as f:
    first_line = f.readline().strip()

slash_index = first_line.index("/")
username = first_line[:slash_index]
password = first_line[slash_index + 1:]

# Azure SQL 연결 정보
server = "synapse-workspace-si.sql.azuresynapse.net"
database = "sibidb"

# ODBC Driver 18 for SQL Server 설치 페이지
# https://learn.microsoft.com/ko-kr/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver17
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