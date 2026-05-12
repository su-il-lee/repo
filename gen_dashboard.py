import pandas as pd
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('D:/claude/object_comments_20260414102809.xlsx')
df['ETL_DATE'] = df['ETL_DATE'].astype(str)
df = df.fillna('')

records = df[['BRAN_CD','BRAN_NM','BRAN_ENG_NM','ORNZ_NM_0','ORNZ_NM_1','ORNZ_NM_2','ORNZ_NM_DAM','ORNZ_NM_3','MGMT_INFO_EXPS_YN','TEAM_DEL_YN','ETL_DATE']].to_dict(orient='records')

by_div = df.groupby('ORNZ_NM_0').size().to_dict()
by_div2 = df.groupby('ORNZ_NM_2').size().to_dict()
by_dam = df.groupby('ORNZ_NM_DAM').size().to_dict()

etl_date = df['ETL_DATE'].iloc[0][:10]
total = len(df)
expo_y = int((df['MGMT_INFO_EXPS_YN']=='Y').sum())
expo_n = int((df['MGMT_INFO_EXPS_YN']=='N').sum())
del_y = int((df['TEAM_DEL_YN']=='Y').sum())
del_n = int((df['TEAM_DEL_YN']=='N').sum())
div_count = int(df['ORNZ_NM_0'].nunique())

div_labels = json.dumps(list(by_div.keys()), ensure_ascii=False)
div_values = json.dumps(list(by_div.values()))
div2_labels = json.dumps(list(by_div2.keys()), ensure_ascii=False)
div2_values = json.dumps(list(by_div2.values()))
dam_labels = json.dumps(list(by_dam.keys()), ensure_ascii=False)
dam_values = json.dumps(list(by_dam.values()))
all_data_json = json.dumps(records, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>브랜드 현황 대시보드 - {etl_date}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: Arial, "맑은 고딕", sans-serif; background: #f0f2f5; color: #333; }}
  .header {{ background: linear-gradient(135deg, #1a237e, #283593); color: white; padding: 24px 32px; }}
  .header h1 {{ font-size: 24px; font-weight: 700; }}
  .header p {{ font-size: 14px; opacity: 0.8; margin-top: 6px; }}
  .container {{ max-width: 1400px; margin: 0 auto; padding: 24px 32px; }}
  .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }}
  .kpi-card {{ background: white; border-radius: 10px; padding: 20px 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid; }}
  .kpi-card.blue {{ border-color: #1565c0; }}
  .kpi-card.green {{ border-color: #2e7d32; }}
  .kpi-card.orange {{ border-color: #e65100; }}
  .kpi-card.purple {{ border-color: #6a1b9a; }}
  .kpi-label {{ font-size: 12px; color: #888; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
  .kpi-value {{ font-size: 38px; font-weight: 700; margin: 6px 0 2px; }}
  .kpi-card.blue .kpi-value {{ color: #1565c0; }}
  .kpi-card.green .kpi-value {{ color: #2e7d32; }}
  .kpi-card.orange .kpi-value {{ color: #e65100; }}
  .kpi-card.purple .kpi-value {{ color: #6a1b9a; }}
  .kpi-sub {{ font-size: 12px; color: #aaa; }}
  .charts-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
  .chart-card {{ background: white; border-radius: 10px; padding: 20px 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 16px; }}
  .chart-title {{ font-size: 14px; font-weight: 700; color: #444; margin-bottom: 16px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
  .chart-wrap {{ position: relative; height: 240px; }}
  .table-card {{ background: white; border-radius: 10px; padding: 20px 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 24px; }}
  .table-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }}
  .table-header h2 {{ font-size: 15px; font-weight: 700; color: #444; }}
  .search-box {{ padding: 8px 14px; border: 1px solid #ddd; border-radius: 6px; font-size: 13px; width: 260px; outline: none; }}
  .search-box:focus {{ border-color: #1565c0; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ background: #f5f7fa; padding: 10px 12px; text-align: left; font-weight: 700; color: #555; border-bottom: 2px solid #e0e0e0; white-space: nowrap; }}
  td {{ padding: 9px 12px; border-bottom: 1px solid #f0f0f0; vertical-align: middle; }}
  tr:hover td {{ background: #f9fbff; }}
  .badge {{ display: inline-block; padding: 2px 9px; border-radius: 12px; font-size: 11px; font-weight: 600; }}
  .badge-y {{ background: #e8f5e9; color: #2e7d32; }}
  .badge-n {{ background: #ffebee; color: #c62828; }}
  .badge-del {{ background: #fff3e0; color: #e65100; }}
  .filter-bar {{ display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; }}
  .filter-btn {{ padding: 5px 14px; border: 1px solid #ddd; border-radius: 20px; font-size: 12px; cursor: pointer; background: white; color: #555; transition: all 0.2s; }}
  .filter-btn.active, .filter-btn:hover {{ background: #1565c0; color: white; border-color: #1565c0; }}
  .pagination {{ display: flex; justify-content: center; align-items: center; gap: 6px; margin-top: 16px; font-size: 13px; }}
  .page-btn {{ padding: 5px 10px; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; background: white; }}
  .page-btn.active {{ background: #1565c0; color: white; border-color: #1565c0; }}
  .page-btn:hover:not(.active) {{ background: #f0f4ff; }}
  .tag {{ display: inline-block; background: rgba(255,255,255,0.2); color: white; padding: 3px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
</style>
</head>
<body>
<div class="header">
  <h1>브랜드 현황 대시보드</h1>
  <p>기준 일자: <span class="tag">{etl_date}</span> &nbsp;|&nbsp; 파일: object_comments_20260414102809.xlsx</p>
</div>
<div class="container">

  <div class="kpi-grid">
    <div class="kpi-card blue">
      <div class="kpi-label">전체 브랜드</div>
      <div class="kpi-value">{total}</div>
      <div class="kpi-sub">등록된 브랜드 총합</div>
    </div>
    <div class="kpi-card green">
      <div class="kpi-label">관리정보 노출</div>
      <div class="kpi-value">{expo_y}</div>
      <div class="kpi-sub">노출(Y) {expo_y}건 / 미노출(N) {expo_n}건</div>
    </div>
    <div class="kpi-card orange">
      <div class="kpi-label">팀 삭제 브랜드</div>
      <div class="kpi-value">{del_y}</div>
      <div class="kpi-sub">삭제(Y) {del_y}건 / 유지(N) {del_n}건</div>
    </div>
    <div class="kpi-card purple">
      <div class="kpi-label">부문 수</div>
      <div class="kpi-value">{div_count}</div>
      <div class="kpi-sub">패션 · 코스메틱 · JAJU</div>
    </div>
  </div>

  <div class="charts-grid">
    <div class="chart-card" style="margin-bottom:0;">
      <div class="chart-title">부문별 브랜드 수 (1Level)</div>
      <div class="chart-wrap"><canvas id="chartPie"></canvas></div>
    </div>
    <div class="chart-card" style="margin-bottom:0;">
      <div class="chart-title">2레벨 조직별 브랜드 수</div>
      <div class="chart-wrap"><canvas id="chartDoughnut"></canvas></div>
    </div>
    <div class="chart-card" style="margin-bottom:0;">
      <div class="chart-title">노출 / 팀삭제 현황</div>
      <div class="chart-wrap"><canvas id="chartStatus"></canvas></div>
    </div>
  </div>

  <div class="chart-card">
    <div class="chart-title">담당(DAM)별 브랜드 수</div>
    <div style="position:relative;height:280px;"><canvas id="chartDam"></canvas></div>
  </div>

  <div class="table-card">
    <div class="table-header">
      <h2>브랜드 상세 목록 ({total}건)</h2>
      <input class="search-box" type="text" id="searchInput" placeholder="브랜드명 / 코드 검색..." oninput="filterTable()">
    </div>
    <div class="filter-bar">
      <button class="filter-btn active" onclick="setFilter('all', this)">전체 ({total})</button>
      <button class="filter-btn" onclick="setFilter('패션부문', this)">패션부문 ({by_div.get('패션부문',0)})</button>
      <button class="filter-btn" onclick="setFilter('코스메틱부문', this)">코스메틱부문 ({by_div.get('코스메틱부문',0)})</button>
      <button class="filter-btn" onclick="setFilter('JAJU본부', this)">JAJU본부 ({by_div.get('JAJU본부',0)})</button>
    </div>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>코드</th>
          <th>브랜드명</th>
          <th>영문명</th>
          <th>부문 (1Level)</th>
          <th>2레벨</th>
          <th>담당</th>
          <th>팀</th>
          <th>노출</th>
          <th>팀삭제</th>
          <th>ETL 일자</th>
        </tr>
      </thead>
      <tbody id="tableBody"></tbody>
    </table>
    <div class="pagination" id="pagination"></div>
  </div>
</div>

<script>
const allData = {all_data_json};
let filtered = [...allData];
let currentFilter = 'all';
let currentPage = 1;
const pageSize = 20;

function setFilter(val, btn) {{
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  currentFilter = val;
  currentPage = 1;
  filterTable();
}}

function filterTable() {{
  const q = document.getElementById('searchInput').value.toLowerCase();
  filtered = allData.filter(r => {{
    const matchDiv = currentFilter === 'all' || r.ORNZ_NM_0 === currentFilter;
    const matchSearch = !q || r.BRAN_NM.toLowerCase().includes(q) || r.BRAN_ENG_NM.toLowerCase().includes(q) || r.BRAN_CD.toLowerCase().includes(q);
    return matchDiv && matchSearch;
  }});
  currentPage = 1;
  renderTable();
}}

function renderTable() {{
  const tbody = document.getElementById('tableBody');
  const start = (currentPage - 1) * pageSize;
  const page = filtered.slice(start, start + pageSize);
  tbody.innerHTML = page.map((r, i) => `
    <tr>
      <td style="color:#bbb;">${{start + i + 1}}</td>
      <td><b>${{r.BRAN_CD}}</b></td>
      <td>${{r.BRAN_NM}}</td>
      <td style="color:#777;">${{r.BRAN_ENG_NM}}</td>
      <td>${{r.ORNZ_NM_0}}</td>
      <td>${{r.ORNZ_NM_2}}</td>
      <td>${{r.ORNZ_NM_DAM}}</td>
      <td>${{r.ORNZ_NM_3}}</td>
      <td><span class="badge ${{r.MGMT_INFO_EXPS_YN === 'Y' ? 'badge-y' : 'badge-n'}}">${{r.MGMT_INFO_EXPS_YN}}</span></td>
      <td><span class="badge ${{r.TEAM_DEL_YN === 'Y' ? 'badge-del' : 'badge-y'}}">${{r.TEAM_DEL_YN}}</span></td>
      <td style="color:#aaa;font-size:11px;">${{r.ETL_DATE.slice(0,10)}}</td>
    </tr>
  `).join('');
  renderPagination();
}}

function renderPagination() {{
  const total = Math.ceil(filtered.length / pageSize);
  const pg = document.getElementById('pagination');
  if (total <= 1) {{ pg.innerHTML = ''; return; }}
  let html = `<span style="color:#888;margin-right:8px;">${{filtered.length}}건 / ${{total}}페이지</span>`;
  for (let i = 1; i <= total; i++) {{
    html += `<button class="page-btn ${{i === currentPage ? 'active' : ''}}" onclick="goPage(${{i}})">${{i}}</button>`;
  }}
  pg.innerHTML = html;
}}

function goPage(p) {{ currentPage = p; renderTable(); }}

renderTable();

new Chart(document.getElementById('chartPie'), {{
  type: 'pie',
  data: {{
    labels: {div_labels},
    datasets: [{{ data: {div_values}, backgroundColor: ['#1565c0','#e65100','#2e7d32'], borderWidth: 2, borderColor: '#fff' }}]
  }},
  options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ position: 'bottom', labels: {{ font: {{ size: 11 }} }} }} }} }}
}});

new Chart(document.getElementById('chartDoughnut'), {{
  type: 'doughnut',
  data: {{
    labels: {div2_labels},
    datasets: [{{ data: {div2_values}, backgroundColor: ['#1565c0','#1976d2','#42a5f5','#90caf9','#e65100'], borderWidth: 2, borderColor: '#fff' }}]
  }},
  options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ position: 'bottom', labels: {{ font: {{ size: 10 }} }} }} }} }}
}});

new Chart(document.getElementById('chartStatus'), {{
  type: 'bar',
  data: {{
    labels: ['노출 Y', '노출 N', '팀삭제 Y', '팀삭제 N'],
    datasets: [{{ data: [{expo_y}, {expo_n}, {del_y}, {del_n}], backgroundColor: ['#2e7d32','#c62828','#e65100','#1565c0'], borderRadius: 4 }}]
  }},
  options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, ticks: {{ stepSize: 20 }} }} }} }}
}});

new Chart(document.getElementById('chartDam'), {{
  type: 'bar',
  data: {{
    labels: {dam_labels},
    datasets: [{{ label: '브랜드 수', data: {dam_values}, backgroundColor: '#1565c0', borderRadius: 4 }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{ x: {{ ticks: {{ font: {{ size: 11 }} }} }}, y: {{ beginAtZero: true, ticks: {{ stepSize: 5 }} }} }}
  }}
}});
</script>
</body>
</html>"""

with open('D:/claude/brand_dashboard_20260414.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('done')
