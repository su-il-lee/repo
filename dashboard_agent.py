"""
Dashboard Agent
- D:\claude 폴더에서 가장 최근 타임스탬프(YYYYMMDDHHMMSS.csv) CSV 파일을 자동 탐색
- 데이터를 분석하여 자동으로 HTML 대시보드 생성
- 사용법: python dashboard_agent.py
"""

import os
import re
import glob
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ──────────────────────────────────────────
# 1. 가장 최근 타임스탬프 CSV 탐색
# ──────────────────────────────────────────
def find_latest_csv(directory):
    pattern = re.compile(r"^\d{14}\.csv$")
    candidates = [
        f for f in os.listdir(directory)
        if pattern.match(f)
    ]
    if not candidates:
        raise FileNotFoundError("타임스탬프 형식(YYYYMMDDHHMMSS.csv)의 CSV 파일이 없습니다.")
    candidates.sort(reverse=True)
    latest = candidates[0]
    print(f"[Agent] 최신 파일 선택: {latest}")
    return os.path.join(directory, latest), latest

# ──────────────────────────────────────────
# 2. 데이터 로드 및 타입 분류
# ──────────────────────────────────────────
def load_and_classify(filepath):
    df = pd.read_csv(filepath, encoding="utf-8-sig")
    print(f"[Agent] 데이터 로드 완료: {df.shape[0]}행 x {df.shape[1]}컬럼")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = [
        c for c in df.select_dtypes(include="object").columns
        if df[c].nunique() <= 30 and df[c].nunique() >= 2
    ]
    date_cols = [c for c in df.columns if "DATE" in c.upper() or "DT" in c.upper()]

    print(f"[Agent] 수치형: {numeric_cols}")
    print(f"[Agent] 범주형(≤30 unique): {categorical_cols}")
    return df, numeric_cols, categorical_cols, date_cols

# ──────────────────────────────────────────
# 3. 차트 생성
# ──────────────────────────────────────────
def build_charts(df, numeric_cols, categorical_cols, date_cols):
    charts = []

    # 합계 대상 수치 컬럼 탐색 (코드성 컬럼 제외)
    skip_keywords = ["CD", "NM", "DT", "YN", "NO", "ID", "SEQ"]
    metric_cols = [
        c for c in numeric_cols
        if not any(c.upper().endswith(k) or c.upper().startswith(k) for k in skip_keywords)
    ]
    metric_col = metric_cols[0] if metric_cols else (numeric_cols[0] if numeric_cols else None)

    def _bar(grouped, x_col, y_col, title, top_n=None):
        grouped = grouped.sort_values(y_col, ascending=False)
        if top_n:
            grouped = grouped.head(top_n)
        fig = px.bar(
            grouped, x=x_col, y=y_col,
            title=title,
            color=y_col,
            color_continuous_scale="Blues",
            text=y_col,
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(
            xaxis_tickangle=-35,
            margin=dict(t=50, b=80),
            height=420,
            coloraxis_showscale=False,
        )
        return fig

    # ── 1) 판매일자별 합계 — 비활성화 ──────────────────
    # (표시 안 함)

    # ── 2) 조직구분(팀)별 합계 (ORNZ_NM_3) ────────────
    if "ORNZ_NM_3" in df.columns and metric_col:
        grp = df.groupby("ORNZ_NM_3")[metric_col].sum().reset_index()
        grp.columns = ["조직구분(팀)", "합계"]
        fig = _bar(grp, "조직구분(팀)", "합계", f"조직구분(팀)별 합계 ({metric_col})")
        charts.append(fig.to_html(full_html=False, include_plotlyjs=False))

    # ── 3) 점포별 합계 (STOR_CD → STOR_NM) — 상위 30개 ──────────
    if "STOR_CD" in df.columns and metric_col:
        name_col = "STOR_NM" if "STOR_NM" in df.columns else "STOR_CD"
        grp_cols = ["STOR_CD"] + ([name_col] if name_col != "STOR_CD" else [])
        grp = df.groupby(grp_cols)[metric_col].sum().reset_index()
        grp["표시명"] = grp[name_col].astype(str)
        fig = _bar(grp, "표시명", metric_col, f"점포별 합계 ({metric_col}) — 상위 10", top_n=10)
        charts.append(fig.to_html(full_html=False, include_plotlyjs=False))

    # ── 4) 유통소분류별 합계 (DSBT_LGRP_CD → DSBT_LGRP_NM) ──
    if "DSBT_LGRP_CD" in df.columns and metric_col:
        name_col = "DSBT_LGRP_NM" if "DSBT_LGRP_NM" in df.columns else "DSBT_LGRP_CD"
        grp_cols = ["DSBT_LGRP_CD"] + ([name_col] if name_col != "DSBT_LGRP_CD" else [])
        grp = df.groupby(grp_cols)[metric_col].sum().reset_index()
        grp["표시명"] = grp[name_col].astype(str) if name_col in grp.columns else grp["DSBT_LGRP_CD"].astype(str)
        fig = _bar(grp, "표시명", metric_col, f"유통소분류별 합계 ({metric_col}) — 상위 10", top_n=10)
        charts.append(fig.to_html(full_html=False, include_plotlyjs=False))

    # ── 5) 브랜드별 합계 (BRAN_CD → BRAN_NM) ──────────
    if "BRAN_CD" in df.columns and metric_col:
        name_col = "BRAN_NM" if "BRAN_NM" in df.columns else "BRAN_CD"
        grp_cols = ["BRAN_CD"] + ([name_col] if name_col != "BRAN_CD" else [])
        grp = df.groupby(grp_cols)[metric_col].sum().reset_index()
        grp["표시명"] = grp[name_col].astype(str) if name_col in grp.columns else grp["BRAN_CD"].astype(str)
        fig = _bar(grp, "표시명", metric_col, f"브랜드별 합계 ({metric_col})")
        charts.append(fig.to_html(full_html=False, include_plotlyjs=False))

    # ── 지정 컬럼이 없을 경우 기존 자동 탐지 fallback ──
    if not charts:
        for col in categorical_cols[:6]:
            counts = df[col].value_counts().reset_index()
            counts.columns = [col, "COUNT"]
            fig = _bar(counts, col, "COUNT", f"{col} 분포")
            charts.append(fig.to_html(full_html=False, include_plotlyjs=False))

    return charts

# ──────────────────────────────────────────
# 4. 요약 통계 테이블
# ──────────────────────────────────────────
def build_summary_table(df):
    rows = [
        f"<tr><td>총 행 수</td><td>{df.shape[0]:,}</td></tr>",
        f"<tr><td>총 컬럼 수</td><td>{df.shape[1]}</td></tr>",
        f"<tr><td>결측값 있는 컬럼</td><td>{df.isnull().any().sum()}</td></tr>",
        f"<tr><td>중복 행</td><td>{df.duplicated().sum():,}</td></tr>",
    ]
    return "\n".join(rows)

# ──────────────────────────────────────────
# 5. 데이터 미리보기 테이블
# ──────────────────────────────────────────
def build_preview_table(df, n=10):
    preview = df.head(n)
    headers = "".join(f"<th>{c}</th>" for c in preview.columns)
    body_rows = ""
    for _, row in preview.iterrows():
        cells = "".join(f"<td>{v}</td>" for v in row.values)
        body_rows += f"<tr>{cells}</tr>\n"
    return headers, body_rows

# ──────────────────────────────────────────
# 6. HTML 대시보드 렌더링
# ──────────────────────────────────────────
def render_dashboard(filename, df, charts, summary_rows, preview_headers, preview_body):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chart_blocks = ""
    for i, chart_html in enumerate(charts):
        if i % 2 == 0:
            chart_blocks += '<div class="row">'
        chart_blocks += f'<div class="chart-box">{chart_html}</div>'
        if i % 2 == 1 or i == len(charts) - 1:
            chart_blocks += "</div>"

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>Dashboard - {filename}</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; color: #333; }}
  header {{ background: linear-gradient(135deg, #1a73e8, #0d47a1); color: white;
            padding: 24px 32px; display: flex; justify-content: space-between; align-items: center; }}
  header h1 {{ font-size: 1.6rem; }}
  header span {{ font-size: 0.85rem; opacity: 0.85; }}
  .container {{ max-width: 1400px; margin: 0 auto; padding: 24px 16px; }}
  .summary-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }}
  .summary-card {{ background: white; border-radius: 10px; padding: 20px; text-align: center;
                   box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
  .summary-card .label {{ font-size: 0.8rem; color: #888; margin-bottom: 6px; }}
  .summary-card .value {{ font-size: 1.8rem; font-weight: 700; color: #1a73e8; }}
  .section-title {{ font-size: 1.1rem; font-weight: 600; margin: 24px 0 12px; color: #444;
                    border-left: 4px solid #1a73e8; padding-left: 10px; }}
  .row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
  .chart-box {{ background: white; border-radius: 10px; padding: 16px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; }}
  .table-wrap {{ overflow-x: auto; background: white; border-radius: 10px;
                 padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 32px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
  th {{ background: #1a73e8; color: white; padding: 8px 10px; text-align: left; white-space: nowrap; }}
  td {{ padding: 7px 10px; border-bottom: 1px solid #eee; white-space: nowrap; }}
  tr:hover td {{ background: #f5f8ff; }}
  footer {{ text-align: center; padding: 20px; color: #aaa; font-size: 0.78rem; }}
</style>
</head>
<body>
<header>
  <h1>📊 Auto Dashboard</h1>
  <span>파일: {filename} &nbsp;|&nbsp; 생성: {now}</span>
</header>
<div class="container">

  <div class="section-title">요약</div>
  <div class="summary-grid">
    <div class="summary-card"><div class="label">총 행 수</div><div class="value">{df.shape[0]:,}</div></div>
    <div class="summary-card"><div class="label">총 컬럼 수</div><div class="value">{df.shape[1]}</div></div>
    <div class="summary-card"><div class="label">결측값 컬럼</div><div class="value">{df.isnull().any().sum()}</div></div>
    <div class="summary-card"><div class="label">중복 행</div><div class="value">{df.duplicated().sum():,}</div></div>
  </div>

  <div class="section-title">차트</div>
  {chart_blocks}

  <div class="section-title">데이터 미리보기 (상위 10행)</div>
  <div class="table-wrap">
    <table>
      <thead><tr>{preview_headers}</tr></thead>
      <tbody>{preview_body}</tbody>
    </table>
  </div>

</div>
<footer>Generated by Dashboard Agent &nbsp;|&nbsp; {now}</footer>
</body>
</html>"""
    return html

# ──────────────────────────────────────────
# Main
# ──────────────────────────────────────────
def main():
    filepath, filename = find_latest_csv(BASE_DIR)
    df, numeric_cols, categorical_cols, date_cols = load_and_classify(filepath)
    charts = build_charts(df, numeric_cols, categorical_cols, date_cols)
    summary_rows = build_summary_table(df)
    preview_headers, preview_body = build_preview_table(df)

    html = render_dashboard(filename, df, charts, summary_rows, preview_headers, preview_body)

    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    out_path = os.path.join(BASE_DIR, f"dashboard_{now_str}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[Agent] 대시보드 생성 완료: {out_path}")

if __name__ == "__main__":
    main()
