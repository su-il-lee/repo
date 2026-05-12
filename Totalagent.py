"""
Total Agent
1단계: PBconnect.py  - Azure Synapse 접속 확인
2단계: 2ndStep.py   - SQL 쿼리 입력 후 CSV 다운로드
3단계: dashboard_agent.py - 최신 CSV로 대시보드 생성
"""

import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_step(title, cmd, capture=False):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=capture, text=True)
    if capture:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    return result.returncode

def main():
    python = sys.executable

    # ── 1단계: 접속 확인 ──────────────────────────
    print("\n[1/3] Azure Synapse 접속 확인 중...")
    ret = subprocess.run(
        [python, "-c", f"""
import sys, os
sys.path.insert(0, r'{BASE_DIR}')
import pyodbc

with open(r'{BASE_DIR}/InfoU.ini', 'r') as f:
    first_line = f.readline().strip()
slash_index = first_line.index('/')
username = first_line[:slash_index]
password = first_line[slash_index + 1:]

server = 'synapse-workspace-si.sql.azuresynapse.net'
database = 'sibidb'
conn_str = (
    'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={{server}};'
    f'DATABASE={{database}};'
    f'UID={{username}};'
    f'PWD={{password}};'
    'Authentication=ActiveDirectoryPassword;'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
)
try:
    with pyodbc.connect(conn_str) as conn:
        print('SUCCESS: 접속 성공')
except Exception as e:
    print(f'FAIL: {{e}}')
    sys.exit(1)
"""],
        cwd=BASE_DIR, text=True, capture_output=True
    )
    print(ret.stdout.strip())
    if ret.stderr:
        print(ret.stderr.strip())
    if ret.returncode != 0 or "FAIL" in ret.stdout:
        print("\n접속 실패로 작업을 중단합니다.")
        sys.exit(1)

    # ── 2단계: 쿼리 입력 및 CSV 다운로드 ──────────
    print(f"\n{'='*50}")
    print("  [2/3] 데이터 다운로드")
    print(f"{'='*50}")

    # 멀티라인 입력 지원: stdin이 파이프면 전체 읽기, 터미널이면 빈 줄로 완료
    if not sys.stdin.isatty():
        query = sys.stdin.read().strip()
    else:
        print("\n실행할 SQL 쿼리를 입력하세요 (입력 완료 후 빈 줄 Enter):")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line == "" and lines:
                break
            lines.append(line)
        query = "\n".join(lines).strip()

    if not query:
        print("쿼리가 입력되지 않았습니다. 종료합니다.")
        sys.exit(1)

    ret = subprocess.run(
        [python, "2ndStep.py"],
        input=query,
        cwd=BASE_DIR, text=True, capture_output=True
    )
    output = ret.stdout + ret.stderr
    # UserWarning 제거 후 출력
    for line in output.splitlines():
        if "UserWarning" not in line and "Pandas4Warning" not in line and "select_dtypes" not in line and "pandas.pydata" not in line:
            print(line)
    if ret.returncode != 0:
        print("\nCSV 다운로드 실패로 작업을 중단합니다.")
        sys.exit(1)

    # ── 3단계: 대시보드 생성 ──────────────────────
    print(f"\n{'='*50}")
    print("  [3/3] 대시보드 생성")
    print(f"{'='*50}")
    ret = subprocess.run(
        [python, "dashboard_agent.py"],
        cwd=BASE_DIR, text=True, capture_output=True
    )
    output = ret.stdout + ret.stderr
    dashboard_file = None
    for line in output.splitlines():
        if "UserWarning" not in line and "Pandas4Warning" not in line and "select_dtypes" not in line and "pandas.pydata" not in line:
            print(line)
        if "dashboard_" in line and ".html" in line:
            # 경로 추출
            for token in line.split():
                if "dashboard_" in token and ".html" in token:
                    dashboard_file = token.strip()

    if ret.returncode != 0:
        print("\n대시보드 생성 실패.")
        sys.exit(1)

    # 브라우저 오픈
    if dashboard_file and os.path.exists(dashboard_file):
        os.startfile(dashboard_file)
        print(f"\n브라우저에서 대시보드를 열었습니다: {dashboard_file}")

    print(f"\n{'='*50}")
    print("  모든 작업이 완료되었습니다.")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
