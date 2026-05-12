import requests
from config import NEWS_API_KEY, KEYWORDS
from datetime import datetime, timedelta

def fetch_news():
    articles = []
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    for keyword in KEYWORDS:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": keyword,
            "from": week_ago,
            "language": "ko",
            "sortBy": "relevancy",
            "pageSize": 3,
            "apiKey": NEWS_API_KEY
        }
        res = requests.get(url, params=params).json()
        for a in res.get("articles", []):
            articles.append({
                "keyword": keyword,
                "title":   a["title"],
                "source":  a["source"]["name"],
                "url":     a["url"],
                "date":    a["publishedAt"][:10],
                "content": a.get("description", "")
            })
    return articles