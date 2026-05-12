from datetime import datetime
import os

def generate_ppt(articles, analysis_text):
    # PPT 대신 HTML 파일로 생성 (python-pptx 오류 우회)
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    date_str = datetime.now().strftime("%Y년 %m월 %d일")
    filename = "AI_뉴스클리핑_" + datetime.now().strftime("%Y%m%d") + ".html"
    output_path = os.path.join(output_dir, filename)

    # 분석 텍스트를 HTML로 변환
    lines = analysis_text.split("\n")
    html_lines = ""
    for line in lines:
        line = line.strip()
        if not line:
            html_lines += "<br>"
        elif line.startswith("####"):
            html_lines += f"<h3>{line.replace('####','').strip()}</h3>"
        elif line.startswith("###"):
            html_lines += f"<h2>{line.replace('###','').strip()}</h2>"
        elif line.startswith("- 제목:"):
            html_lines += f'<p class="title">{line}</p>'
        elif line.startswith("- 핵심"):
            html_lines += f'<p class="content">{line}</p>'
        elif line.startswith("- 팀"):
            html_lines += f'<p class="point">{line}</p>'
        else:
            html_lines += f"<p>{line}</p>"

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>AI 뉴스 클리핑 - {date_str}</title>
<style>
  body {{ font-family: 'Malgun Gothic', sans-serif; margin: 0; background: #f8faff; }}
  .cover {{ background: #0f172a; color: white; padding: 60px 80px; }}
  .cover h1 {{ font-size: 48px; margin: 0 0 16px; }}
  .cover p {{ color: #06b6d4; font-size: 18px; margin: 0; }}
  .content {{ max-width: 1000px; margin: 40px auto; padding: 0 40px; }}
  h2 {{ color: #0f172a; font-size: 24px; border-bottom: 2px solid #2563eb; padding-bottom: 8px; margin-top: 40px; }}
  h3 {{ color: #1e3a5f; font-size: 18px; margin: 24px 0 8px; }}
  .title {{ font-weight: bold; color: #0f172a; }}
  .content {{ color: #374151; }}
  .point {{ background: #eff6ff; border-left: 4px solid #2563eb; padding: 8px 16px; color: #1e3a5f; }}
  p {{ margin: 4px 0; line-height: 1.7; }}
</style>
</head>
<body>
<div class="cover">
  <h1>AI 뉴스 클리핑</h1>
  <p>{date_str} 주간 클리핑 | AI 모델 · 패션 AI · K-뷰티 AI · 규제·정책</p>
</div>
<div class="content">
{html_lines}
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("HTML 저장 완료: " + output_path)
    return output_path