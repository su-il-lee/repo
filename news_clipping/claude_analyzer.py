from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def analyze(articles):
    news_text = "\n".join([
        f"[{a['keyword']}] {a['title']} ({a['source']}, {a['date']})\n{a['content']}"
        for a in articles
    ])

    prompt = f"""다음 뉴스들을 팀 공유용 클리핑으로 정리해주세요.
각 뉴스마다 아래 형식으로 작성해주세요:
- 제목: (한 줄 요약)
- 핵심 내용: (2~3줄)
- 팀 관련 포인트: (우리 팀에 주는 시사점 한 줄)

뉴스 목록:
{news_text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )

    content = response.choices[0].message.content

    # 빈 응답 방어 처리
    if not content:
        print("경고: Groq 응답이 비어있습니다. 뉴스 제목만으로 대체합니다.")
        content = "\n".join([
            f"- 제목: {a['title']}\n- 출처: {a['source']} ({a['date']})\n- 팀 관련 포인트: 추가 분석 필요\n"
            for a in articles
        ])

    return content