from dotenv import load_dotenv
import os

load_dotenv(encoding="utf-8")

GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
NEWS_API_KEY  = os.getenv("NEWS_API_KEY")
GMAIL_USER    = os.getenv("GMAIL_USER")
GMAIL_APP_PW  = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENTS    = os.getenv("RECIPIENTS", "").split(",")

KEYWORDS = ["AI 인공지능", "패션 AI", "K-뷰티 AI", "생성형 AI"]