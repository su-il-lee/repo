from news_fetcher   import fetch_news
from claude_analyzer import analyze
from ppt_generator  import generate_ppt
from mailer         import send_mail

def main():
    print("1. 뉴스 수집 중...")
    articles = fetch_news()

    print("2. Claude AI 분석 중...")
    analysis = analyze(articles)

    print("3. PPT 생성 중...")
    ppt_path = generate_ppt(articles, analysis)

    print("4. 메일 발송 중...")
    send_mail(ppt_path)

    print("완료!")

if __name__ == "__main__":
    main()